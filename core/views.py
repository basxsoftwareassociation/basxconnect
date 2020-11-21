from bread.utils.urlgenerator import registerurl
from bread.utils.views import render_layout_to_response
from htmlgenerator import DIV


@registerurl
def generalsettings(request):
    return render_layout_to_response(request, DIV("Hello"))


@registerurl
def appearancesettings(request):
    return render_layout_to_response(request, DIV("Hello"))


@registerurl
def personssettings(request):
    return render_layout_to_response(request, DIV("Hello"))


@registerurl
def relationshipssettings(request):
    return render_layout_to_response(request, DIV("Hello"))


@registerurl
def apikeyssettings(request):
    return render_layout_to_response(request, DIV("Hello"))
