import htmlgenerator as hg
import pkg_resources
import requests
from bread import layout
from bread.layout.components.datatable import DataTable, DataTableColumn
from bread.utils.urls import aslayout
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _

from basxconnect.core import models

R = layout.grid.Row
C = layout.grid.Col

TR = layout.datatable.DataTable.row
TD = layout.datatable.DataTableColumn

# The package names we're currently interested in.
PYPI_API = "https://pypi.python.org/pypi/{}/json"
PACKAGE_NAMES = ("basx-bread", "basxconnect", "htmlgenerator")


@user_passes_test(lambda user: user.is_superuser)
@aslayout
def maintenancesettings(request):
    ret = layout.grid.Grid(R(C(hg.H3(_("Maintenance")))), gutter=False)

    package_current = []
    package_latest = []

    for package_name in PACKAGE_NAMES:
        current_version = pkg_resources.get_distribution(package_name).version
        newer_version = "unable to load"

        # load the latest package info from the PyPI API
        pkg_info_req = requests.get(PYPI_API.format(package_name))
        if pkg_info_req.status_code == requests.codes.ok:
            newer_version = pkg_info_req.json()["info"]["version"]

        package_current.append(current_version)
        package_latest.append(newer_version)

    ret.append(
        R(
            C(
                DataTable(
                    columns=[
                        DataTableColumn(
                            header="Package",
                            cell=hg.DIV(hg.C("row.package_name")),
                        ),
                        DataTableColumn(
                            header="Current",
                            cell=hg.DIV(hg.C("row.package_current")),
                        ),
                        DataTableColumn(
                            header="Latest",
                            cell=(hg.DIV(hg.C("row.package_latest"))),
                        ),
                    ],
                    row_iterator=[
                        {
                            "package_name": pkg_name,
                            "package_current": pkg_current,
                            "package_latest": pkg_latest,
                        }
                        for pkg_name, pkg_current, pkg_latest in zip(
                            PACKAGE_NAMES, package_current, package_latest
                        )
                    ],
                )
            )
        )
    )

    return ret
