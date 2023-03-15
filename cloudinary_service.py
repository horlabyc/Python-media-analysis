
# Set your Cloudinary credentials
# ==============================
from dotenv import load_dotenv
load_dotenv()

import cloudinary
import cloudinary.uploader
import cloudinary.api

import pathlib
import os
from datetime import datetime as dt


# Set configuration parameter: return "https" URLs by setting secure=True  
# ==============================
config = cloudinary.config(secure=True)
supported_ext = (".png", ".jpg", ".jpeg")

def upload_image(filename, folder="my_photo_uploads"):
  stem = pathlib.Path(filename).stem
  res = cloudinary.uploader.upload(filename, public_id=stem, folder=folder)
  return res

def upload_and_tag_image(filename, folder="my_photo_uploads"):
  stem = pathlib.Path(filename).stem
  res = cloudinary.uploader.upload(filename, public_id=stem, folder=folder, detection="openimages", auto_tagging=0.25)
  return res

def upload_photos_in_folder():
  counter = 0
  start_time = dt.now(); 
  print("===========================================")
  print(f"Upload started at {dt.now()}")
  for file in sorted(os.listdir("photos")):
    if pathlib.Path(file).suffix.lower() in supported_ext:
      try:
        print(f"Uploading {file}...")
        upload_and_tag_image("photos/" + file)
        counter += 1
      except Exception as error:
        print(f"Failed to upload file {file}:: {error}")
  end_time = dt.now(); 
  print("===========================================")
  print(f"{counter} files successfully uploaded at {dt.now()}")
  print(f"Uploaded completed in at {end_time - start_time} mins")

def get_all_tags():
  print("Fetching all media tags...")
  all_tags = []
  tags = cloudinary.api.tags(max_result=100)
  all_tags.extend(tags['tags'])
  next_cursor = tags.get('next_cursor')
  while next_cursor:
    tags = cloudinary.api.tags(max_result=100, next_cursor=next_cursor)
    all_tags.extend(tags['tags'])
    next_cursor = tags.get('next_cursor')
  return(all_tags)

def search_img():
  response = cloudinary.Search().expression(
    "resource_type:image AND tags=tree"
  ).sort_by("public_id", "desc").execute()
  return response


images = search_img()
print(images['total_count'])
for image in images['resources']:
  print(image['url'])

def get_images_with_tags():
  all_resources = []
  response = cloudinary.api.resources(
    type="upload",
    resource_type="image",
    prefix="my_photo_uploads",
    tags=True,
    max_result=100
  )
  all_resources.extend(response['resources'])
  next_cursor = 
  print(response)

get_images_with_tags()