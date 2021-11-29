import htmlgenerator as hg
from bread import layout as layout
from bread.utils import reverse_model
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from haystack.query import SearchQuerySet
from haystack.utils import Highlighter
from htmlgenerator import mark_safe

from ... import models, settings

R = layout.grid.Row
C = layout.grid.Col

ITEM_CLASS = "search_result_item"
ITEM_LABEL_CLASS = "search_result_label"
ITEM_VALUE_CLASS = "search_result_value"

searchbar = layout.search.Search(
    placeholder=_("Search person"),
    backend=layout.search.SearchBackendConfig(
        reverse_lazy("basxconnect.core.views.person.search_person_view.searchperson"),
    ),
    width="140%",
)


def searchperson(request):
    query = request.GET.get("q")

    highlight = CustomHighlighter(query)
    if not query or len(query) < settings.MIN_CHARACTERS_DYNAMIC_SEARCH:
        return HttpResponse("")

    query_set = (
        SearchQuerySet()
        .models(models.Person)
        .autocomplete(name_auto=query)
        .filter_or(personnumber=query)
    )

    def onclick(person):
        link = reverse_model(
            person,
            "edit",
            kwargs={"pk": person.pk},
        )
        return f"document.location = '{link}'"

    ret = _display_results(query_set, highlight, onclick)
    return HttpResponse(
        hg.DIV(
            ret,
            _class="raised",
            style="margin-bottom: 1rem; padding: 16px 0 48px 48px; background-color: #fff",
        ).render({})
    )


def _display_results(query_set, highlight, onclick):
    if query_set.count() == 0:
        return _("No results")

    def _display_as_list_item(person):
        if person is None:
            # this happens if we have entries in the search-backend which have been deleted
            return hg.BaseElement()
        return hg.LI(
            hg.SPAN(
                mark_safe(highlight.highlight(person.personnumber)),
                style="width: 48px; display: inline-block",
                _class=ITEM_VALUE_CLASS,
            ),
            hg.SPAN(
                person.name,
                _class=ITEM_LABEL_CLASS,
                style="dispay:none;",
            ),
            " ",
            mark_safe(highlight.highlight(person.search_index_snippet())),
            style="cursor: pointer; padding: 8px 0;",
            onclick=onclick(person),
            onmouseenter="this.style.backgroundColor = 'lightgray'",
            onmouseleave="this.style.backgroundColor = 'initial'",
            _class=ITEM_CLASS,
        )

    result_list = [
        _display_as_list_item(search_result.object)
        for search_result in query_set[:25]
        if search_result and search_result.object
    ]

    return hg.UL(
        hg.LI(_("%s items found") % len(query_set), style="margin-bottom: 20px"),
        *result_list,
    )


class CustomHighlighter(Highlighter):
    def find_window(self, highlight_locations):
        return (0, self.max_length)
