import htmlgenerator as hg
from bread import layout as layout
from bread.views import EditView, ReadView, layoutasreadonly
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from basxconnect.core.layouts.editlegalperson import editlegalperson_form
from basxconnect.core.layouts.editnaturalperson import editnaturalperson_form
from basxconnect.core.layouts.editperson import editperson_head
from basxconnect.core.layouts.editpersonassociation import editpersonassociation_form

from ... import models

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


def personform_shortcut(request, formlayout, isreadview):
    return hg.BaseElement(
        layout.grid.Grid(
            editperson_head(request, isreadview=isreadview),
            layout.form.Form(hg.C("form"), formlayout),
            gutter=False,
        )
    )


class NaturalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editnaturalperson_form(self.request),
            isreadview=False,
        )


class NaturalPersonReadView(ReadView):
    def get_layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                editnaturalperson_form(self.request),
                isreadview=True,
            )
        )


class LegalPersonEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editlegalperson_form(self.request),
            isreadview=False,
        )


class LegalPersonReadView(ReadView):
    def get_layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                editlegalperson_form(self.request),
                isreadview=True,
            )
        )


class PersonAssociationEditView(EditView):
    def get_layout(self):
        return personform_shortcut(
            self.request,
            editpersonassociation_form(self.request),
            isreadview=False,
        )


class PersonAssociationReadView(ReadView):
    def get_layout(self):
        return layoutasreadonly(
            personform_shortcut(
                self.request,
                editpersonassociation_form(self.request),
                isreadview=True,
            )
        )


@csrf_exempt
def togglepersonstatus(request, pk: int):
    if request.method == "POST":
        person = get_object_or_404(models.Person, pk=pk)
        person.active = not person.active
        person.save()
    return HttpResponse(
        _("%s is %s") % (person, _("Active") if person.active else _("Inactive"))
    )
