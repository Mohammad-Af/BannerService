#!/bin/bash
wget 'https://mohammad-minitest.s3.us-east-2.amazonaws.com/banner_images.zip'
unzip banner_images.zip
wget 'https://mohammad-minitest.s3.us-east-2.amazonaws.com/csv.zip'
unzip csv.zip
python manage.py makemigrations
python manage.py migrate
python main/data_loader.py
python manage.py runserver 0.0.0.0:8000 & celery -f celery.worker.log -A BannerService worker --beat -l info