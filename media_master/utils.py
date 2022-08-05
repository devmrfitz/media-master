# Author: devmrfitz

import os

class UnidentifiedVideoError(Exception):
    pass

FFMPEG_PATH = os.path.join(os.path.dirname(__file__), 'ffmpeg/ffmpeg')
FONT_FILE_PATH = os.path.join(os.path.dirname(__file__), 'Roboto-Bold.ttf')
FONT_RATIO = 1.8

def invert_image(source_path, destination_path):
    from PIL import Image, ImageEnhance, ImageOps
    image = Image.open(source_path)
    image = ImageOps.invert(image)
    image = ImageEnhance.Contrast(image).enhance(2)
    image.save(destination_path)
    image.close()

def compress_image(source_path: str, destination_path: str, quality=75):
    from PIL import Image
    image = Image.open(source_path)
    image.save(destination_path, optimize=True, quality=quality)
    image.close()

def resize_image(source_path: str, destination_path: str, width: int, height: int):
    from PIL import Image 
    image = Image.open(source_path)
    # resize
    image = image.resize((width, height))
    image.save(destination_path)
    # image.show()
    image.close()

def watermark_image_using_image(source_path, destination_path, watermark_url):
    # download watermark to temporary directory
    import tempfile
    import requests
    import os

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    # Create a temporary file name
    watermark_filename = os.path.join(temp_dir, 'temp.png')

    # Download the watermark
    response = requests.get(watermark_url)
    with open(watermark_filename, 'wb') as f:
        f.write(response.content)
    
    from PIL import Image   
    image = Image.open(source_path)
    # resize
    image = image.resize((500, 500))
    # watermark
    watermark = Image.open(watermark_filename)
    image.paste(watermark, (0, 0), watermark)
    image.save(destination_path)
    # image.show()
    image.close()

def watermark_image_using_text(source_path, destination_path, text, color="black", opacity=0.5, diagonal_percentage = 0.6):
    import math
    from PIL import Image, ImageFont, ImageDraw

    image = Image.open(source_path)

    # sample dimensions
    pdf_width = image.size[0]
    pdf_height = image.size[1]

    message_length = len(text)

    # load font (tweak ratio based on your particular font)
    
    diagonal_length = int(math.sqrt((pdf_width**2) + (pdf_height**2)))
    diagonal_to_use = diagonal_length * diagonal_percentage
    font_size = int(diagonal_to_use / (message_length / FONT_RATIO))
    font = ImageFont.truetype(FONT_FILE_PATH, font_size)
    #font = ImageFont.load_default() # fallback

    # watermark
    mark_width, mark_height = font.getsize(text)
    watermark = Image.new('RGBA', (mark_width, mark_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)
    draw.text((0, 0), text=text, font=font, fill=(0, 0, 0, int(256 * opacity)), color=color)
    angle = math.degrees(math.atan(pdf_height/pdf_width))
    watermark = watermark.rotate(angle, expand=1)

    # merge
    wx, wy = watermark.size
    px = int((pdf_width - wx)/2)
    py = int((pdf_height - wy)/2)
    image.paste(watermark, (px, py, px + wx, py + wy), watermark)

    image.save(destination_path)
    image.close()

def trim_video(video_path, output_path, start_seconds, end_seconds):
    import subprocess
    import datetime

    # change seconds to HH:MM:SS
    start_time = str(datetime.timedelta(seconds=start_seconds))
    end_time = str(datetime.timedelta(seconds=end_seconds))

    # Trim the video
    ffmpeg_output = subprocess.run([FFMPEG_PATH, '-i', video_path, '-ss', start_time, '-to', end_time, 
        '-c', 'copy', output_path, '-accurate_seek'], capture_output=True, text=True)
    if ffmpeg_output.stderr and "Conversion failed!" in ffmpeg_output.stderr:
        raise UnidentifiedVideoError(ffmpeg_output.stderr)

def compress_video(video_path, output_path, crf=28):
    if crf < 0 or crf > 51:
        raise Exception('crf must be between 0 and 51')
            
    import subprocess

    # Compress the video
    ffmpeg_output = subprocess.run([FFMPEG_PATH, '-i', video_path, '-c:v', 
        'libx265', '-crf', str(crf), '-c:a', 'copy', output_path], capture_output=True, text=True)
    if ffmpeg_output.stderr and "Conversion failed!" in ffmpeg_output.stderr:
        raise UnidentifiedVideoError(ffmpeg_output.stderr)

