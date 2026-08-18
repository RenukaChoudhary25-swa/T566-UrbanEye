from pathlib import Path

GARBAGE_DATASET = Path("datasets/garbage")

# All 6 waste categories become class 1 = garbage
GARBAGE_CLASS_ID = 1

for split in ["train", "valid", "test"]:
    labels_folder = GARBAGE_DATASET / split / "labels"

    if not labels_folder.exists():
        print(f"Not found: {labels_folder}")
        continue

    count = 0

    for label_file in labels_folder.glob("*.txt"):
        lines = label_file.read_text().splitlines()
        new_lines = []

        for line in lines:
            parts = line.split()

            if len(parts) >= 5:
                parts[0] = str(GARBAGE_CLASS_ID)

            new_lines.append(" ".join(parts))

        label_file.write_text("\n".join(new_lines))
        count += 1

    print(f"{split}: converted {count} label files")

print("Garbage labels converted successfully!")