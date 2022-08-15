import htmlgenerator as hg
from basxbread import layout
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import utils

R = layout.grid.Row
C = layout.grid.Col


def documenttemplates_tab():
    from basxbread.contrib.document_templates.models import DocumentTemplate

    from basxconnect.core import models

    templates = DocumentTemplate.objects.filter(
        model=ContentType.objects.get_for_model(models.NaturalPerson)
    )
    prefixes = {}
    for template in templates:
        prefix = hg.mark_safe("<wbr/>")
        if "-" in template.name:
            prefix = template.name.split("-", 1)[0].strip()
        if prefix not in prefixes:
            prefixes[prefix] = []
        prefixes[prefix].append(template)

    return layout.tabs.Tab(
        _("Series letters"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    hg.DIV(
                        hg.Iterator(
                            prefixes.items(),
                            "group",
                            hg.DIV(
                                hg.H3(hg.C("group.0")),
                                hg.UL(
                                    hg.Iterator(
                                        hg.C("group.1"),
                                        "template",
                                        hg.LI(
                                            layout.components.button.Button(
                                                icon="download",
                                                buttontype="tertiary",
                                            ).as_href(
                                                href=hg.F(
                                                    lambda c: c[
                                                        "template"
                                                    ].generate_document_url(c["object"])
                                                )
                                            ),
                                            hg.DIV(
                                                hg.C("template"),
                                                style="align-self: center; margin-left: 1rem",
                                            ),
                                            style="display: flex; margin-bottom: 1rem",
                                        ),
                                    )
                                ),
                            ),
                        ),
                        style="display: grid; grid-template-columns: 1fr 1fr",
                    )
                )
            )
        ),
    )
