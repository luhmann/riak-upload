import argparse
import os
import json
import base64
import magic
import StringIO
from PIL import Image
from riak import RiakClient, RiakNode

parser = argparse.ArgumentParser(description='Takes a list of urls and ')
parser.add_argument('--destRiak', dest='dest_riak', default='10.228.39.181', help='The host we push the riak data')
parser.add_argument('--imgFolder', dest='input_folder', default='img', help='The input folder that contains the images we want to push')
args = parser.parse_args()

# map arguments
dest_riak_host = args.dest_riak

base_dir = os.path.dirname(os.path.realpath(__file__))
input_dir = os.path.join(base_dir, args.input_folder)

# connect to live riak
riak_connection = RiakClient(protocol='http', host=dest_riak_host, http_port=8098)
riak_bucket = riak_connection.bucket('ez')

# save image in integration riak
def saveToRiak(key, json):
  img = riak_bucket.new(key, encoded_data=json)
  img.store()

# get and save all images
for img in os.listdir(input_dir):
  img_path = os.path.join(input_dir, img)
  print 'Uploading %s' % img_path
  im = Image.open(img_path)
  mime = magic.Magic(mime=True)
  mime_type = mime.from_file(img_path)
  output = StringIO.StringIO()
  im.save(output, 'JPEG')
  json_repr = {
    'id': img,
    'title': img,
    'size': str(os.path.getsize(img_path)),
    'width': str(im.size[0]),
    'height': str(im.size[1]),
    'mimeType': mime_type,
    'imageBinary': base64.b64encode(output.getvalue()),
    'type': 'image'
  }
  output.close()

  saveToRiak(img, json.dumps(json_repr))
