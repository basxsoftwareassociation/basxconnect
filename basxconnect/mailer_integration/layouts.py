import bread
import htmlgenerator as hg
from bread import layout
from bread.layout.components import tag
from bread.layout.components.icon import Icon
from bread.utils import reverse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.layouts import editperson
from basxconnect.core.models import Person
from basxconnect.mailer_integration.models import Interest

R = bread.layout.grid.Row
C = bread.layout.grid.Col


def mailer_integration_tile(request):
    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    addresses = person.core_email_list.all()
    return editperson.tile_with_icon(
        Icon("email--new"),
        hg.H4(
            _("Email Subscriptions"),
        ),
        *[_display_preferences(email) for email in addresses]
        if hasattr(person, "core_email_list") and person.core_email_list.count() > 0
        else C("Person has no email addresses"),
    )


def _display_preferences(email):
    if not hasattr(email, "mailingpreferences"):
        return _display_email_without_preferences(email)
    mailingpreferences = email.mailingpreferences
    modal = modal_edit_mailingpreferences(mailingpreferences)
    interests = [
        R(
            C(interest, width=6, breakpoint="lg"),
            C(
                is_interested_indicator(interest in mailingpreferences.interests.all()),
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
                    _(mailingpreferences.status),
                    tag_color=map_tag_color(mailingpreferences.status),
                    onclick="return false;",
                    style="margin-left: 1rem;",
                ),
                style="margin-bottom: 1.5rem;",
            ),
        ),
        *interests,
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


def _display_email_without_preferences(email):
    modal_add = modal_add_mailingpreferences(email)
    return hg.BaseElement(
        hg.DIV(email.email, style="font-weight: bold;"),
        hg.DIV(_("no mailing preferences yet for "), email.email),
        layout.button.Button(
            _("Add mailing preferences"),
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


def modal_edit_mailingpreferences(mailingpreferences):
    modal = layout.modal.Modal.with_ajax_content(
        heading=_("Edit Email Subscriptions"),
        url=reverse(
            "basxconnect.mailer_integration.views.editmailingpreferencesview",
            kwargs={"pk": mailingpreferences.pk},
            query={"asajax": True},
        ),
        submitlabel=_("Save"),
    )
    modal[0][1].attributes["style"] = "overflow: visible"
    modal[0].attributes["style"] = "overflow: visible"
    return modal


def modal_add_mailingpreferences(email: models.Email):
    ret = layout.modal.Modal.with_ajax_content(
        heading=_("Add Mailing Preferences"),
        url=reverse(
            "basxconnect.mailer_integration.views.addmailingpreferencesview",
            query={"asajax": True, "email": email.pk, "status": "subscribed"},
        ),
        submitlabel=_("Save"),
    )
    ret[0][1].attributes["style"] = "overflow: visible"
    ret[0].attributes["style"] = "overflow: visible"
    return ret
