import bread.layout
import htmlgenerator as hg
from django.utils.translation import gettext_lazy as _


def sync_help_modal():
    return bread.layout.modal.Modal(
        _("Help"),
        _(
            "The button below is currently the only way of getting new subcribers from the mailer into our system. Is it also the only way of getting updates for subscribers that we already have in our system. This is what happens when the button is pressed:"
        ),
        hg.DIV(
            hg.UL(
                hg.LI(
                    _(
                        "For all the Subscriptions that are in the relevant segment in the Mailer, we check whether the email address is already in BasxConnect."
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
            style="padding-left: 1rem;",
        ),
        width=8,
    )
