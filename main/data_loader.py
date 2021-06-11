import csv
import os
import django
import logging

from django.db import IntegrityError, transaction

from BannerService.settings import BASE_DIR


def load(csv_dir='csv'):
    logger = logging.getLogger("data_loader")
    # to use models we should set this environment first
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BannerService.settings")
    django.setup()

    from main.models import Click, Impression, Conversion

    data = {
        Click: os.path.join(BASE_DIR, csv_dir, '{}/clicks_{}.csv'),
        Impression: os.path.join(BASE_DIR, csv_dir, '{}/impressions_{}.csv'),
        Conversion: os.path.join(BASE_DIR, csv_dir, '{}/conversions_{}.csv')
    }

    for quarter in range(1, 5):
        for model, path in data.items():
            with open(path.format(quarter, quarter), 'r') as fin:
                dr = csv.DictReader(fin)
                for record in dr:
                    try:
                        with transaction.atomic():
                            model.objects.create(quarter=quarter, **record)
                    except IntegrityError as error:
                        logger.warning(f"Duplicate record found: quarter={quarter}, {record}")


if __name__ == '__main__':
    load()
