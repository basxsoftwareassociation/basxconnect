from basxbread import layout
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts.editperson.common import utils

R = layout.grid.Row


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
                    layout.history_table.diff_table(
                        lambda c: type(c["object"]), historyentries
                    ).with_toolbar(_("Changes"))
                )
            ),
        ),
    )
