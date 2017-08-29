# This "view", along with json_api.py, gives us a minimal API to replace the
# IIIF endpoints.  The IIIF endpoints added some value, but we aren't using it
# yet, and they removed a lot of information we need for simple automated
# traversal of batch list -> batch -> issues -> titles.

import json

from django.conf import settings
from django.contrib import humanize
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404

from core import models
from core.decorator import cache_page, cors
from core.utils.utils import _page_range_short, _rdf_base, _get_tip

import json_api

def _render(j):
    return HttpResponse(json.dumps(j, indent=2), content_type='application/json')

@cors
@cache_page(settings.API_TTL_SECONDS)
def batches(request, page_number=1):
    return _render(json_api.batches(page_number))

@cors
@cache_page(settings.API_TTL_SECONDS)
def batch(request, batch_name):
    batch = get_object_or_404(models.Batch, name=batch_name)
    return _render(json_api.batch(batch))

@cors
@cache_page(settings.API_TTL_SECONDS)
def title(request, lccn):
    title = get_object_or_404(models.Title, lccn=lccn)
    return _render(json_api.title(title))

@cors
@cache_page(settings.API_TTL_SECONDS)
def issue(request, lccn, date, edition):
    title, issue, page = _get_tip(lccn, date, edition)
    return _render(json_api.issue(issue))
