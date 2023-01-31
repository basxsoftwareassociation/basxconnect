from basxbread.utils.urls import aslayout

import basxconnect.core.layouts.settings_layout as settings_layout


@aslayout
def relationshipssettings(request):
    return settings_layout.relationshipssettings(request)
