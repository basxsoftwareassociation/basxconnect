import bread
import htmlgenerator as hg
from bread import layout
from bread.layout.components import tag
from bread.layout.components.icon import Icon
from bread.utils import ModelHref
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils.formats import localize
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts.editperson.common.utils import tile_with_icon
from basxconnect.core.models import Person
from basxconnect.mailer_integration.models import Interest, Subscription

R = bread.layout.grid.Row
C = bread.layout.grid.Col


def mailer_integration_tile(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    addresses = person.core_email_list.all()
    return tile_with_icon(
        Icon("email--new"),
        hg.H4(
            _("Email Subscriptions"),
        ),
        *[_display_subscription(email) for email in addresses]
        if hasattr(person, "core_email_list") and person.core_email_list.count() > 0
        else C(_("Person has no email addresses")),
    )


def _display_subscription(email):
    if not hasattr(email, "subscription"):
        return _display_email_without_subscription(email)
    subscription = email.subscription
    modal = modal_edit_subscription(subscription)
    interests = [
        R(
            C(interest, width=6, breakpoint="lg"),
            C(
                is_interested_indicator(interest in subscription.interests.all()),
                breakpoint="lg",
            ),
            style="padding-bottom: 24px;",
        )
        for interest in Interest.objects.all()
    ]
    return hg.BaseElement(
        R(
            C(
                hg.SPAN(email.email, style="font-weight: bold;"),
                tag.Tag(
                    _(subscription.status),
                    tag_color=map_tag_color(subscription.status),
                    onclick="return false;",
                    style="margin-left: 1rem;",
                ),
                hg.SPAN(
                    subscription.get_language_display(),
                    style="padding-left:0.5rem;",
                ),
                style="margin-bottom: 1.5rem;",
            ),
        ),
        *interests,
        R(
            C(_("Last synchronized"), width=6, breakpoint="lg"),
            C(
                localize(
                    localtime(subscription.latest_sync.sync_completed_datetime),
                    use_l10n=settings.USE_L10N,
                )
                if hasattr(subscription.latest_sync, "sync_completed_datetime")
                else "",
                breakpoint="lg",
            ),
            style="padding-bottom: 24px;",
        ),
        R(
            C(
                layout.button.Button(
                    "Edit",
                    buttontype="tertiary",
                    icon="edit",
                    **modal.openerattributes,
                ),
                modal,
                style="margin-top: 1.5rem;margin-bottom: 3rem;",
            )
        ),
    )


def _display_email_without_subscription(email):
    modal_add = modal_add_subscription(email)
    return hg.BaseElement(
        hg.DIV(email.email, style="font-weight: bold;"),
        hg.DIV(_("No subscription yet for "), email.email),
        layout.button.Button(
            _("Add subscription"),
            buttontype="ghost",
            icon="add",
            **modal_add.openerattributes,
        ),
        modal_add,
    )


def map_tag_color(status):
    mapping = {"subscribed": "green"}
    return mapping.get(status, "gray")


def is_interested_indicator(is_subscribed):
    if is_subscribed:
        color = "#198038"
        text = _("active")
    else:
        color = "#e0e0e0"
        text = _("inactive")
    return hg.DIV(
        hg.DIV(
            "",
            style=f"height: 8px; width: 8px; background-color: {color}; border-radius: 50%; display: inline-block;",
        ),
        hg.DIV(text, style="display: inline-block; padding-left: 8px"),
        style="display: inline-block;",
    )


def modal_edit_subscription(mailingpreferences):
    modal = layout.modal.Modal.with_ajax_content(
        heading=_("Edit subscription"),
        url=ModelHref(
            Subscription,
            "ajax_edit",
            kwargs={"pk": mailingpreferences.pk},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )
    modal[0][1].attributes["style"] = "overflow: visible"
    modal[0].attributes["style"] = "overflow: visible"
    return modal


def modal_add_subscription(email: models.Email):
    ret = layout.modal.Modal.with_ajax_content(
        heading=_("Add subscription"),
        url=ModelHref(
            Subscription,
            "ajax_add",
            query={"asajax": True, "email": email.pk, "status": "subscribed"},
        ),
        submitlabel=_("Save"),
    )
    ret[0][1].attributes["style"] = "overflow: visible"
    ret[0].attributes["style"] = "overflow: visible"
    return ret
