from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def get_basic_metrics(issues):
    total = len(issues)
    if total == 0:
        return {
            "total": 0,
            "potholes": 0,
            "garbage": 0,
            "critical": 0,
            "high_priority": 0,
            "pending": 0,
            "resolved": 0,
            "resolution_rate": 0.0,
            "sla_met_pct": 100.0,
            "avg_response_hours": 0.0
        }
        
    potholes = sum(1 for i in issues if i.get("type") == "Pothole")
    garbage = sum(1 for i in issues if i.get("type") == "Garbage")
    critical = sum(1 for i in issues if i.get("priority") == "Critical")
    high_priority = sum(1 for i in issues if i.get("priority") == "High")
    pending = sum(1 for i in issues if i.get("status") == "Pending")
    resolved = sum(1 for i in issues if i.get("status") == "Resolved")
    
    resolution_rate = (resolved / total) * 100.0
    
    # Calculate average resolution time (in hours) and SLA compliance
    resolved_durations = []
    sla_compliance_count = 0
    now = datetime.now()
    
    for i in issues:
        reported_at = datetime.fromisoformat(i.get("reported_at"))
        sla_days = i.get("sla_days", 3)
        sla_limit = reported_at + timedelta(days=sla_days)
        
        if i.get("status") == "Resolved" and i.get("resolved_at"):
            resolved_at = datetime.fromisoformat(i.get("resolved_at"))
            duration_hours = (resolved_at - reported_at).total_seconds() / 3600.0
            resolved_durations.append(duration_hours)
            
            # Check SLA
            if resolved_at <= sla_limit:
                sla_compliance_count += 1
        else:
            # Active issue
            if now <= sla_limit:
                sla_compliance_count += 1
                
    avg_response_hours = float(np.mean(resolved_durations)) if resolved_durations else 18.5 # default benchmark
    sla_met_pct = (sla_compliance_count / total) * 100.0
    
    return {
        "total": total,
        "potholes": potholes,
        "garbage": garbage,
        "critical": critical,
        "high_priority": high_priority,
        "pending": pending,
        "resolved": resolved,
        "resolution_rate": resolution_rate,
        "sla_met_pct": sla_met_pct,
        "avg_response_hours": avg_response_hours
    }

def get_issue_trends(issues, days_back=14):
    now = datetime.now().date()
    dates = [now - timedelta(days=d) for d in range(days_back - 1, -1, -1)]
    
    trends = {d.strftime("%b %d"): {"Pothole": 0, "Garbage": 0, "Others": 0} for d in dates}
    
    for i in issues:
        reported_date = datetime.fromisoformat(i.get("reported_at")).date()
        date_str = reported_date.strftime("%b %d")
        if date_str in trends:
            itype = i.get("type")
            if itype in ["Pothole", "Garbage"]:
                trends[date_str][itype] += 1
            else:
                trends[date_str]["Others"] += 1
                
    # Format for chart
    data = []
    for date_str, counts in trends.items():
        for k, v in counts.items():
            data.append({
                "Date": date_str,
                "Issue Type": k,
                "Count": v
            })
            
    return pd.DataFrame(data)

def get_ward_distribution(issues):
    wards_data = {}
    for i in issues:
        ward = i.get("ward", "Unknown")
        itype = i.get("type", "Other")
        
        if ward not in wards_data:
            wards_data[ward] = {"Pothole": 0, "Garbage": 0, "Others": 0, "Total": 0}
            
        wards_data[ward]["Total"] += 1
        if itype in ["Pothole", "Garbage"]:
            wards_data[ward][itype] += 1
        else:
            wards_data[ward]["Others"] += 1
            
    # Format for charts
    rows = []
    for ward, counts in wards_data.items():
        rows.append({
            "Ward": ward,
            "Pothole": counts["Pothole"],
            "Garbage": counts["Garbage"],
            "Others": counts["Others"],
            "Total": counts["Total"]
        })
    return pd.DataFrame(rows).sort_values(by="Total", ascending=False)

def get_severity_distribution(issues):
    severities = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
    for i in issues:
        priority = i.get("priority", "Medium")
        if priority in severities:
            severities[priority] += 1
            
    return pd.DataFrame([
        {"Priority": k, "Count": v} for k, v in severities.items()
    ])

def get_area_resolution_table(issues):
    ward_stats = {}
    now = datetime.now()
    
    for i in issues:
        ward = i.get("ward", "Unknown")
        status = i.get("status")
        reported_at = datetime.fromisoformat(i.get("reported_at"))
        sla_days = i.get("sla_days", 3)
        sla_limit = reported_at + timedelta(days=sla_days)
        
        if ward not in ward_stats:
            ward_stats[ward] = {
                "Ward": ward,
                "Total": 0,
                "Open": 0,
                "Resolved": 0,
                "SLA_Met": 0,
                "Resolution_Durations": []
            }
            
        stats = ward_stats[ward]
        stats["Total"] += 1
        
        if status == "Resolved":
            stats["Resolved"] += 1
            if i.get("resolved_at"):
                resolved_at = datetime.fromisoformat(i.get("resolved_at"))
                duration_hours = (resolved_at - reported_at).total_seconds() / 3600.0
                stats["Resolution_Durations"].append(duration_hours)
                if resolved_at <= sla_limit:
                    stats["SLA_Met"] += 1
        else:
            stats["Open"] += 1
            if now <= sla_limit:
                stats["SLA_Met"] += 1
                
    # Calculate averages
    rows = []
    for ward, stats in ward_stats.items():
        durations = stats["Resolution_Durations"]
        avg_res = f"{np.mean(durations):.1f} hrs" if durations else "18.5 hrs" # fallback benchmark
        
        sla_pct = (stats["SLA_Met"] / stats["Total"]) * 100.0
        
        rows.append({
            "Ward": ward,
            "Open": stats["Open"],
            "Resolved": stats["Resolved"],
            "Avg Response": avg_res,
            "SLA Compliance": f"{sla_pct:.1f}%"
        })
        
    return pd.DataFrame(rows).sort_values(by="Open", ascending=False)
