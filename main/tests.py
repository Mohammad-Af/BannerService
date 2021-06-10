import os

from django.test import TestCase

from django.urls import reverse
import datetime
import subprocess
import shutil

from BannerService.settings import BASE_DIR
from main.data_loader import load
from main.models import Click, Conversion


class ServeBannerTest(TestCase):
    def setUp(self):
        self.quarter = 1 + (datetime.datetime.now().minute // 15)

    def test_scenario_1(self):  # test for X > 10
        for i in range(200):
            Click(click_id=i,
                  banner_id=i % 20,
                  campaign_id=1,
                  quarter=self.quarter).save()

        for i in range(200):
            Conversion(conversion_id=i,
                       click_id=i,
                       revenue=i,
                       quarter=self.quarter).save()

        response = self.client.get(reverse('serve_banners', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['banners']),
                         set([f'/images/image_{i}.png' for i in range(10, 20)]))

    def test_scenario_2(self):  # test for 10 > X >= 5
        for i in range(100):
            Click(click_id=i,
                  banner_id=i % 20,
                  campaign_id=1,
                  quarter=self.quarter).save()

        for i in range(6):
            Conversion(conversion_id=i,
                       click_id=i,
                       revenue=i,
                       quarter=self.quarter).save()

        response = self.client.get(reverse('serve_banners', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['banners']),
                         set([f'/images/image_{i}.png' for i in range(6)]))

    def test_scenario_3(self):  # test for 5 > X >= 1
        for i in range(12):
            Click(click_id=i,
                  banner_id=i % 7,
                  campaign_id=1,
                  quarter=self.quarter).save()

        for i in range(2):
            Conversion(conversion_id=i,
                       click_id=i,
                       revenue=i,
                       quarter=self.quarter).save()

        response = self.client.get(reverse('serve_banners', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['banners']),
                         set([f'/images/image_{i}.png' for i in range(5)]))

    def test_scenario_4(self):  # test for X = 0
        for i in range(12):
            Click(click_id=i,
                  banner_id=i % 7,
                  campaign_id=1,
                  quarter=self.quarter).save()

        response = self.client.get(reverse('serve_banners', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.context['banners']),
                         set([f'/images/image_{i}.png' for i in range(5)]))

    def test_scenario_4_random_banner(self):  # test for X = 0
        for i in range(12):
            Click(click_id=i,
                  banner_id=i,
                  campaign_id=i,
                  quarter=self.quarter).save()

        response = self.client.get(reverse('serve_banners', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(set(response.context['banners'])), 5)


class DataInsertionTest(TestCase):
    #
    # os.path.join(BASE_DIR, csv_dir, '{}/clicks_{}.csv')
    #    os.path.join(BASE_DIR, csv_dir, '{}/impressions_{}.csv')
    # os.path.join(BASE_DIR, csv_dir, '{}/conversions_{}.csv')
    # def setUP(self):
    #     self.remove_files(os.path.join(BASE_DIR, 'test'))

    def create_files(self):
        files = {
            'clicks_{}.csv': 'click_id,banner_id,campaign_id\n',
            'conversions_{}.csv': 'conversion_id,click_id,revenue\n',
            'impressions_{}.csv': 'banner_id,campaign_id\n'
        }
        for i in range(1, 5):
            directory = os.path.join(BASE_DIR, f'test/{i}')
            os.makedirs(directory)
            for fname, header in files.items():
                f = open(os.path.join(directory, fname.format(i)), 'w')
                f.write(header)
                f.close()

    def remove_files(self, directory):
        if os.path.exists(directory):
            shutil.rmtree(directory)

    def test_normal_record(self):
        self.create_files()
        f = open(os.path.join(BASE_DIR, 'test/1/clicks_1.csv'), "a")
        f.write('1,1,1\n')
        f.write('2,2,2\n')
        f.write('3,3,3\n')
        f.close()
        load('test')
        self.assertEqual(Click.objects.count(), 3)
        self.remove_files(os.path.join(BASE_DIR, 'test'))

    def test_duplicate_record(self):
        self.create_files()
        f = open(os.path.join(BASE_DIR, 'test/1/clicks_1.csv'), "a")
        f.write('1,1,1\n')
        f.write('2,2,2\n')
        f.write('1,1,1\n')
        f.close()
        load('test')
        self.assertEqual(Click.objects.count(), 2)
        self.remove_files(os.path.join(BASE_DIR, 'test'))
