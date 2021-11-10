import os

import htmlgenerator as hg
import pkg_resources
import requests
from bread import layout
from bread.layout.components.button import Button
from bread.layout.components.datatable import DataTable, DataTableColumn
from django.conf import settings
from django.db import connection
from django.utils.translation import gettext_lazy as _

PYPI_API = "https://pypi.python.org/pypi/{}/json"
PACKAGE_NAMES = ("basx-bread", "basxconnect", "htmlgenerator")

R = layout.grid.Row
C = layout.grid.Col


def maintainance_package_layout(request):
    package_current = []
    package_latest = []
    for package_name in PACKAGE_NAMES:
        current_version = pkg_resources.get_distribution(package_name).version
        newer_version = _("unable to load")

        # load the latest package info from the PyPI API
        pkg_info_req = requests.get(PYPI_API.format(package_name))
        if pkg_info_req.status_code == requests.codes.ok:
            newer_version = pkg_info_req.json()["info"]["version"]

        package_current.append(current_version)
        package_latest.append(newer_version)

    return DataTable(
        columns=[
            DataTableColumn(
                header=_("Package"),
                cell=hg.DIV(hg.C("row.package_name")),
            ),
            DataTableColumn(
                header=_("Current"),
                cell=hg.DIV(hg.C("row.package_current")),
            ),
            DataTableColumn(
                header=_("Latest"),
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


def maintenance_database_optimization(request):
    database_path = settings.DATABASES["default"]["NAME"]

    current_db_size = os.stat(database_path).st_size / 1_000
    previous_size = None

    optimize_btn = hg.FORM(
        layout.form.CsrfToken(),
        Button(_("Optimize"), type="submit"),
        hg.INPUT(type="hidden", name="previous-size", value=current_db_size),
        method="POST",
    )

    if request.method == "POST":
        post_body = {key: val[0] for key, val in dict(request.POST).items()}
        # to avoid unexpected POST requests, check if "previous-size" is included.
        if "previous-size" in post_body:
            connection.cursor().execute("VACUUM;")
            # get the previous size
            previous_size = float(post_body["previous-size"])
            current_db_size = os.stat(database_path).st_size / 1_000

    return hg.BaseElement(
        hg.If(
            previous_size is not None,
            hg.H5(f"Previous Size: {previous_size : .2f} kB"),
            hg.H5(f"Current Size: {current_db_size : .2f} kB"),
        ),
        hg.If(
            previous_size is not None,
            hg.H5(f"Minimized Size: {current_db_size : .2f} kB"),
        ),
        optimize_btn,
    )
