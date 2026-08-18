from pathlib import Path
import shutil
import random

random.seed(42)

SRC = Path("datasets/urbaneye_final")
DST = Path("datasets/urbaneye_small")

TRAIN_PER_CLASS = 60
VAL_PER_CLASS = 16


# -------------------------------------------------
# CLEAN OLD SMALL DATASET
# -------------------------------------------------

if DST.exists():
    shutil.rmtree(DST)


for split in ["train", "valid"]:
    (DST / split / "images").mkdir(parents=True, exist_ok=True)
    (DST / split / "labels").mkdir(parents=True, exist_ok=True)


# -------------------------------------------------
# FIND IMAGE + LABEL PAIRS
# -------------------------------------------------

def find_pairs(split):

    image_dir = SRC / split / "images"
    label_dir = SRC / split / "labels"

    pothole = []
    garbage = []

    for label in label_dir.glob("*.txt"):

        lines = label.read_text(errors="ignore").splitlines()

        classes = set()

        for line in lines:

            parts = line.strip().split()

            if parts:
                try:
                    classes.add(int(parts[0]))
                except:
                    pass

        image = None

        for ext in [".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"]:

            candidate = image_dir / (label.stem + ext)

            if candidate.exists():
                image = candidate
                break

        if image is None:
            continue

        if 0 in classes:
            pothole.append((image, label))

        if 1 in classes:
            garbage.append((image, label))

    return pothole, garbage


# -------------------------------------------------
# COPY UNIQUE IMAGES
# -------------------------------------------------

def copy_images(items, destination, amount, used):

    random.shuffle(items)

    count = 0

    for image, label in items:

        if image.name in used:
            continue

        shutil.copy2(
            image,
            destination / "images" / image.name
        )

        shutil.copy2(
            label,
            destination / "labels" / label.name
        )

        used.add(image.name)

        count += 1

        if count >= amount:
            break

    return count


# -------------------------------------------------
# TRAIN
# -------------------------------------------------

train_pothole, train_garbage = find_pairs("train")

print("Available training images:")
print("Pothole:", len(train_pothole))
print("Garbage:", len(train_garbage))

used_train = set()

p = copy_images(
    train_pothole,
    DST / "train",
    TRAIN_PER_CLASS,
    used_train
)

g = copy_images(
    train_garbage,
    DST / "train",
    TRAIN_PER_CLASS,
    used_train
)


# -------------------------------------------------
# VALIDATION
# -------------------------------------------------

val_pothole, val_garbage = find_pairs("valid")

print("\nAvailable validation images:")
print("Pothole:", len(val_pothole))
print("Garbage:", len(val_garbage))

used_val = set()

vp = copy_images(
    val_pothole,
    DST / "valid",
    VAL_PER_CLASS,
    used_val
)

vg = copy_images(
    val_garbage,
    DST / "valid",
    VAL_PER_CLASS,
    used_val
)


# -------------------------------------------------
# DATA YAML
# -------------------------------------------------

yaml = """train: train/images
val: valid/images

nc: 2
names: ['pothole', 'garbage']
"""

(DST / "data.yaml").write_text(yaml)


# -------------------------------------------------
# FINAL REPORT
# -------------------------------------------------

train_count = len(
    list((DST / "train" / "images").glob("*"))
)

val_count = len(
    list((DST / "valid" / "images").glob("*"))
)

train_labels = len(
    list((DST / "train" / "labels").glob("*.txt"))
)

val_labels = len(
    list((DST / "valid" / "labels").glob("*.txt"))
)


print("\n===================================")
print("SMALL URBANEYE DATASET CREATED")
print("===================================")

print("Pothole requested:", TRAIN_PER_CLASS)
print("Garbage requested:", TRAIN_PER_CLASS)

print("Training images:", train_count)
print("Training labels:", train_labels)

print("Validation images:", val_count)
print("Validation labels:", val_labels)

print("\nDataset:")
print(DST.resolve())