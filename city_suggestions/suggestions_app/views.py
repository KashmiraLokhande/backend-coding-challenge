from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .models import City
from .utils import calculate_score

@require_GET
def suggestions(request):
    query = request.GET.get('q', '').strip()
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')

    if not query:
        return JsonResponse({"suggestions": []})

    suggestions_list = []

    cities = City.objects.filter(name__icontains=query)

    

    for city in cities:
        score = calculate_score(query, latitude, longitude, city)
        suggestions_list.append({
            'name': f"{city.name}, {city.country}",
            'latitude': str(city.lat),
            'longitude': str(city.lon),
            'score': score
        })
    # Sort the suggestions by descending score
    suggestions_list.sort(key=lambda x: x['score'], reverse=True)

    return JsonResponse({"suggestions": suggestions_list})
