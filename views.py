from django.shortcuts import render
from django import template
from django.http import Http404, HttpResponse

def cities(request):
    page_title = "All Cities"
    return render(request, "or-cities.html", locals())
