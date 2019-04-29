# Upload records to GFW API

# Installation

`pip install git+https://github.com/wri/upload_records.git`

# concatenate records to existing dataset

`concatenate_record DATASET BUCKET [--prefix FILEPREFIX] [--filetype FILEXTENTION]`

This tool will try to concatenate all files in bucket with given prefix and file extention to dataset.
It will try to concatenate until API confirms import with a 204.

