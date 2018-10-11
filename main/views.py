from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .models import Feed, SeedWikiWebsite, Website, WikiCategory


def index(request):
    return render(request, "index.html")


@staff_member_required
def crawl(request):
    return render(request, "crawl.html", {
        'num_cats': WikiCategory.objects.count(),
        'num_seed_links': SeedWikiWebsite.objects.count(),
        'num_websites': Website.objects.count(),
        'num_feeds': Feed.objects.count()
    })


@require_GET
def search(request):
    results = []
    query = request.GET.get("q")
    if query:
        vector = SearchVector('title', 'description', config="german")
        search_query = SearchQuery(query, config="german")
        results = Feed.objects.annotate(rank=SearchRank(vector, search_query)).order_by('-rank')

    return render(request, "search.html", {
        'query': query,
        'results': results,
    })
