from django.shortcuts import render

from bread.utils.urlgenerator import registerurl
from htmlgenerator import DIV


@registerurl
def generalsettings(request):
    return render(
        request, "bread/dynamic_layout.html", {"view": {"layout": DIV("Hello")}}
    )


@registerurl
def appearancesettings(request):
    return render(
        request, "bread/dynamic_layout.html", {"view": {"layout": DIV("Hello")}}
    )


@registerurl
def personssettings(request):
    return render(
        request, "bread/dynamic_layout.html", {"view": {"layout": DIV("Hello")}}
    )


@registerurl
def relationshipssettings(request):
    return render(
        request, "bread/dynamic_layout.html", {"view": {"layout": DIV("Hello")}}
    )


@registerurl
def apikeyssettings(request):
    return render(
        request, "bread/dynamic_layout.html", {"view": {"layout": DIV("Hello")}}
    )
