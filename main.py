import json
from datetime import datetime
import shutil


# dst_link = "https://raw.githubusercontent.com/BlueHephaestus/mooncoin/refs/heads/main/moon.png"
imgs_dir = "imgs/"
dst_file = "moon.png"
log_file = "updates.log"

# Get correct image from lookup for tonight
# Copy it to the correct location

# Get current date
today = datetime.now().strftime("%Y-%m-%d")

with open("lookup.json", "r") as f:
    lookup = json.load(f)

# Get moon data for today
moon_data = lookup[today]
img_fname, _, desc = moon_data
img_fpath = f"{imgs_dir}{img_fname}"

# Copy to dst file.
shutil.copyfile(img_fpath, dst_file)

# Update log file.
with open(log_file, "a") as f:
    f.write(f"{today}: Icon: {img_fname}, Desc: {desc}\n")

print(f"Updated {dst_file} with {img_fname} for {today}")