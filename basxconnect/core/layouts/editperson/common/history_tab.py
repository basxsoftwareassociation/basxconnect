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


def changes(c):
    if c["row"][0] is not None and c["row"][1] is not None:
        return list(c["row"][0].diff_against(c["row"][1]).changes)
    return ()


def haschanges(a, b):
    return a is not None and b is not None and len(a.diff_against(b).changes) > 0


def fieldname(c, model):
    try:
        return model._meta.get_field(c["change"].field).verbose_name
    except FieldDoesNotExist:
        return c["change"].field.replace("_", " ").capitalize()


def newfieldvalue(c, model):
    try:
        field = model._meta.get_field(c["change"].field)
        if isinstance(field, RelatedField):
            try:
                return field.related_model.objects.get(id=int(c["change"].new))
            except field.related_model.DoesNotExist:
                return hg.SPAN(_("<Value has been deleted>"), style="color: red")
    except FieldDoesNotExist:
        pass
    return c["change"].new


def oldfieldvalue(c, model):
    try:
        field = model._meta.get_field(c["change"].field)
        if isinstance(field, RelatedField):
            ret = field.related_model.objects.filter(id=int(c["change"].old)).first()
            return ret or hg.SPAN(_("<Value has been deleted>"), style="color: red")
    except FieldDoesNotExist:
        pass
    return c["change"].old


def diff_table(model, historylist, showObjectLabel=None):
    def historyentries(c):
        return (
            (i, j)
            for i, j in pairwise(chain(historylist(c), [None]))
            if haschanges(i, j)
        )

    return layout.components.datatable.DataTable(
        row_iterator=hg.F(historyentries),
        columns=[
            layout.components.datatable.DataTableColumn(
                _("Date"),
                layout.localize(layout.localtime(hg.C("row")[0].history_date).date()),
            ),
            layout.components.datatable.DataTableColumn(
                _("Time"),
                layout.localize(layout.localtime(hg.C("row")[0].history_date).time()),
            ),
            layout.components.datatable.DataTableColumn(
                _("User"),
                hg.C("row")[0].history_user,
            ),
            *(
                [
                    layout.components.datatable.DataTableColumn(
                        _("Object"),
                        hg.F(lambda c: showObjectLabel(c["row"][0].instance)),
                    )
                ]
                if showObjectLabel is not None
                else []
            ),
            layout.components.datatable.DataTableColumn(
                _("Changes"),
                hg.UL(
                    hg.Iterator(
                        hg.F(changes),
                        "change",
                        hg.LI(
                            hg.SPAN(
                                hg.F(lambda c: fieldname(c, model(c))),
                                style="font-weight: 600",
                            ),
                            ": ",
                            hg.SPAN(
                                hg.If(
                                    hg.C("change").old,
                                    hg.F(lambda c: oldfieldvalue(c, model(c))),
                                    settings.HTML_NONE,
                                ),
                                style="text-decoration: line-through;",
                            ),
                            " -> ",
                            hg.SPAN(
                                hg.If(
                                    hg.C("change").new,
                                    hg.F(lambda c: newfieldvalue(c, model(c))),
                                    settings.HTML_NONE,
                                )
                            ),
                        ),
                    ),
                ),
            ),
        ],
    )


def history_tab():
    """
    new_record, old_record = p.history.all()
    delta = new_record.diff_against(old_record)
    for change in delta.changes:
        print("{} changed from {} to {}".format(change.field, change.old, change.new))
    """

    def historyentries(c):
        return c["object"].history.all()

    return layout.tabs.Tab(
        _("History"),
        utils.grid_inside_tab(
            R(
                utils.tiling_col(
                    diff_table(
                        lambda c: type(c["object"]), historyentries
                    ).with_toolbar(_("Changes"))
                )
            ),
        ),
    )
