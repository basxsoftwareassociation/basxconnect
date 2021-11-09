# The package names we're currently interested in.
import json
import os

import htmlgenerator as hg
import pkg_resources
import requests
from bread import layout
from bread.layout.components.button import Button
from bread.layout.components.datatable import DataTable, DataTableColumn
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
    # get the database's size (in kilobytes)
    # TODO: Add a button that runs the command
    current_db_size = os.stat(os.getcwd() + "/db.sqlite3").st_size / 1000
    previous_size = 0
    debug_str = ""

    if request.method == "POST":
        cursor = connection.cursor()
        debug_str = cursor.execute("VACUUM;")
        current_db_size = os.stat(os.getcwd() + "/db.sqlite3").st_size / 1000
        previous_size = request.body.decode("utf-8")
        previous_size = previous_size[previous_size.find("previous-size") + 13 :]

    optimize_btn = hg.FORM(
        layout.form.CsrfToken(),
        Button("Optimize", type="submit"),
        hg.INPUT(type="hidden", name="previous-size", value=current_db_size),
        method="POST",
    )

    return hg.BaseElement(
        hg.If(
            request.method == "POST",
            hg.H5(f"Previous Size: {previous_size : .2f} KB"),
            hg.H5(f"Current Size: {current_db_size : .2f} KB"),
        ),
        hg.If(request.method == "POST", f"Minimized Size: {current_db_size : .2f} KB"),
        optimize_btn,
    )
