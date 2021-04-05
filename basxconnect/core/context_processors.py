import htmlgenerator as hg
from bread import layout
from django.utils.html import mark_safe

from . import models, settings


def basxconnect_core(request):
    return {
        "headerlayout": layout.shell_header.ShellHeader(
            hg.C("PLATFORMNAME"),
            models.Person.objects.filter(pk=settings.OWNER_PERSON_ID).first(),
        ),
        "PLATFORMNAME": mark_safe('basx <span style="font-weight: 600">Connect</span>'),
    }
