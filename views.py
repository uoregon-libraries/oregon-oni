from django.shortcuts import render
from django import template
from django.http import Http404, HttpResponse

def titles_by_location(request):
    page_title = "Titles By Location"
    return render(request, "or-locations.html", locals())
