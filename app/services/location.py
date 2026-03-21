import math

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def find_nearest_gate(user_lat, user_lon, gates):
    nearest = None
    min_dist = float("inf")

    for g in gates:
        dist = calculate_distance(user_lat, user_lon, g.latitude, g.longitude)

        if dist < min_dist:
            min_dist = dist
            nearest = g

    return nearest, min_dist