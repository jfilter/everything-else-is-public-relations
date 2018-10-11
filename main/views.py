from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .models import Feed, SeedWikiWebsite, Website, WikiCategory, STATUS_WAITING, STATUS_SUCCESS, STATUS_ERROR, STATUS_WORKING


def index(request):
    return render(request, "index.html")


@staff_member_required
def stats(request):
    return render(request, "stats.html", {
        'num_cats': [WikiCategory.objects.count(), WikiCategory.objects.filter(status=STATUS_WAITING).count(), WikiCategory.objects.filter(status=STATUS_WORKING).count()],
        'num_seed_links': [SeedWikiWebsite.objects.count(), SeedWikiWebsite.objects.filter(status=STATUS_WAITING).count(), SeedWikiWebsite.objects.filter(status=STATUS_WORKING).count()],
        'num_websites': [Website.objects.count(), Website.objects.filter(status=STATUS_WAITING).count(), Website.objects.filter(status=STATUS_WORKING).count()],
        'num_feeds': [Feed.objects.count()]
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
