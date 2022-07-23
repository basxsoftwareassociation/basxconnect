import htmlgenerator as hg
from basxbread import layout
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import utils

R = layout.grid.Row
C = layout.grid.Col


def documenttemplates_tab():
    documents = hg.F(
        lambda c: ContentType.objects.get_for_model(
            c["object"]
        ).documenttemplate_set.all()
    )
    return layout.tabs.Tab(
        _("Documents"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    hg.Iterator(
                        documents,
                        "document",
                        hg.DIV(
                            hg.A(
                                hg.C("document.name"),
                                href=hg.F(
                                    lambda c: c["document"].generate_document_url(
                                        c["object"]
                                    )
                                ),
                            )
                        ),
                    )
                )
            ),
        ),
    )
