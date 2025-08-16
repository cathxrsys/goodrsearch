from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .indexing import Indexing

from django.core.paginator import Paginator
from django.core.paginator import EmptyPage



def index(request):
    context = {}
    
    return render(request, 'search/index.html', context)


def search(request):
    query = request.GET.get("query")
    
    
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1
    
    if query == None or query.strip() == '':
        return redirect('/')
    
    indexing = Indexing()
    files = indexing.get(query)
    
    p = Paginator(files, 10)
    
    
    context = {}
    
    try:
        context['files'] = p.page(page)
    except EmptyPage:
        context['files'] = []
    
    
    context['query'] = query
    context['page_obj'] = p.get_page(page)
    context['page'] = int(page)
        
    return render(request, 'search/search.html', context)