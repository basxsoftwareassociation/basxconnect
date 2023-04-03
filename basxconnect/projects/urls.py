from basxbread import menu, utils
from django.utils.translation import gettext_lazy as _

from . import models

projectsGroup = menu.Group(_("Projects"))

urlpatterns = [
    *utils.default_model_paths(models.Project),
]

projectGroup = menu.Group(_("Projects"))
menu.registeritem(
    menu.Item(
        utils.Link(
            utils.ModelHref(models.Project, "browse"),
            models.Project._meta.verbose_name,
        ),
        projectGroup,
    )
)
