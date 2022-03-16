import htmlgenerator as hg
from bread.utils import Link, ModelHref
from bread.views import BrowseView
from django.utils.translation import gettext_lazy as _

from basxconnect.core.models import Term


class VocabularyBrowseView(BrowseView):
    rowactions = [
        BrowseView.editlink(),
        Link(
            href=ModelHref(Term, "browse", query={"vocabulary_slug": hg.C("row").slug}),
            label=_("Terms of vocabulary"),
            iconname="tree-view--alt",
        ),
    ]
