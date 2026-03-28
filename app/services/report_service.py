import json
from app.database.queries import get_ngos, get_volunteers, insert_report
from app.services.ai_service import analyze_and_match
from app.utils.location import calculate_distance


def format_users(users):
    return [
        f"{u['name']} ({u['role']}) - {u['skills']} in {u['location']}"
        for u in users
    ]


# 🔥 NEW FUNCTION
def filter_nearby(users, lat, lon, max_km=10):
    nearby = []

    for u in users:
        if u.get("latitude") and u.get("longitude"):
            dist = calculate_distance(lat, lon, u["latitude"], u["longitude"])
            if dist <= max_km:
                nearby.append(u)

    return nearby


def process_report(report):
    ngos_raw = get_ngos()
    volunteers_raw = get_volunteers()

    # 🔥 STEP 1: FILTER BY LOCATION
    nearby_ngos = filter_nearby(
        ngos_raw,
        report.latitude,
        report.longitude
    )

    nearby_volunteers = filter_nearby(
        volunteers_raw,
        report.latitude,
        report.longitude
    )

    print("NEARBY NGOs:", nearby_ngos)
    print("NEARBY Volunteers:", nearby_volunteers)

    # 🔥 STEP 2: FORMAT FOR AI
    ngos = format_users(nearby_ngos)
    volunteers = format_users(nearby_volunteers)

    # 🔥 STEP 3: AI MATCHING
    ai_result = analyze_and_match(
        report.description,
        ngos,
        volunteers
    )

    # 🔥 STEP 4: PARSE AI
    try:
        ai_data = json.loads(ai_result)
    except:
        ai_data = {
            "category": "unknown",
            "urgency": "medium",
            "best_ngo": "not found",
            "matched_volunteers": []
        }

    # 🔥 STEP 5: SAVE
    saved = insert_report({
        "description": report.description,
        "location": report.location,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "image_url": report.image_url,
        "ai_response": json.dumps(ai_data),
        "category": ai_data.get("category"),
        "urgency": ai_data.get("urgency"),
        "status": "pending"
    })

    return {
        "ai_result": ai_data,
        "saved": saved
    }