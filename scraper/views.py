from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .CustomViews.scraper.scraping import scrape_modatelas_core

def scrape_modatelas_view(request):
    data = scrape_modatelas_core()
    # Devolver como JSON
    return JsonResponse(data, safe=False)