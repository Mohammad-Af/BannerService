import csv
import os
import django

# to use models we should set this environment first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BannerService.settings")
django.setup()

from main.models import Click, Impression, Conversion

data = {
    Click: 'csv/{}/clicks_{}.csv',
    Impression: 'csv/{}/impressions_{}.csv',
    Conversion: 'csv/{}/conversions_{}.csv'
}

for quarter in range(1, 5):
    for model, path in data.items():
        with open(path.format(quarter, quarter), 'r') as fin:
            dr = csv.DictReader(fin)
            for record in dr:
                try:
                    model.objects.create(quarter=quarter, **record)
                except django.db.utils.IntegrityError as error:
                    # log record is already in database
                    pass

