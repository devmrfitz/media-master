# Media Maestro

Welcome to Media Maestro, a tool for managing media files. It is a simple utility that allows performing common tasks on media files in an asynchronous manner, so that you can focus on your work without being interrupted by the heavy lifting.

## Usage

Media Maestro accepts commands in the form of the following metadata fields associated with each blob:

- `command`: Stringified list containing the command to be executed as the first element and the arguments to be passed to it.
- `email`(optional): Email address of the site admin, so that they can be notified in case a user uploads an invalid file.

## Commands

The currently supported commands are present in the `media_maestro/utils.py` file.

For example, the following metadata on an image blob would trigger a compression with 80% quality:

```json
{
    "command": "[\"compress_image\", 80]",
    "email": "email@example.com"
}
```

To see further usage examples, go to `upload.py`.

## Techologies used

- [Azure Functions](https://azure.microsoft.com/en-us/services/azure-functions/): Azure Functions are a set of serverless functions that can be triggered by events, such as when a file is uploaded. Media Maestro uses Azure Functions to trigger the processing of media files.

- [Azure Blob Storage](https://azure.microsoft.com/en-us/services/azure-storage/): Azure Blob Storage is a cloud storage service that allows you to store and retrieve files from a cloud storage account. The files which Media Maestro operates on are stored in Azure Blob Storage.

- [Courier](https://www.courier.com): Courier is a multi-channel notification service that allows you to send notifications to users. Media Maestro uses Courier to send email to site admins when an invalid file is uploaded.

- [ffmpeg](https://www.ffmpeg.org): ffmpeg is a command line utility that allows you to convert media files. Media Maestro uses ffmpeg to process video files.

- [Pillow](https://github.com/python-pillow/Pillow): Pillow is a Python library that allows you to manipulate images. Media Maestro uses Pillow to manipulate images.
