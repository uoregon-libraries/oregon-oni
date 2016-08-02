from django.shortcuts import render_to_response
from django.template import RequestContext

from core.models import Place

def history(request):
    page_title = "Historic Essays"
    return render_to_response('essay_index.html', dictionary=locals(), context_instance=RequestContext(request))

def essay(request, essay):
    page_title = "Historic Essays"
    return render_to_response('essays/%s.html' % essay, dictionary=locals(), context_instance=RequestContext(request))
