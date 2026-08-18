import json
import os
from datetime import datetime
from app.services.priority import calculate_priority

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "sample_issues.json")

def load_issues():
    if not os.path.exists(DB_PATH):
        return []
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading issues: {e}")
        return []

def save_issues(issues):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(issues, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving issues: {e}")
        return False

def save_uploaded_file(uploaded_file, filename):
    import os
    from PIL import Image
    upload_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "uploads")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    if isinstance(uploaded_file, Image.Image):
        uploaded_file.save(file_path)
    elif hasattr(uploaded_file, "getbuffer"):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    else:
        # In case it is a numpy array (annotated image)
        import cv2
        cv2.imwrite(file_path, uploaded_file)
        
    return file_path

def add_issue(issue_type, description, priority, latitude, longitude, location_text, ward, confidence=None, image_path=None):
    issues = load_issues()
    
    # Generate sequential ID
    max_num = 0
    for issue in issues:
        id_parts = issue.get("id", "").split("-")
        if len(id_parts) == 3 and id_parts[0] == "ISS" and id_parts[1] == "2026":
            try:
                num = int(id_parts[2])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    
    new_id = f"ISS-2026-{max_num + 1:04d}"
    
    # Calculate transparent priority reasoning
    # Pass priority as severity
    p_info = calculate_priority(
        category=issue_type,
        severity=priority,
        confidence=confidence,
        location_text=location_text,
        description=description
    )
    
    final_priority = p_info["priority"]
    priority_reason = p_info["reason"]
    
    sla_days = 5
    if final_priority == "Critical":
        sla_days = 1
    elif final_priority == "High":
        sla_days = 2
    elif final_priority == "Medium":
        sla_days = 3
        
    new_issue = {
        "id": new_id,
        "type": issue_type,
        "description": description,
        "status": "Pending",
        "priority": final_priority,
        "priority_reason": priority_reason,
        "latitude": float(latitude) if latitude is not None else 12.9716,
        "longitude": float(longitude) if longitude is not None else 77.5946,
        "location_text": location_text,
        "ward": ward,
        "reported_at": datetime.now().isoformat().split(".")[0],
        "confidence": confidence,
        "assigned_to": None,
        "sla_days": sla_days,
        "resolved_at": None,
        "image_path": image_path
    }
    
    issues.append(new_issue)
    save_issues(issues)
    return new_issue

def update_issue_status(issue_id, status, assigned_to=None):
    issues = load_issues()
    updated = False
    for issue in issues:
        if issue.get("id") == issue_id:
            issue["status"] = status
            if assigned_to is not None:
                issue["assigned_to"] = assigned_to
            if status == "Resolved":
                issue["resolved_at"] = datetime.now().isoformat().split(".")[0]
            else:
                issue["resolved_at"] = None
            updated = True
            break
    if updated:
        save_issues(issues)
    return updated
