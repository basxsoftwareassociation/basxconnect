from django.utils.html import mark_safe

from . import models, settings


def basxconnect_core(request):
    return {
        "PLATFORMNAME": mark_safe('basx <span style="font-weight: 600">Connect</span>'),
        "COMPANYNAME": models.Person.objects.filter(pk=settings.OWNER_PERSON_ID).first()
        or "<Missing Owner>",
    }
