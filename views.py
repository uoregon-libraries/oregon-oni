from math import log10, floor
import datetime
import random

from django.core.cache import cache
from django.shortcuts import render
from django import template
from django.contrib import humanize
from django.http import Http404, HttpResponse
from django.template.defaulttags import register
from django.db.models import Min, Max

from core import models

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
        issue_dates = models.Issue.objects.all().aggregate(
            min_date=Min('date_issued'),
            max_date=Max('date_issued')
        )

        if issue_dates['min_date'] is None or issue_dates['max_date'] is None:
            return (1600, 1800)

        min_year = issue_dates['min_date'].year
        max_year = issue_dates['max_date'].year

        fulltext_range = (min_year, max_year)
        cache.set('fulltext_range', fulltext_range)

    return fulltext_range

def featured_page():
    # Seed the RNG with today's date so we always feature the same page(s) for
    # an entire day
    random.seed(datetime.date.today().strftime("%Y%m%d"))

    min_year, _ = _fulltext_range()
    now = datetime.date.today()
    page = None
    title = "This day in history"

    qs = models.Page.objects
    qs = qs.filter(jp2_filename__isnull = False)
    qs = qs.filter(sequence = 1)

    tries = 0
    while page is None and tries < 10:
        tries += 1
        year = random.randrange(min_year, 1951)
        subquery = qs.filter(issue__date_issued = datetime.datetime(year, now.month, now.day))
        num = subquery.count()
        if num > 0:
            page = subquery[random.randrange(num)]

    if page is None:
        qs = qs.order_by('?')
        if qs.count() > 0:
            page = qs.order_by('?')[0]
            title = "Featured Page"

    return page, title

# Calls the featured page plugin handler to get in order to inject some useful
# dynamic values
def home(request):
    """Grab featured content from the plugin, then set up some of the
    high-level data like approximate page count"""
    page, featured_page_title = featured_page()
    page_count = models.Page.objects.count()
    approx_page_adjective, approx_pages = _approx(page_count)
    earliest_year, latest_year = _fulltext_range()

    return render(request, 'home.html', locals())
