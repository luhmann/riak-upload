Install system dependencies:

`brew install python libmagic libtiff libjpeg webp little-cms2`

Install python packages:

`pip install -r requirements.txt`

Put the image files you want to upload in `img`-folder (or specify folder on execution)

`python riakUpload.py`

Flags are:

  `--destRiak="<ip>"` - the ip or hostname of the riak you want to push to

  `--imgFolder="<name>"` - the path of the image folder, relative of the script-folder
