import bread
import htmlgenerator as hg
from bread.layout.components import icon, tag
from bread.layout.components.icon import Icon
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import editperson
from basxconnect.core.models import Person
from basxconnect.mailer_integration.models import Interest

R = bread.layout.grid.Row
C = bread.layout.grid.Col


def mailer_integration_tile(request):

    person = get_object_or_404(Person, pk=request.resolver_match.kwargs["pk"])
    return editperson.tile_with_icon(
        Icon("email--new"),
        C(
            _display_mailingpreferences(person.mailingpreferences)
            if hasattr(person, "mailingpreferences")
            else hg.DIV("Person has not been linked to a Mailchimp contact"),
            style="padding-bottom: 1rem;",
        ),
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


def _display_mailingpreferences(mailingpreferences):

    interests = [
        R(
            C(hg.DIV(interest, style="font-weight: bold;"), width=6, breakpoint="lg"),
            C(
                is_interested_indicator(interest in mailingpreferences.interests.all()),
                breakpoint="lg",
            ),
            style="padding-top: 24px;",
        )
        for interest in Interest.objects.all()
    ]
    return hg.BaseElement(
        R(
            C(
                hg.H4(
                    _("Email Subscriptions"),
                )
            ),
            C(
                tag.Tag(
                    _(mailingpreferences.status),
                    tag_color=map_tag_color(mailingpreferences.status),
                    onclick="return false;",
                ),
            ),
        ),
        *interests,
    )
