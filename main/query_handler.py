from main.models import Conversion, Click
import random


def calculate_x(campaign_id, quarter):
    return Conversion.objects.raw(f'''
                select campaign_id as id, count(distinct banner_id) as X
                from main_conversion mcv
                         join main_click mcl
                              on mcv.click_id = mcl.click_id
                where mcv.quarter = {quarter}
                  and mcl.quarter = {quarter}
                  and campaign_id = {campaign_id}''')[0].X


def get_top_banners_by_conversion(campaign_id, quarter, count):
    res = Conversion.objects.raw(f'''
                        select banner_id as id
                        from main_conversion mcv
                                 join main_click mcl
                                      on mcv.click_id = mcl.click_id
                        where mcv.quarter = {quarter}
                          and mcl.quarter = {quarter}
                          and campaign_id = {campaign_id}
                        group by banner_id
                        order by sum(revenue) desc
                        limit {count}''')
    return list(map(lambda x: x.id, res))


def get_top_banners_by_click(campaign_id, quarter, count):
    res = Click.objects.raw(f'''select banner_id as id
                            from main_click
                            where quarter = {quarter}
                              and campaign_id = {campaign_id}
                            group by banner_id
                            order by count(*) desc
                            limit {count}''')
    return list(map(lambda x: x.id, res))


def get_random_banner(quarter):
    result = Click.objects.filter(quarter=quarter)
    index = random.randint(0, result.count() - 1)
    return result[index].banner_id
