#!/usr/bin/env python3

import os
import sys
from docopt import docopt
import json
import magic

DEFAULT_BASE_URL = "http://localhost:8080/"


__doc__ = """Usage: {0} [options]

Options:
-c, --clobber                    Allow overwriting of existing files
-h, --help                       This help
-v, --version                    Print version and exit
-r, --images-root=<path>         Where the original images are
                                 [DEFAULT: .]
-t, --thumbs-root=<path>         Where the thumbnails are
                                 [DEFAULT: thumbs]
-T, --thumbs-root-in-href=<path> How an index....html file should refer to
                                 the thumbnail root.
                                 [DEFAULT: thumbs]
-i, --index-root=<path>          Where the index_....html files will be created
                                 [DEFAULT: .]
-b, --base-url=<url>             All images and indices will have <url> at the beginning
                                 [DEFAULT: {1}]
""".format(sys.argv[0], DEFAULT_BASE_URL)


def main_index(indices):
  yield """
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1, maximum-scale=1">

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

    <link href="https://unpkg.com/nanogallery2/dist/css/nanogallery2.min.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="https://unpkg.com/nanogallery2/dist/jquery.nanogallery2.min.js"></script>

    <style>
.myButton {
  box-shadow:inset 0px 1px 0px 0px #9acc85;
  background:linear-gradient(to bottom, #74ad5a 5%, #68a54b 100%);
  background-color:#74ad5a;
  border:1px solid #3b6e22;
  display:inline-block;
  cursor:pointer;
  color:#ffffff;
  font-family:Arial;
  font-size:13px;
  font-weight:bold;
  padding:6px 12px;
  text-decoration:none;
  margin: .2em;
}
.myButton:hover {
  background:linear-gradient(to bottom, #68a54b 5%, #74ad5a 100%);
  background-color:#68a54b;
}
.myButton:active {
  position:relative;
  top:1px;
}
</style>
  </head>
  <body>
  <h1>Albums</h1>
  <ul>
  """

  for index in indices:
    yield f'<li><a class="myButton" href="{index}">{os.path.splitext(index.split("index_")[1])[0]}</a></li>\n'


  yield "</ul></body></html>"


def index_html(file_and_thumb_names, thumbs_root_in_href, title, *, videos=False, indexv_name="",
    indexi_name="", itemsBaseURL=DEFAULT_BASE_URL):
  fats = file_and_thumb_names
  trih = thumbs_root_in_href

  yield """
<html>
  <head>
    <meta name="viewport" content="user-scalable=no, width=device-width, initial-scale=1, maximum-scale=1">

    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.1/jquery.min.js"></script>

    <link href="https://unpkg.com/nanogallery2/dist/css/nanogallery2.min.css" rel="stylesheet" type="text/css">
    <script type="text/javascript" src="https://unpkg.com/nanogallery2/dist/jquery.nanogallery2.min.js"></script>

    <style>
.myButton {{
  box-shadow:inset 0px 1px 0px 0px #9acc85;
  background:linear-gradient(to bottom, #74ad5a 5%, #68a54b 100%);
  background-color:#74ad5a;
  border:1px solid #3b6e22;
  display:inline-block;
  cursor:pointer;
  color:#ffffff;
  font-family:Arial;
  font-size:13px;
  font-weight:bold;
  padding:6px 12px;
  text-decoration:none;
  margin: .2em;
}}
.myButton:hover {{
  background:linear-gradient(to bottom, #68a54b 5%, #74ad5a 100%);
  background-color:#68a54b;
}}
.myButton:active {{
  position:relative;
  top:1px;
}}
</style>

  </head>
  <body>
  <h1>{0}</h1>
  <div id="gallery_div"></div>

  <a class="myButton" href="index.html">Index</a>
  """.format(title)

  if not videos and indexv_name != "" and os.path.exists(indexv_name):
    yield f'<a class="myButton" href="{indexv_name}">Videos</a>\n'

  if videos and indexi_name != "" and os.path.exists(indexi_name):
    yield f'<a class="myButton" href="{indexi_name}">Images</a>\n'

  yield """
  <script>

jQuery(document).ready(function () {
  jQuery("#gallery_div").nanogallery2(
  """

  items = {
    "items":[
    ],
    "thumbnailWidth":  "auto",
    "thumbnailHeight": 170,
    "itemsBaseURL":    itemsBaseURL,
    "locationHash":    False,
    "galleryDisplayMode": "pagination",
    "thumbnailAlignment": "justified",
  }

  max_per_gal = 40

  offsets = [x for x in range(0, len(fats) + max_per_gal, max_per_gal)]

  for offset in offsets:
    gal_num = (offset / max_per_gal) + 1
    beg = offset
    end = offset + max_per_gal
    last = min(len(fats), end)
    if beg >= len(fats):
      continue

    items["items"].append({"src":   fats[offset]["filename"], "srct":  trih + "/" + fats[offset]["thumb_filename"], "title": f'{beg + 1} - {last}', "ID": gal_num, "kind": 'album'})
    for i in range(beg, last):
      items["items"].append({"src": fats[i]["filename"], "srct": trih + "/" + fats[i]["thumb_filename"], "title": str(i + 1), "ID": 100 + i, "albumID": gal_num})

  yield json.dumps(items, indent=2, separators=(',', ': '))

  yield ");})</script></body></html>"


def is_an_image(path):
  return (magic.from_file(path, mime=True).split("/")[0] == "image")


def is_a_video(path):
  return (magic.from_file(path, mime=True).split("/")[0] == "video")


def is_a_video_thumbnail(path):
  filename = os.path.basename(path)
  return filename.startswith("tv-") and filename.endswith(".jpg")


def is_an_image_thumbnail(path):
  filename = os.path.basename(path)
  return filename.startswith("t-")


def video_thumbnails_in(filenames):
  return [
    filename
    for filename in filenames
    if is_a_video_thumbnail(filename)
  ]


def image_thumbnails_in(filenames):
  return [
    filename
    for filename in filenames
    if is_an_image_thumbnail(filename)
  ]


def midsize_basename_from_thumb_basename(image_basename):
  """
  I've converted images with just blah.jpg -> t-blah.jpg
                                  blah.png -> t-blah.png
                                  etc.
                              and blah.jpg -> t600-blah.jpg
                                  blah.png -> t600-blah.png
  Not handling videos yet
  """
  if is_an_image_thumbnail(image_basename):

    # Cut off the t- and insert a t600-
    return "t600-" + image_basename[2:]
  return None


def image_basename_from_thumb_basename(image_basename):
  """
  I've converted images with just blah.jpg -> t-blah.jpg
                                  blah.png -> t-blah.png
                                  etc.
  But there's no canonical image thing for videos, so I converted
  them very explicitly with blah.mp4 -> tv-blah.mp4.jpg
  """
  if is_a_video_thumbnail(image_basename):

    # Cut off the tv- and .jpg
    return image_basename[3:-4]
  elif is_an_image_thumbnail(image_basename):

    # Cut off the t-
    return image_basename[2:]


def main():
  args = docopt(__doc__, version="1.0.0")

  thumbs_root = os.path.normpath(args["--thumbs-root"])
  thumbs_root_in_href = args["--thumbs-root-in-href"]
  images_root = os.path.normpath(args["--images-root"])
  clobber = args["--clobber"]
  index_root = args["--index-root"]
  base_url = args["--base-url"]

  created_indices = make_indices(thumbs_root, images_root, thumbs_root_in_href,
      index_root, clobber=clobber, itemsBaseURL=base_url)

  if os.path.exists("index.html") and not clobber:
    print("Not clobbering index.html")
    exit(0)

  print("Writing index.html")
  with open("index.html", "w") as f:
    for line in main_index(sorted(created_indices)):
      f.write(line)


def unroot(*, root_path, full_path):
  """
  >>> unroot(root_path="/a/b", full_path="/a/b/c/d/e")
  'c/d/e'

  Trailing / on root_path is optional

  >>> unroot(root_path="/a/b/", full_path="/a/b/c/d/e")
  'c/d/e'

  If no common root, return `None`

  >>> unroot(root_path="a/b/", full_path="/a/b/c/d/e") == None
  True
  >>> unroot(root_path="a/b/", full_path="a/b/c/d/e")
  'c/d/e'
  >>> unroot(root_path="b/", full_path="a/b/c/d/e") == None
  True

  This shouldn't be so hard.
  """
  root_path_parts = root_path.split(os.path.sep)

  # Ignore possible trailing /
  if root_path_parts[-1] == "":
    root_path_parts.pop(-1)

  full_path_parts = full_path.split(os.path.sep)

  # If they don't begin with the same stuff, have no idea what's going on
  if full_path_parts[0: len(root_path_parts)] != root_path_parts:
    return None

  rootless_parts = full_path_parts[len(root_path_parts):]

  return os.path.join(*rootless_parts)


def make_indices(thumbs_root, images_root, thumbs_root_in_href,
    index_root, clobber=False, *, itemsBaseURL):
  created_indices = []

  for (curdir, subdirs, filenames) in os.walk(thumbs_root, topdown=True):
    if len(filenames) > 0:
      rootless = unroot(full_path=curdir, root_path=thumbs_root)

      # If they don't begin with the same stuff, have no idea what's going on
      if rootless == None:
        print(f"Real error: {curdir} doesn't begin with {thumbs_root}")
        exit(1)

      cur_images_dir = os.path.join(images_root, rootless)

      rootless_parts = rootless.split(os.path.sep)

      cur_index_filename = os.path.join(index_root, "_".join(["index"] + rootless_parts)) + ".html"
      cur_indexv_filename = os.path.join(index_root, "_".join(["indexv"] + rootless_parts)) + ".html"

      # # Creating video indices first because want a link to them on images pages
      # # only if they exist

      # # Videos
      # filenames = video_thumbnails_in(filenames)
      # if len(filenames) > 0:
      #   if os.path.isfile(cur_indexv_filename) and not clobber:
      #     print(f"{cur_indexv_filename} already exists.  Not clobbering")
      #     continue

      #   print(f"Creating {cur_indexv_filename}")
      #   fats = []
      #   for filename in filenames:
      #     fats.append(
      #       {
      #         "filename": os.path.join(rootless, image_basename_from_thumb_basename(filename)),
      #         "thumb_filename": os.path.join(rootless, filename)
      #       }
      #     )
      #   with open(cur_indexv_filename, 'w') as f:
      #     for line in index_html(fats, thumbs_root_in_href, rootless, videos=True,
      #         indexi_name=cur_index_filename):
      #       f.write(line)

      #   # Video indices will just be discoverable from image pages
      #   # created_indices.append(cur_indexv_filename)


      # Images
      filenames = image_thumbnails_in(filenames)
      if len(filenames) > 0:
        if os.path.isfile(cur_index_filename) and not clobber:
          print(f"{cur_index_filename} already exists.  Not clobbering")
          continue

        print(f"Creating {cur_index_filename}")
        fats = []
        for filename in filenames:

          # If there's a midsize file, use that as the main image
          midsize_filename = midsize_basename_from_thumb_basename(filename)
          midsize_path = os.path.join(rootless, midsize_filename)
          if os.path.isfile(midsize_path):
            image_path = midsize_path
          else:
            image_path = os.path.join(rootless, image_basename_from_thumb_basename(filename))


          fats.append(
            {
              "filename": image_path,
              "thumb_filename": os.path.join(rootless, filename)
            }
          )
        with open(cur_index_filename, 'w') as f:
          for line in index_html(fats, thumbs_root_in_href, rootless, indexv_name=cur_indexv_filename,
              itemsBaseURL=DEFAULT_BASE_URL):
            f.write(line)
        created_indices.append(cur_index_filename)

  return tuple([os.path.normpath(d) for d in created_indices])


if __name__ == "__main__":
  main()
