import re

def calculate_priority(category, severity, confidence, location_text, description):
    """
    Calculates issue priority dynamically and transparently based on:
    - category (Pothole, Garbage, Water Logging, Streetlight Out, etc.)
    - severity (High, Medium, Low)
    - confidence (0.0 to 1.0, or None)
    - location/impact (keywords indicating high public risk)
    """
    # 1. Base Score from Category & Severity
    severity_map = {"High": 3, "Medium": 2, "Low": 1}
    base_score = severity_map.get(severity, 2)
    
    # Adjust base score slightly based on the category impact (e.g. Water Logging / Traffic is inherently higher impact)
    cat_modifier = 0.0
    if category in ["Water Logging", "Traffic Signal Out"]:
        cat_modifier = 0.5
        
    # 2. Confidence Modifier (AI detections)
    # Higher confidence increases priority; low confidence reduces it to prevent false alarms
    conf_score = 0.0
    if confidence is not None:
        if confidence >= 0.85:
            conf_score = 1.0
        elif confidence >= 0.60:
            conf_score = 0.5
        else:
            conf_score = -0.5
    else:
        # Manual reports get a standard confidence score
        conf_score = 0.5
        
    # 3. Location & Impact Modifier
    # Scan location text and description for high-priority areas
    impact_keywords = [
        "school", "hospital", "metro", "station", "highway", "main road", 
        "junction", "crossing", "flyover", "stadium", "market", "office", 
        "plaza", "avenue", "bus stop", "clinic", "residential", "street", "road"
    ]
    
    search_text = f"{location_text} {description}".lower()
    high_impact = any(kw in search_text for kw in impact_keywords)
    
    impact_score = 1.0 if high_impact else 0.0
    
    # Total Score calculation
    total_score = base_score + cat_modifier + conf_score + impact_score
    
    # Map to priority grades
    if total_score >= 4.5:
        priority = "Critical"
    elif total_score >= 3.5:
        priority = "High"
    elif total_score >= 2.0:
        priority = "Medium"
    else:
        priority = "Low"
        
    # Build reasons
    reasons = []
    reasons.append(f"Severity classification: **{severity}** (+{base_score} pts)")
    if cat_modifier != 0:
        reasons.append(f"High-impact category: **{category}** (+{cat_modifier} pts)")
        
    if confidence is not None:
        reasons.append(f"YOLO AI confidence: **{confidence:.1%}** ({'+' if conf_score >= 0 else ''}{conf_score} pts)")
    else:
        reasons.append(f"Citizen manually verified (+{conf_score} pts)")
        
    if high_impact:
        # Find matching keyword
        matched_kw = next((kw for kw in impact_keywords if kw in search_text), "key infrastructure")
        reasons.append(f"Impact zone (near **{matched_kw}**) (+{impact_score} pts)")
    else:
        reasons.append("Standard impact zone (+0.0 pts)")
        
    reason_text = " • ".join(reasons)
    
    return {
        "priority": priority,
        "score": total_score,
        "reason": reason_text,
        "high_impact": high_impact
    }
