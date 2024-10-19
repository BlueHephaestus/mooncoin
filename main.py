import json
from datetime import datetime
import shutil


# dst_link = "https://raw.githubusercontent.com/BlueHephaestus/mooncoin/refs/heads/main/moon.png"
imgs_dir = "imgs/"
dst_img_file = "moon.png"
log_file = "updates.log"

# Get correct image from lookup for tonight
# Copy it to the correct location

# Get current date
today = datetime.now().strftime("%Y-%m-%d")

with open("lookup.json", "r") as f:
    lookup = json.load(f)

# Get moon data for today
moon_data = lookup[today]
img_fname, _, emoji, desc = moon_data

# Get image to use
img_fpath = f"{imgs_dir}{img_fname}"

# Copy to dst img file.
shutil.copyfile(img_fpath, dst_img_file)

# Get new name to use with emoji
name = f"Lunar {emoji}"

# Load existing metadata and update this value
with open("metadata.json", "r") as f:
    metadata = json.load(f)
metadata["name"] = name

# Re-write metadata file
with open("metadata.json", "w") as f:
    # json.dump(metadata, f)
    json.dump(metadata, f, ensure_ascii=False, indent=4)

# Update log file.
with open(log_file, "a") as f:
    f.write(f"{today}: Icon: {img_fname}, Name: {name}, Desc: {desc}\n")

print(f"Updated {dst_img_file} and metadata.json with {img_fname} for {today}")