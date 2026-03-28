from app.database.supabase_client import supabase

def get_ngos():
    try:
        response = supabase.table("users").select("*").eq("role", "ngo").execute()
        return response.data
    except Exception as e:
        print("NGO FETCH ERROR:", e)
        return []

def get_volunteers():
    try:
        response = supabase.table("users").select("*").eq("role", "volunteer").execute()
        return response.data
    except Exception as e:
        print("VOLUNTEER FETCH ERROR:", e)
        return []

def insert_report(data):
    try:
        response = supabase.table("reports").insert(data).execute()
        return response.data
    except Exception as e:
        print("INSERT ERROR:", e)
        return []

def get_all_reports():
    response = supabase.table("reports").select("*").execute()
    return response.data 

def get_volunteer_tasks(name):
    response = supabase.table("reports") \
        .select("*") \
        .ilike("ai_response", f"%{name}%") \
        .execute()

    return response.data   

def update_report_status(report_id, status):
    response = supabase.table("reports") \
        .update({"status": status}) \
        .eq("id", report_id) \
        .execute()

    return response.data