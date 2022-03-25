from bread import layout
from bread.utils import Link, ModelHref, pretty_modelname
from bread.views import BrowseView
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Term, Vocabulary


class TermsBrowseView(BrowseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
                    label=_("Add %s") % pretty_modelname(Term),
                ),
                icon=layout.icon.Icon("add", size=20),
            )
        return super().get(*args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        vocabulary_slug = self.request.GET.get("vocabulary_slug")
        if vocabulary_slug:
            qs = qs.filter(vocabulary__slug=vocabulary_slug)
        return qs
