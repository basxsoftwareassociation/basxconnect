import htmlgenerator as hg
from bread import layout
from bread.layout.components.icon import Icon
from bread.views import EditView


class NaturalPersonEditMailingsView(EditView):
    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.naturalpersoneditmailingsview"

    @staticmethod
    def heading():
        return "Mailings"

    @staticmethod
    def modal_fields():
        return [
            "preferred_language",
            "type",
            "salutation_letter",
            "gender",
            "form_of_address",
        ]

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.modal_fields()]
        return hg.DIV(*form_fields)


class LegalPersonEditMailingsView(EditView):
    @staticmethod
    def path():
        return "basxconnect.core.views.person.person_modals_views.legalpersoneditmailingsview"

    @staticmethod
    def heading():
        return "Mailings"

    @staticmethod
    def modal_fields():
        return [
            "preferred_language",
            "type",
            "salutation_letter",
        ]

    @staticmethod
    def icon():
        return Icon("settings--adjust")

    def get_layout(self):
        form_fields = [layout.form.FormField(field) for field in self.modal_fields()]
        return hg.DIV(*form_fields)
