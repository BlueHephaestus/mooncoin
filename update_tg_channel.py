# Take the name from the metadata file,
# And the moon.png image, and use them to update the telegram channel to match.
# This assumes they were just updated by the update.sh script.
#
from telethon import TelegramClient, events, sync
from telethon.tl.functions.channels import EditPhotoRequest, EditTitleRequest
from telethon.tl.types import InputChatUploadedPhoto
import json

API_ID = "10916087"
API_HASH = "338987851abe0058fed92e589150b7e1"
SYSTEM_NUMBER = "+18647109821"

channel_username = "LUNARsolana"

client = TelegramClient('bluehephaestus', API_ID, API_HASH)
client.start(SYSTEM_NUMBER)

# Get current title and image
with open("metadata.json", "r") as f:
    metadata = json.load(f)
    title = metadata["name"]

channel_entity = client.get_entity(channel_username)
upload_file_result = client.upload_file(file='moon.png')
input_chat_uploaded_photo = InputChatUploadedPhoto(upload_file_result)

# Image gets updated regardless, title will cause error if it's the same title.
try:
   result = client(EditPhotoRequest(channel=channel_entity, photo=input_chat_uploaded_photo))
except Exception as e: 
    print(e)

try:
    result = client(EditTitleRequest(channel=channel_entity, title=title))
except Exception as e:
    print(e)

