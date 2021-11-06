import htmlgenerator as hg
from bread import layout
from bread.utils.urls import aslayout
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _

from basxconnect.core.layouts import admin_layout

R = layout.grid.Row
C = layout.grid.Col

TR = layout.datatable.DataTable.row
TD = layout.datatable.DataTableColumn


@user_passes_test(lambda user: user.is_superuser)
@aslayout
def maintenancesettings(request):
    # Add the view's header
    ret = layout.grid.Grid(R(C(hg.H3(_("Maintenance")))), gutter=False)

    # package information
    ret.append(R(C(admin_layout.maintainance_package_layout(request))))

    # Database Optimization

    return ret
