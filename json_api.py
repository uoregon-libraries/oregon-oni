from rfc3339 import rfc3339

from core import models
from core.utils import strftime
from django.conf import settings
from django.core.paginator import Paginator

def batches(page_number):
    batches = models.Batch.viewable_batches()
    paginator = Paginator(batches, 25)
    page = paginator.page(page_number)
    batch_data = [batch(b, include_issues=False) for b in page.object_list]
    j = {'batches': batch_data}

    if page.has_next():
        url_next = urlresolvers.reverse('openoni_batches_json_page', args=[page.next_page_number()])
        j['next'] = settings.BASE_URL + url_next

    if page.has_previous():
        url_prev = urlresolvers.reverse('openoni_batches_json_page', args=[page.previous_page_number()])
        j['previous'] = settings.BASE_URL + url_prev

    return j

def batch(batch, include_issues=True):
    b = {}
    b['name'] = batch.name
    b['ingested'] = rfc3339(batch.created)
    b['page_count'] = batch.page_count
    b['lccns'] = batch.lccns()
    b['awardee'] = {
        "name": batch.awardee.name,
        "url": settings.BASE_URL + batch.awardee.json_url
    }
    b['url'] = settings.BASE_URL + batch.json_url
    if include_issues:
        b['issues'] = []
        for issue in batch.issues.all():
            i = {
                "title": {
                    "name": issue.title.display_name,
                    "url": settings.BASE_URL + issue.title.json_url,
                },
                "date_issued": strftime(issue.date_issued, "%Y-%m-%d"),
                "url": settings.BASE_URL + issue.json_url
            }
            b['issues'].append(i)

    return b

def title(title):
    j = {
        "url": settings.BASE_URL + title.json_url,
        "lccn": title.lccn,
        "name": title.display_name,
        "place_of_publication": title.place_of_publication,
        "publisher": title.publisher,
        "start_year": title.start_year,
        "end_year": title.end_year,
        "subject": [s.heading for s in title.subjects.all()],
        "place": [p.name for p in title.places.all()],
        "issues": [{
            "url": settings.BASE_URL + i.json_url,
            "date_issued": strftime(i.date_issued, "%Y-%m-%d")
        } for i in title.issues.all()]
    }

    return j

def issue(issue):
    j = {
        'url': 'http://' + settings.BASE_URL + issue.json_url,
        'date_issued': strftime(issue.date_issued, "%Y-%m-%d"),
        'volume': issue.volume,
        'number': issue.number,
        'edition': issue.edition,
        'title': {"name": issue.title.display_name, "url": 'http://' + settings.BASE_URL + issue.title.json_url},
        'batch': {"name": issue.batch.name, "url": 'http://' + settings.BASE_URL + issue.batch.json_url},
    }

    j['pages'] = [{
        "url": settings.BASE_URL + p.json_url,
        "sequence": p.sequence
    } for p in issue.pages.all()]

    return j
