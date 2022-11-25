from basxbread import layout
from basxbread.utils import Link, ModelHref
from basxbread.views import BrowseView
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Term, Vocabulary


class TermsBrowseView(BrowseView):
    rowclickaction = BrowseView.gen_rowclickaction("edit", return_to_current=True)
    rowactions = [BrowseView.deletelink()]
    columns = ["term", "slug"]

    def get(self, *args, **kwargs):
        vocabulary = Vocabulary.objects.filter(
            slug=self.request.GET.get("vocabulary_slug")
        ).first()
        if vocabulary:
            self.primary_button = layout.button.Button.from_link(
                Link(
                    href=ModelHref(
                        Term,
                        "add",
                        query={"vocabulary": vocabulary.id},
                        return_to_current=True,
                    ),
                    label=_("Add %s") % Term._meta.verbose_name,
                ),
                icon=layout.icon.Icon("add", size=20),
            )
            self.title = Vocabulary.objects.get(
                slug=self.request.GET.get("vocabulary_slug")
            ).name
        return super().get(*args, **kwargs)

    def get_queryset(self):
        qs = Term.objects.including_disabled()
        vocabulary_slug = self.request.GET.get("vocabulary_slug")
        if vocabulary_slug:
            qs = qs.filter(vocabulary__slug=vocabulary_slug)
        return qs
