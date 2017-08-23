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

# Filter for looking up a dict value in templates
#
# Usage: {{ thing|lookup:some_variable }}
@register.filter(name='lookup')
def lookup(obj, key):
    return obj[key]

# Removes the given prefix from text or just returns the text as-is
def _remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

# Converts string to lowercase, strips "The", "A", and "An" from the string if
# they're at the beginning, and removes leading / trailing spaces
def _title_sort_key(s):
    s = s.lower().strip()
    s = _remove_prefix(s, "the")
    s = _remove_prefix(s, "a")
    s = _remove_prefix(s, "an")
    return s

def titles_by_location(request):
    page_title = "Titles By Location"

    titles = models.Title.objects.filter(has_issues=True)
    locations = {"Unknown": []}
    for title in titles:
        places = title.places.all()
        if len(places) == 0:
            locations["Unknown"].append(title)
            continue

        for place in places:
            loc = place.get_city_county
            if loc not in locations:
                locations[loc] = []
            locations[loc].append(title)

    if len(locations["Unknown"]) == 0:
        del locations["Unknown"]

    for location in locations:
        locations[location] = sorted(locations[location], key = lambda title: _title_sort_key(title.display_name))

    locs = sorted(locations, key=str.lower)
    return render(request, "or-locations.html", locals())

def _round_to_2(x):
    return round(x, -int(floor(log10(abs(x))-1)))

def _approx(x):
    rounded = int(_round_to_2(x))
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
