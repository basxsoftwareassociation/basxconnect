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
from basxconnect.mailer_integration.help import sync_help_modal
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

    help_modal = sync_help_modal()
    return hg.BaseElement(
        Form(
            forms.Form(),
            bread.layout.grid.Grid(
                hg.H3(_("Synchronization of Email Subcriptions")),
                notification,
                gutter=False,
            ),
            help_modal,
            layout.forms.helpers.Submit(
                _("Download subscriptions"), style="display: inline-block;"
            ),
            layout.button.Button(
                _("Help"),
                buttontype="ghost",
                style="margin-left: 1rem",
                icon="help",
                **help_modal.openerattributes,
            ),
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
        settings.MAILER.add_person(MailerPerson.from_subscription(self.object))
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
        settings.MAILER.put_person(MailerPerson.from_subscription(self.object))
        return result
