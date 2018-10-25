from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET

from .models import Feed, SeedWikiWebsite, Website, WikiCategory, STATUS_WAITING, STATUS_SUCCESS, STATUS_ERROR, STATUS_WORKING


@require_GET
def index(request):
    results = []
    query = request.GET.get("q")
    if query:
        # url and title have the main weights
        vector = SearchVector('title', weight='A', config="german") + SearchVector('website', weight='A', config="german") + SearchVector('description', weight='B', config="german")
        search_query = SearchQuery(query, config="german")
        results = Feed.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gte=0.3).order_by('-rank')

    return render(request, "index.html", {
        'query': query,
        'results': results,
    })


@staff_member_required
def stats(request):
    return render(request, "stats.html", {
        'num_cats': [WikiCategory.objects.count(), WikiCategory.objects.filter(status=STATUS_WAITING).count(), WikiCategory.objects.filter(status=STATUS_WORKING).count()],
        'num_seed_links': [SeedWikiWebsite.objects.count(), SeedWikiWebsite.objects.filter(status=STATUS_WAITING).count(), SeedWikiWebsite.objects.filter(status=STATUS_WORKING).count()],
        'num_websites': [Website.objects.count(), Website.objects.filter(status=STATUS_WAITING).count(), Website.objects.filter(status=STATUS_WORKING).count()],
        'num_feeds': [Feed.objects.count()]
    })
