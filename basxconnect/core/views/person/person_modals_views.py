import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.views import EditView
from django.utils.translation import gettext_lazy as _


class NaturalPersonEditMailingsView(EditView):
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
        "gender",
        "form_of_address",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.naturalpersoneditmailingsview"

    @staticmethod
    def read_heading():
        return _("Settings")

    @staticmethod
    def edit_heading():
        return _("Edit mailing settings")

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)


class LegalPersonEditMailingsView(EditView):
    fields = [
        "preferred_language",
        "type",
        "salutation_letter",
    ]

    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.legalpersoneditmailingsview"

    @staticmethod
    def read_heading():
        return _("Settings")

    @staticmethod
    def edit_heading():
        return _("Edit mailing settings")

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.fields]
        return hg.DIV(*form_fields)
