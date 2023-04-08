import datetime

import htmlgenerator as hg
from basxbread import layout, menu, utils, views
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from . import models
from .views import send_invoice, send_receipt


def invoice_download(context):
    from dynamic_preferences.registries import global_preferences_registry

    invoice_template = global_preferences_registry.manager()[
        "invoicing__default_invoice_template"
    ]
    return invoice_template.generate_document_url(context["row"], pdf=True)


def receipt_download(context):
    from dynamic_preferences.registries import global_preferences_registry

    receipt_template = global_preferences_registry.manager()[
        "invoicing__default_receipt_template"
    ]
    return receipt_template.generate_document_url(context["row"], pdf=True)


invoice_form = layout.grid.Grid(
    layout.grid.Row(
        layout.grid.Col(
            layout.tile.Tile(
                hg.If(
                    hg.C("object"),
                    hg.H3(
                        hg.C("object.total_amount"),
                        hg.DIV(
                            hg.BaseElement(
                                layout.ObjectFieldValue("net_amount"),
                                " ",
                                _("Net"),
                            ),
                            style="font-size: 0.75rem",
                        ),
                        hg.If(
                            hg.C("object.vat"),
                            hg.DIV(
                                hg.BaseElement(
                                    "+ ",
                                    layout.ObjectFieldValue("vat_amount"),
                                    " ",
                                    layout.ObjectFieldLabel("vat"),
                                ),
                                style="font-size: 0.75rem",
                            ),
                        ),
                        hg.If(
                            hg.C("object.wht"),
                            hg.DIV(
                                hg.BaseElement(
                                    "- ",
                                    layout.ObjectFieldValue("wht_amount"),
                                    " ",
                                    layout.ObjectFieldLabel("wht"),
                                ),
                                style="font-size: 0.75rem",
                            ),
                        ),
                    ),
                    hg.H3(_("New"), " ", models.Invoice._meta.verbose_name),
                ),
                hg.DIV(
                    layout.forms.FormField("number", no_wrapper=True),
                    layout.forms.FormField("client", no_wrapper=True),
                    layout.forms.FormField("paymenttype", no_wrapper=True),
                    style="display: flex; justify-content: space-between",
                ),
                hg.DIV(
                    layout.forms.FormField(
                        "note",
                        style="margin-top: 1rem; width: 100%",
                        inputelement_attrs={"rows": 4},
                    ),
                ),
                light=True,
            ),
            layout.forms.Formset.as_inline_datatable(
                "items", ["project", "description", "amount"]
            ),
            width=10,
        ),
        layout.grid.Col(
            layout.tile.Tile(
                layout.grid.Row(
                    layout.grid.Col(
                        hg.DIV(_("Dates"), style="margin-bottom: 1rem"),
                        layout.forms.FormField("created"),
                        layout.forms.FormField("invoice_sent"),
                        layout.forms.FormField("payed"),
                        layout.forms.FormField("receipt_sent"),
                        layout.forms.FormField("cancelled", style="margin-top: 3rem"),
                    ),
                    layout.grid.Col(
                        hg.DIV(
                            _("Currency and taxes"),
                            style="margin-bottom: 1rem",
                        ),
                        layout.forms.FormField("currency"),
                        layout.forms.FormField("amounts_include_vat"),
                        layout.forms.FormField("vat"),
                        layout.forms.FormField("wht"),
                    ),
                ),
                light=True,
            ),
            width=6,
        ),
    ),
    style="margin-bottom: 4rem",
)

urlpatterns = [
    *utils.default_model_paths(
        models.Invoice,
        browseview=views.BrowseView._with(
            queryset=models.Invoice.objects.get_active(),
            columns=[
                "created",
                "number",
                "client",
                "total_amount",
                layout.datatable.DataTableColumn(
                    layout.ObjectFieldLabel("invoice_sent", hg.C("object_list").model),
                    hg.If(
                        hg.C("row").invoice_sent,
                        hg.C("row").invoice_sent,
                        layout.modal.Modal.with_ajax_content(
                            hg.format(
                                _("Send invoice {} to {}"),
                                hg.C("row").number,
                                hg.C("row").client,
                            ),
                            utils.ModelHref(
                                hg.C("row"), "sendinvoice", query={"asajax": True}
                            ),
                            submitlabel=_("Send invoice"),
                            size="md",
                            id=hg.format("send-invoice-{}", hg.C("row").id),
                        ).with_trigger(
                            layout.button.Button.from_link(
                                utils.Link(
                                    href="",
                                    label=_("Send invoice"),
                                    iconname="mail--all",
                                    permissions=[
                                        hg.F(
                                            lambda c: utils.permissionname(
                                                c["row"], "change"
                                            )
                                        )
                                    ],
                                ),
                                notext=True,
                                small=True,
                                buttontype="ghost",
                            )
                        ),
                    ),
                ),
                layout.datatable.DataTableColumn(
                    layout.ObjectFieldLabel("payed", hg.C("object_list").model),
                    hg.If(
                        hg.C("row").payed,
                        hg.C("row").payed,
                        layout.modal.Modal.with_ajax_content(
                            hg.C("row"),
                            utils.ModelHref(
                                hg.C("row"), "markpayed", query={"asajax": True}
                            ),
                            submitlabel=_("Mark payed"),
                            id=hg.format("mark-payed-{}", hg.C("row").id),
                        ).with_trigger(
                            layout.button.Button.from_link(
                                utils.Link(
                                    href="",
                                    label=_("Mark payed"),
                                    iconname="checkmark",
                                    permissions=[
                                        hg.F(
                                            lambda c: utils.permissionname(
                                                c["row"], "change"
                                            )
                                        )
                                    ],
                                ),
                                notext=True,
                                small=True,
                                buttontype="ghost",
                            )
                        ),
                    ),
                ),
                layout.datatable.DataTableColumn(
                    layout.ObjectFieldLabel("receipt_sent", hg.C("object_list").model),
                    hg.If(
                        hg.C("row").receipt_sent,
                        hg.C("row").receipt_sent,
                        hg.If(
                            hg.C("row").payed,
                            layout.modal.Modal.with_ajax_content(
                                hg.format(
                                    _("Send receipt for invoice {} to {}"),
                                    hg.C("row").number,
                                    hg.C("row").client,
                                ),
                                utils.ModelHref(
                                    hg.C("row"), "sendreceipt", query={"asajax": True}
                                ),
                                submitlabel=_("Send receipt"),
                                size="md",
                                id=hg.format("send-receipt-{}", hg.C("row").id),
                            ).with_trigger(
                                layout.button.Button.from_link(
                                    utils.Link(
                                        href="",
                                        label=_("Send receipt"),
                                        iconname="mail--all",
                                        permissions=[
                                            hg.F(
                                                lambda c: utils.permissionname(
                                                    c["row"], "change"
                                                )
                                            )
                                        ],
                                    ),
                                    notext=True,
                                    small=True,
                                    buttontype="ghost",
                                )
                            ),
                        ),
                    ),
                ),
                layout.datatable.DataTableColumn(
                    _("Invoice"),
                    hg.If(
                        hg.F(
                            lambda c: models.pref("default_invoice_template")
                            is not None
                        ),
                        layout.button.Button(
                            notext=True, icon="download", buttontype="ghost", small=True
                        ).as_href(hg.F(invoice_download)),
                        hg.SPAN(
                            _(
                                "Select a default invoice template first in the global preferences"
                            ),
                            style="color: #FF5500",
                        ),
                    ),
                ),
                layout.datatable.DataTableColumn(
                    _("Receipt"),
                    hg.If(
                        hg.F(
                            lambda c: models.pref("default_receipt_template")
                            is not None
                        ),
                        hg.If(
                            hg.C("row.payed"),
                            layout.button.Button(
                                notext=True,
                                icon="download",
                                buttontype="ghost",
                                small=True,
                            ).as_href(hg.F(receipt_download)),
                        ),
                        hg.SPAN(
                            _(
                                "Select a default receipt template first in the global preferences"
                            ),
                            style="color: #FF5500",
                        ),
                    ),
                ),
            ],
            rowactions=[
                views.BrowseView.editlink(),
                layout.modal.Modal.with_ajax_content(
                    hg.C("row"),
                    utils.ModelHref(hg.C("row"), "cancel", query={"asajax": True}),
                    submitlabel=_("Cancel"),
                    id=hg.format("cancel-{}", hg.C("row").id),
                ).with_trigger(
                    layout.button.Button.from_link(
                        utils.Link(
                            href="",
                            label=_("Cancel"),
                            iconname="trash-can",
                            permissions=[
                                hg.F(lambda c: utils.permissionname(c["row"], "delete"))
                            ],
                        ),
                        notext=True,
                        small=True,
                        buttontype="ghost",
                    )
                ),
            ],
        ),
        editview=views.EditView._with(
            fields=[invoice_form],
            get_success_url=lambda s: s.request.get_full_path(),
        ),
        addview=views.AddView._with(
            fields=[invoice_form],
            get_success_url=lambda s: utils.reverse_model(
                models.Invoice, "edit", kwargs={"pk": s.object.pk}
            ),
        ),
        markpayed=views.EditView._with(
            fields=["payed"], get_initial=lambda s: {"payed": now().date}
        ),
        cancel=views.EditView._with(
            fields=["cancelled"],
            get_initial=lambda s: {"cancelled": datetime.date.today()},
        ),
        sendinvoice=send_invoice,
        sendreceipt=send_receipt,
    ),
    *utils.default_model_paths(models.PaymentType),
]

invoicingGroup = menu.Group(_("Invoicing"))

menu.registeritem(
    menu.Item(
        utils.Link(
            utils.ModelHref(models.Invoice, "browse"),
            models.Invoice._meta.verbose_name_plural,
        ),
        invoicingGroup,
    )
)
menu.registeritem(
    menu.Item(
        utils.Link(
            utils.ModelHref(models.PaymentType, "browse"),
            models.PaymentType._meta.verbose_name_plural,
        ),
        invoicingGroup,
    )
)
