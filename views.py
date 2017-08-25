from math import log10, floor

from django.core.cache import cache
from django.shortcuts import render
from django import template
from django.contrib import humanize
from django.http import Http404, HttpResponse
from django.template.defaulttags import register
from django.db.models import Min, Max

from core import models

from onisite.plugins.featured_content import helpers as featured_content_helpers

def _round_to_100k(x):
    return round(x, -5)

def _approx(x):
    rounded = int(_round_to_100k(x))
    if rounded > x:
        return "almost", rounded
    if rounded < x:
        return "over", rounded

    return "", rounded

def _fulltext_range():
    fulltext_range = cache.get('fulltext_range')
    if not fulltext_range:
        # get the maximum and minimum years that we have content for
        issue_dates = models.Issue.objects.all().aggregate(min_date=Min('date_issued'),
        max_date=Max('date_issued'))

        min_year = issue_dates['min_date'].year
        max_year = issue_dates['max_date'].year

        fulltext_range = (min_year, max_year)
        cache.set('fulltext_range', fulltext_range)

    return fulltext_range

# Calls the featured page plugin handler to get in order to inject some useful
# dynamic values
def home(request):
    """Grab featured content from the plugin, then set up some of the
    high-level data like approximate page count"""
    pages, this_day_title = featured_content_helpers.get_pages()
    page_count = models.Page.objects.count()
    approx_page_adjective, approx_pages = _approx(page_count)
    earliest_year, latest_year = _fulltext_range()

    return render(request, 'featured.html', locals())
