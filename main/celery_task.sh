#!/bin/bash
rm banner_images.zip
rm csv.zip
rm wget-log*
wget 'https://mohammad-minitest.s3.us-east-2.amazonaws.com/banner_images.zip'
unzip -o banner_images.zip
wget 'https://mohammad-minitest.s3.us-east-2.amazonaws.com/csv.zip'
unzip -o csv.zip
export PYTHONPATH=./
python main/data_loader.py