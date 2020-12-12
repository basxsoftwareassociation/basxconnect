from bread import layout as lyt
from django.utils.translation import gettext_lazy as _

person_edit_layout = lyt.DIV(
    lyt.DIV(
        lyt.grid.Grid(
            lyt.grid.Row(
                lyt.grid.Col(
                    lyt.grid.Row(
                        lyt.FIELDSET(
                            lyt.LEGEND(_("Base data")),
                            lyt.grid.Grid(
                                lyt.grid.Row(
                                    lyt.grid.Col(lyt.form.FormField("first_name")),
                                    lyt.grid.Col(lyt.form.FormField("last_name")),
                                ),
                                lyt.grid.Row(lyt.grid.Col(lyt.form.FormField("name"))),
                            ),
                        )
                    ),
                    lyt.grid.Row(
                        lyt.FIELDSET(
                            _("Addresses"),
                            lyt.grid.Grid(
                                # Home Address
                                lyt.form.FormSetField(
                                    "core_postal_list",
                                    lyt.grid.Row(lyt.grid.Col(_("Home"))),
                                    lyt.grid.Row(
                                        lyt.grid.Col(lyt.form.FormField("address"))
                                    ),
                                    lyt.grid.Row(
                                        lyt.grid.Col(
                                            lyt.form.FormField("postcode"),
                                        ),
                                        lyt.grid.Col(lyt.form.FormField("city")),
                                    ),
                                    lyt.grid.Row(
                                        lyt.grid.Col(lyt.form.FormField("country"))
                                    ),
                                    max_num=1,
                                    extra=1,
                                ),
                                # PO Box
                                lyt.form.FormSetField(
                                    "core_pobox_list",
                                    lyt.grid.Row(lyt.grid.Col(_("Post office box"))),
                                    lyt.grid.Row(
                                        lyt.grid.Col(lyt.form.FormField("pobox_name"))
                                    ),
                                    lyt.grid.Row(
                                        lyt.grid.Col(lyt.form.FormField("postcode")),
                                        lyt.grid.Col(lyt.form.FormField("city")),
                                        lyt.grid.Col(lyt.form.FormField("country")),
                                    ),
                                    max_num=1,
                                    extra=1,
                                )
                                # TODO Button "more addresses"
                                # TODO Mailing-Sperre
                                # TODO Adressherkunft
                            ),
                        )
                    ),
                ),
                lyt.grid.Col(
                    lyt.grid.Row(
                        lyt.FIELDSET(
                            _("Personal data"),
                            lyt.grid.Grid(
                                lyt.grid.Row(
                                    lyt.grid.Col(lyt.form.FormField("salutation")),
                                    lyt.grid.Col(lyt.form.FormField("title")),
                                    lyt.grid.Col(
                                        lyt.form.FormField("preferred_language")
                                    ),
                                ),
                                # TODO Anrede formal, Briefanrede
                                lyt.grid.Row(
                                    lyt.grid.Col(lyt.form.FormField("date_of_birth")),
                                    lyt.grid.Col(
                                        lyt.form.FormField("salutation_letter")
                                    ),
                                ),
                            ),
                        )
                    ),
                    # TODO Verknüpfung
                    # TODO Kommunikationskanäle
                ),
            ),
            lyt.grid.Row(
                lyt.grid.Col(
                    lyt.grid.Row(
                        lyt.FIELDSET(
                            _("Categories"),
                            lyt.grid.Grid(
                                # TODO Suche
                                # TODO Kategorien Labels
                            ),
                        ),
                    )
                ),
                lyt.grid.Col(
                    # TODO Bemerkungen
                ),
            ),
        ),
    )
)
