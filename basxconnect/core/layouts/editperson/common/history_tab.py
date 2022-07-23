from itertools import chain

from django.conf import settings
from django.core.exceptions import FieldDoesNotExist
from django.db.models.fields.related import RelatedField

try:
    from itertools import pairwise
except ImportError:
    # python<3.10 compatability
    from itertools import tee

    def pairwise(iterable):
        a, b = tee(iterable)
        next(b, None)
        return zip(a, b)


import htmlgenerator as hg
from basxbread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import utils

R = layout.grid.Row
C = layout.grid.Col


def history_tab():

    """
    new_record, old_record = p.history.all()
    delta = new_record.diff_against(old_record)
    for change in delta.changes:
        print("{} changed from {} to {}".format(change.field, change.old, change.new))
    """

    def changes(c):
        if c["row"][1] is not None:
            return c["row"][0].diff_against(c["row"][1]).changes
        return ()

    def fieldname(c):
        try:
            return c["object"]._meta.get_field(c["change"].field).verbose_name
        except FieldDoesNotExist:
            return c["change"].field.replace("_", " ").capitalize()

    def newfieldvalue(c):
        try:
            field = c["object"]._meta.get_field(c["change"].field)
            if isinstance(field, RelatedField):
                return field.related_model.objects.get(id=int(c["change"].new))
        except FieldDoesNotExist:
            pass
        return c["change"].new

    def oldfieldvalue(c):
        try:
            field = c["object"]._meta.get_field(c["change"].field)
            if isinstance(field, RelatedField):
                return field.related_model.objects.get(id=int(c["change"].old))
        except FieldDoesNotExist:
            pass
        return c["change"].old

    return layout.tabs.Tab(
        _("History"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    layout.components.datatable.DataTable(
                        row_iterator=hg.F(
                            lambda c: pairwise(chain(c["object"].history.all(), [None]))
                        ),
                        columns=[
                            layout.components.datatable.DataTableColumn(
                                _("Date"),
                                layout.localize(
                                    layout.localtime(hg.C("row")[0].history_date).date()
                                ),
                            ),
                            layout.components.datatable.DataTableColumn(
                                _("Time"),
                                layout.localize(
                                    layout.localtime(hg.C("row")[0].history_date).time()
                                ),
                            ),
                            layout.components.datatable.DataTableColumn(
                                _("User"),
                                hg.C("row")[0].history_user,
                            ),
                            layout.components.datatable.DataTableColumn(
                                _("Changes"),
                                hg.UL(
                                    hg.Iterator(
                                        hg.F(changes),
                                        "change",
                                        hg.LI(
                                            hg.SPAN(
                                                hg.F(fieldname),
                                                style="font-weight: 600",
                                            ),
                                            ": ",
                                            hg.SPAN(
                                                hg.If(
                                                    hg.C("change").old,
                                                    hg.F(oldfieldvalue),
                                                    settings.HTML_NONE,
                                                ),
                                                style="text-decoration: line-through;",
                                            ),
                                            " -> ",
                                            hg.SPAN(
                                                hg.If(
                                                    hg.C("change").new,
                                                    hg.F(newfieldvalue),
                                                    settings.HTML_NONE,
                                                )
                                            ),
                                        ),
                                    ),
                                ),
                            ),
                        ],
                    ).with_toolbar(_("Changes"))
                )
            ),
        ),
    )
