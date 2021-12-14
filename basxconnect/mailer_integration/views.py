import traceback

import bread.layout.components.notification
import htmlgenerator as hg
from bread import layout, menu
from bread.layout.components.datatable import DataTableColumn
from bread.layout.components.forms import Form
from bread.utils import aslayout, reverse_model
from bread.utils.links import Link, ModelHref
from bread.views import AddView, EditView
from django import forms
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from basxconnect.mailer_integration import settings
from basxconnect.mailer_integration.abstract.mailer import MailerPerson
from basxconnect.mailer_integration.mailchimp import mailer
from basxconnect.mailer_integration.models import (
    SynchronizationPerson,
    SynchronizationResult,
)
from basxconnect.mailer_integration.synchronize import synchronize

C = bread.layout.grid.Col
R = bread.layout.grid.Row


@aslayout
def mailer_synchronization_view(request):
    if request.method == "POST":
        try:
            sync_result = synchronize(settings.MAILER)
            notification = bread.layout.components.notification.InlineNotification(
                _("Sychronization successful"),
                _(
                    "Synchronized with mailer segment containing %s contacts. %s new persons were added to BasxConnect."
                )
                % (
                    sync_result.total_synchronized_persons,
                    sync_result.persons.filter(
                        sync_status=SynchronizationPerson.NEW
                    ).count(),
                ),
                kind="success",
            )
        except Exception:
            notification = bread.layout.components.notification.InlineNotification(
                "Error",
                f"An error occured during synchronization. {traceback.format_exc()}",
                kind="error",
            )
    else:
        notification = None

    return hg.BaseElement(
        Form.wrap_with_form(
            forms.Form(),
            bread.layout.grid.Grid(
                hg.H3(_("Synchronization of Email Subcriptions")),
                R(
                    C(
                        _(
                            "The button below is currently the only way of getting new subcribers from the mailer into our system. Is it also the only way of getting updates for subscribers that we already have in our system. This is what happens when the button is pressed:"
                        ),
                        hg.UL(
                            hg.LI(
                                _(
                                    "For all the Subscriptions that are in the relevant segment (e.g. 'UM Switzerland') in the Mailer, we check whether the email address is already in BasxConnect."
                                ),
                                _class="bx--list__item",
                            ),
                            hg.LI(
                                _(
                                    "If an email address is already in BasxConnect, the downloaded subscription will be attached to the email address and override the current values in case there are any."
                                ),
                                _class="bx--list__item",
                            ),
                            hg.LI(
                                _(
                                    "If an email address is not yet in BasxConnect, a new person will be created with that email address."
                                ),
                                _class="bx--list__item",
                            ),
                            _class="bx--list--unordered",
                        ),
                        width=8,
                    )
                ),
                hg.If(notification is not None, notification),
                gutter=False,
            ),
            submit_label=_("Download subscriptions"),
        ),
        display_previous_execution(request),
    )


def display_previous_execution(request):
    return R(
        C(
            layout.datatable.DataTable.from_queryset(
                SynchronizationResult.objects.order_by("-sync_completed_datetime"),
                columns=[
                    "total_synchronized_persons",
                    "sync_completed_datetime",
                    DataTableColumn(
                        _("Newly added to BasxConnect"),
                        display_sync_persons(SynchronizationPerson.NEW),
                    ),
                    DataTableColumn(
                        _("In mailer segment but not added to BasxConnect"),
                        display_sync_persons(SynchronizationPerson.SKIPPED),
                    ),
                ],
                title=_("Previous Executions"),
                primary_button="",
                rowactions=[
                    Link(
                        href=ModelHref(
                            SynchronizationResult,
                            "delete",
                            kwargs={"pk": hg.C("row.pk")},
                            query={"next": request.get_full_path()},
                        ),
                        iconname="trash-can",
                        label=_("Delete"),
                    )
                ],
            ),
            width=16,
        )
    )


def display_sync_persons(sync_status):
    return hg.Iterator(
        hg.F(lambda c: c["row"].persons.filter(sync_status=sync_status)),
        "person",
        hg.DIV(
            hg.format(
                "{} {} <{}>",
                hg.C("person.first_name"),
                hg.C("person.last_name"),
                hg.C("person.email"),
            )
        ),
    )


tools_group = menu.Group(_("Tools"), iconname="tool", order=99)

menu.registeritem(
    menu.Item(
        Link(
            reverse_lazy(
                "basxconnect.mailer_integration.views.mailer_synchronization_view"
            ),
            settings.MAILER.name(),
            iconname="email",
        ),
        tools_group,
    )
)


class AddSubscriptionView(AddView):
    fields = ["interests", "language", "email", "status"]

    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        settings.MAILER.add_person(MailerPerson.from_mailing_preferences(self.object))
        return response


class EditSubscriptionView(EditView):
    fields = ["interests", "language"]

    def get_success_url(self):
        return reverse_model(
            self.object.email.person, "read", kwargs={"pk": self.object.email.person.pk}
        )

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        # TODO: https://github.com/basxsoftwareassociation/basxconnect/issues/140
        mailer.Mailchimp().put_person(
            MailerPerson.from_mailing_preferences(self.object)
        )
        return result
