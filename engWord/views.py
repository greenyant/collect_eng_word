from django.shortcuts import render, render_to_response
from django.template import Context, RequestContext

# Create your views here.
def index(request):
    variables = RequestContext(request, { })
    return render_to_response('engWord/index.html', variables)