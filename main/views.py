from django.shortcuts import render

from BannerService.settings import MEDIA_URL
import os
import datetime
import random

from main.query_handler import calculate_x, get_top_banners_by_conversion, get_top_banners_by_click, get_random_banner


def get_banner_image_name(banner):
    return os.path.join(MEDIA_URL, 'image_' + str(banner) + '.png')


def get_banners(campaign_id):
    quarter = 1 + (datetime.datetime.now().minute // 15)  # calculate current hour quarter
    X = calculate_x(campaign_id, quarter)
    if X > 5:
        count = min(10, X)
        return get_top_banners_by_conversion(campaign_id, quarter, count)
    if 0 < X <= 5:
        top_by_conversions = get_top_banners_by_conversion(campaign_id, quarter, X)
        # here we get first 5 banners by clicks to make sure the combination with conversion banners will be unique
        top_by_clicks = get_top_banners_by_click(campaign_id, quarter, 5)
        # we get 5 banners including those are in top_by_conversions
        while len(top_by_conversions) < 5:
            item = top_by_clicks.pop()
            if item not in top_by_conversions:
                top_by_conversions.append(item)
        return top_by_conversions
    if X == 0:
        top_by_clicks = get_top_banners_by_click(campaign_id, quarter, 5)
        cnt = len(top_by_clicks)
        if cnt < 5:
            while len(top_by_clicks) < 5:
                random_banner = get_random_banner(quarter)
                if random_banner not in top_by_clicks:
                    top_by_clicks.append(random_banner)
        return top_by_clicks


def serve_banners(request, campaign_id):
    if request.method == 'GET':
        banners = get_banners(campaign_id)
        random.shuffle(banners)
        banners_url = [get_banner_image_name(banner)
                       for banner in banners]
        return render(request, 'campaign.html',
                      context={"banners": banners_url})
