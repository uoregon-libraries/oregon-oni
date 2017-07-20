from django.shortcuts import render
from django import template
from django.http import Http404, HttpResponse
from django.template.defaulttags import register

from core import models

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
