from math import radians, sin, cos, sqrt, atan2

def calculate_distance(latitude1, longitude1, latitude2, longitude2):
    # Function to calculate the distance between two sets of coordinates
    # Using Haversine formula
    R = 6371.0  # Earth's radius in km

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)
    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_score(query, latitude=None, longitude=None, city=None):
    if latitude is not None and longitude is not None:
        # If latitude and longitude are provided, use the previous scoring function
        return calculate_score_with_distance(query, latitude, longitude, city)
    else:
        # If latitude and longitude are not provided, use the new scoring function
        return calculate_score_without_distance(query, city)

def calculate_score_without_distance(query, city=None):
    score = 0.0

    if not city:
        return score

    name_lower = city.name.lower()
    query_lower = query.lower()

    if query_lower == name_lower:
        # If the query exactly matches the city name, give the highest score
        score = 1.0
    elif name_lower.startswith(query_lower):
        # If the query is a prefix of the city name, give a high score
        score = 0.7
    elif query_lower in name_lower:
        # If the query is present anywhere in the city name, give a moderate score
        score = 0.5
    else:
        # If the query is not present in the city name, give a lower score
        score = 0.0

    return score

def calculate_score_with_distance(query, latitude, longitude, city):
    score = 0.0
    name_lower = city.name.lower()
    query_lower = query.lower()

    if query_lower in name_lower:
        # Add 0.1 to the score if the city name contains the search query
        score += 0.1

        # If latitude and longitude are provided, consider the distance for scoring
        if latitude and longitude:
            distance = calculate_distance(float(latitude), float(longitude), city.lat, city.lon)
            # Add distance-based scoring (the closer, the higher the score)
            score += (1.0 - (distance / 1000)) if distance <= 1000 else 0.0

    return score
