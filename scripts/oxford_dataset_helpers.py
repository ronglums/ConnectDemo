
import shutil, tarfile, os, shutil, re
from os.path import basename, isfile
from urllib.parse import urlparse
from urllib.request import urlopen
from pathlib import Path

# Fetch a file from uri, unzip and untar it into its own directory.
def fetch_and_untar(uri):
    # Parse the uri to extract the local filename
    parsed_uri = urlparse(uri)
    local_filename = basename(parsed_uri.path)

    # If file is not already on disk, retrieve from uri
    if not isfile(local_filename):
        with urlopen(uri) as response:
            with open(local_filename, 'bw+') as f:
                shutil.copyfileobj(response, f)

    # Expand the archive
    with tarfile.open(local_filename) as tar:
        
        import os
        
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)
        
# The script below will rearrange the files so that all of the photos for a specific breed of dog 
# or cat will be stored in its own directory, where the name of the directory is the name of the
# pet's breed.
def move_images_into_labelled_directories(image_dir):
    images_path = Path(image_dir)
    extract_breed_from_filename = re.compile(r'([^/]+)_\d+.jpg$')

    for filename in os.listdir('images'):
        print(filename)
        match = extract_breed_from_filename.match(filename)
        if match is not None:
            breed = match.group(1)
            if not os.path.exists(images_path / breed):
                os.makedirs(images_path / breed)
            src_path = images_path / filename
            dest_path = images_path / breed / filename
            shutil.move(src_path, dest_path)
            
