
import json
import logging
from shutil import rmtree
import azure.functions as func
from azure.storage.blob import BlobServiceClient, ContentSettings
import os 
import tempfile

from media_master.utils import compress_image, compress_video, invert_image, resize_image, trim_video, watermark_image_using_image, watermark_image_using_text 

AZURE_CONNECTION_STRING = os.getenv('AzureWebJobsStorage')
CONTAINER_NAME = "azure-webjobs-hosts"
print = logging.info

def main(myblob: func.blob.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes and {len(myblob.read())}")
    
    metadata = myblob.metadata
    if ("command" not in metadata):
        logging.info("No command metadata found")
        return

    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)

    directory = tempfile.mkdtemp()
    source_file_path = os.path.join(directory, f"source.{myblob.name.split('.')[-1]}")
    destination_file_path = os.path.join(directory, f"destination.{myblob.name.split('.')[-1]}")
    container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)

    blob_path = "/".join(myblob.name.split("/")[1:])
    with open(source_file_path, "wb") as download_file:
        download_file.write(container_client.download_blob(blob_path).readall())    

    command = json.loads(metadata["command"])
    metadata.pop("command")
    parameters = command[1:]

    if (command[0] == "compress_image"):
        logging.info("Compressing image")
        compress_image(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading compressed image")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting compressed image")
    elif (command[0] == "resize_image"):
        logging.info("Resizing image")
        resize_image(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading resized image")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting resized image")
    elif (command[0] == "invert_image"):
        logging.info("Inverting image")
        invert_image(source_file_path, destination_file_path)
        logging.info("Uploading inverted image")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting inverted image")
    elif (command[0] == "watermark_image_using_image"):
        logging.info("Watermarking image using image")
        watermark_image_using_image(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading watermarked image")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting watermarked image")
    elif (command[0] == "watermark_image_using_text"):
        logging.info("Watermarking image using text")
        watermark_image_using_text(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading watermarked image")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting watermarked image")
    elif (command[0] == "trim_video"):
        logging.info("Trimming video")
        trim_video(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading trimmed video")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting trimmed video")
    elif (command[0] == "compress_video"):
        logging.info("Compressing video")
        compress_video(source_file_path, destination_file_path, *parameters)
        logging.info("Uploading compressed video")
        container_client.upload_blob(name=blob_path, data=open(destination_file_path, "rb"), 
        metadata=metadata, overwrite=True, content_settings=ContentSettings(content_type=myblob.blob_properties.get("ContentType")))
        logging.info("Deleting compressed video")
    rmtree(directory)

    


    
