from django.utils.html import mark_safe
from dynamic_preferences.registries import global_preferences_registry

from basxconnect.core.views.person.search_person_view import searchbar


def basxconnect_core(request):
    return {
        "PLATFORMNAME": mark_safe('basx <span style="font-weight: 600">Connect</span>'),
        "COMPANYNAME": global_preferences_registry.manager()[
            "general__organizationname"
        ],
        "SEARCHBAR": searchbar,
    }
