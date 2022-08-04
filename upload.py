import json
import os
from azure.storage.blob import BlobServiceClient, ContentSettings

SAMPLE_IMAGE_PATH = "media_master/test.jpg"
SAMPLE_VIDEO_PATH = "media_master/test.mp4"

# Create a local directory to hold blob data
AZURE_CONNECTION_STRING = os.getenv('AzureWebJobsStorage')
if AZURE_CONNECTION_STRING is None:
    AZURE_CONNECTION_STRING = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://127.0.0.1:10000/devstoreaccount1;QueueEndpoint=http://127.0.0.1:10001/devstoreaccount1;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;"
CONTAINER_NAME = "devmrfitz"

# print(f"String is {AZURE_CONNECTION_STRING}")
blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

# Create a file in the local data directory to upload and download

# Create a blob client using the local file name as the name for the blob
blob_client = blob_service_client.get_container_client(container=CONTAINER_NAME) #, blob=f"data/test.jpg")

# Upload the created file

# blob_client.upload_blob(name = f"data/test.jpg", data=open(SAMPLE_IMAGE_PATH, 'rb'), overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
# blob_client.upload_blob(name = f"data/test.mp4", data=open(SAMPLE_VIDEO_PATH, 'rb'), overwrite=True, content_settings=ContentSettings(content_type='video/mp4'))

for command in [["compress_image", 50], ["resize_image", 20, 50], ["invert_image"], ["watermark_image_using_image", "https://i.imgur.com/hPgGyPA.png",], ["watermark_image_using_text", "jadoo", "red"], ["trim_video", 2, 4], ["compress_video"]]:
# for command in [["invert_image"]]:
    if "image" == command[0].split("_")[1]:
        blob_client.upload_blob(name = f"data/test_{command[0]}.jpg", data=open(SAMPLE_IMAGE_PATH, 'rb'), metadata={"command": json.dumps(command)}, overwrite=True, content_settings=ContentSettings(content_type='image/jpeg'))
    elif "video" == command[0].split("_")[1]:
        blob_client.upload_blob(name = f"data/test_{command[0]}.mp4", data=open(SAMPLE_VIDEO_PATH, 'rb'), metadata={"command": json.dumps(command)}, overwrite=True, content_settings=ContentSettings(content_type='video/mp4'))

