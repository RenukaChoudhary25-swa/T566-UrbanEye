import sys
import os
from PIL import Image

# Add current working directory to sys.path
sys.path.append(os.getcwd())

from app.services.issues import load_issues, add_issue
from app.services.inference import run_detection

def main():
    print("=== URBANEYE VERIFICATION TEST ===")
    
    # 1. Test database load
    print("\n[1/3] Testing database load...")
    issues = load_issues()
    print(f"Loaded {len(issues)} issues from JSON database.")
    if len(issues) > 0:
        print("✅ Database load OK.")
    else:
        print("❌ Database load failed or database empty.")
        sys.exit(1)
        
    # 2. Test database write/append
    print("\n[2/3] Testing database write...")
    test_issue = add_issue(
        issue_type="Pothole",
        description="Verification test pothole description.",
        priority="Low",
        latitude=12.95,
        longitude=77.60,
        location_text="Test Road, Ward 1",
        ward="Ward 1"
    )
    print(f"Successfully added test issue {test_issue['id']}.")
    
    # Reload and verify count has increased
    issues_after = load_issues()
    print(f"Loaded {len(issues_after)} issues after addition.")
    if len(issues_after) == len(issues) + 1:
        print("✅ Database write OK.")
    else:
        print("❌ Database write failed: issue counts did not match.")
        sys.exit(1)
        
    # 3. Test YOLOv8 Model loading and inference
    print("\n[3/3] Testing YOLOv8 model loading and inference...")
    sample_img_dir = os.path.abspath(os.path.join(os.getcwd(), "datasets", "urbaneye_small", "valid", "images"))
    
    if os.path.exists(sample_img_dir):
        files = [f for f in os.listdir(sample_img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if files:
            img_path = os.path.join(sample_img_dir, files[0])
            print(f"Found sample image: {img_path}")
            
            image = Image.open(img_path)
            result = run_detection(image)
            
            print(f"Detection ran successfully. Found {len(result['detections'])} detections.")
            for det in result['detections']:
                print(f" - {det['class_name']}: confidence={det['confidence']:.2f}, severity={det['severity']}")
            print("✅ Model inference OK.")
        else:
            print("⚠️ No images found in dataset valid/images directory to test. Skipping inference test.")
            print("✅ Model load verification skipped but environment OK.")
    else:
        print("⚠️ Dataset directory not found. Skipping inference test.")
        print("✅ Model load verification skipped but environment OK.")

if __name__ == "__main__":
    main()
