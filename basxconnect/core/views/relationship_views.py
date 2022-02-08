import htmlgenerator as hg
from bread import layout
from bread.views import AddView, EditView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models
from basxconnect.core.views.person import search_person_view


def search_select_person(person: str):
    return layout.forms.FormField(
        person,
        widgetclass=layout.search_select.SearchSelect,
        backend=layout.search.SearchBackendConfig(
            reverse_lazy(
                "basxconnect.core.views.person.search_person_view.searchperson"
            ),
            result_selector=f".{search_person_view.ITEM_CLASS}",
            result_label_selector=f".{search_person_view.ITEM_LABEL_CLASS}",
            result_value_selector=f".{search_person_view.ITEM_VALUE_CLASS}",
        ),
    )


formfields = [
    layout.forms.FormField("type"),
    search_select_person("person_a"),
    search_select_person("person_b"),
    layout.forms.FormField("start_date"),
    layout.forms.FormField("end_date"),
]


class EditRelationshipView(EditView):
    model = models.Relationship

    def get_layout(self):
        return layout.grid.Grid(
            hg.H3(_("Edit Relationship")),
            layout.grid.Row(
                layout.grid.Col(
                    layout.forms.Form(
                        hg.C("form"), hg.DIV(*formfields), layout.forms.helpers.Submit()
                    ),
                    width=4,
                )
            ),
            gutter=False,
        )


class AddRelationshipView(AddView):
    model = models.Relationship

    def get_layout(self):
        if self.ajax_urlparameter in self.request.GET:
            return layout.forms.Form(hg.C("form"), hg.BaseElement(*formfields))
        else:
            return layout.grid.Grid(
                hg.H3(_("Add Relationship")),
                layout.grid.Row(
                    layout.grid.Col(
                        layout.forms.Form(
                            hg.C("form"),
                            hg.DIV(*formfields),
                        ),
                        width=4,
                    )
                ),
                gutter=False,
            )
