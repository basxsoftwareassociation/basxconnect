import htmlgenerator as hg
from bread import layout as layout
from bread.utils.urls import reverse_model
from django.http import HttpResponse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _
from haystack.query import SearchQuerySet
from haystack.utils.highlighting import Highlighter

from ... import models

R = layout.grid.Row
C = layout.grid.Col
F = layout.form.FormField


# Search view
# simple person search view, for use with ajax calls
def searchperson(request):
    query = request.GET.get("q")
    highlight = CustomHighlighter(query)

    if not query or len(query) < 3:
        return HttpResponse("")

    objects = (
        SearchQuerySet()
        .models(models.Person)
        .autocomplete(name_auto=query)
        .filter_or(personnumber=query)
    )

    onclick = hg.BaseElement(
        "document.location = '",
        hg.F(
            lambda c, e: reverse_model(
                c["object"].object,
                "edit",
                kwargs={"pk": c["object"].object.pk},
            )
        ),
        "'",
    )

    ret = _display_results(
        objects,
        highlight,
        onclick,
    )
    return HttpResponse(
        hg.DIV(
            ret,
            _class="raised",
            style="margin-bottom: 1rem; padding: 16px 0 48px 48px; background-color: #fff",
        ).render({})
    )


# Search view
# simple person search view, for use with ajax calls
def searchperson_and_insert(request):
    query = request.GET.get("q")
    highlight = CustomHighlighter(query)

    if not query or len(query) < 3:
        return HttpResponse("")

    objects = (
        SearchQuerySet()
        .models(models.Person)
        .autocomplete(name_auto=query)
        .filter_or(personnumber=query)
    )

    # TODO
    onclick = hg.BaseElement(
        ""
        # "set_value(",
        # hg.F(
        #     lambda c, e: c["object"].object.pk,
        # ),
        # ",",
        # ")",
    )
    ret = _display_results(objects, highlight, onclick)
    return HttpResponse(
        hg.DIV(
            ret,
            _class="raised",
            style="margin-bottom: 1rem; padding: 16px 0 48px 48px; background-color: #fff",
        ).render({})
    )


def _display_results(objects, highlight, onclick):
    if objects.count() == 0:
        return _("No results")

    first_results = [
        o.object
        for o in objects.query.get_results()
        if getattr(o, "object", None) and not o.object.deleted
    ][:25]

    def _display_as_list_item(person):
        return hg.LI(
            hg.SPAN(
                mark_safe(person.personnumber),
                style="width: 48px; display: inline-block",
            ),
            " ",
            mark_safe(highlight.highlight(person.search_index_snippet())),
            style="cursor: pointer; padding: 8px 0;",
            onclick=onclick,
            onmouseenter="this.style.backgroundColor = 'lightgray'",
            onmouseleave="this.style.backgroundColor = 'initial'",
        )

    result_list = list(map(_display_as_list_item, first_results))

    return hg.UL(
        hg.LI(_("%s items found") % len(objects), style="margin-bottom: 20px"),
        *result_list
    )


class CustomHighlighter(Highlighter):
    def find_window(self, highlight_locations):
        return (0, self.max_length)
