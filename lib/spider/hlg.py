#!/usr/bin/env python
# coding=utf-8
# 爬取回龙观周边小区数据的爬虫派生类

import re
from bs4 import BeautifulSoup
from lib.item.xiaoqu import *
from lib.zone.city import get_city
from lib.spider.base_spider import *
from lib.utility.date import *
from lib.utility.path import *
from lib.zone.area import *
from lib.utility.log import *
import lib.utility.version
from lib.utility.torhttp import *


class HLGBaseSpider(BaseSpider):
    def collect_area_xiaoqu_data(self, city_name, area_name, fmt="csv"):
        """
        对于每个板块,获得这个板块下所有小区的信息
        并且将这些信息写入文件保存
        :param city_name: 城市
        :param area_name: 板块
        :param fmt: 保存文件格式
        :return: None
        """
        district_name = area_dict.get(area_name, "")
        csv_file = self.today_path + "/{0}.csv".format("huilongguan2")
        with open(csv_file, "w") as f:
            # 开始获得需要的板块数据
            xqs = self.get_xiaoqu_info("bj", "huilongguan2")
            # 锁定
            if self.mutex.acquire(1):
                self.total_num += len(xqs)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for xiaoqu in xqs:
                    f.write(self.date_string + "," + xiaoqu.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
        logger.info("Finish crawl area: " + area_name + ", save data to : " + csv_file)

    @staticmethod
    def get_xiaoqu_info(city, area):
        total_page = 1
        district = area_dict.get(area, "")
        chinese_district = get_chinese_district(district)
        chinese_area = chinese_area_dict.get(area, "")
        xiaoqu_list = list()
        page = 'http://{0}.{1}.com/xiaoqu/{2}/'.format(city, SPIDER_NAME, area)
        print(page)
        logger.info(page)

        headers = create_headers()
        response = requests.get(page, timeout=10, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, "lxml")

        # 获得总的页数
        try:
            page_box = soup.find_all('div', class_='page-box')[0]
            matches = re.search('.*"totalPage":(\d+),.*', str(page_box))
            total_page = int(matches.group(1))
        except Exception as e:
            print("\tWarning: only find one page for {0}".format(area))
            print(e)

        # 从第一页开始,一直遍历到最后一页
        for i in range(1, total_page + 1):
            headers = create_headers()
            page = 'http://{0}.{1}.com/xiaoqu/{2}/pg{3}'.format(city, SPIDER_NAME, area, i)
            print(page)  # 打印版块页面地址
            BaseSpider.random_delay()
            response = requests.get(page, timeout=10, headers=headers)
            html = response.content
            soup = BeautifulSoup(html, "lxml")

            # 获得有小区信息的panel
            house_elems = soup.find_all('li', class_="xiaoquListItem")
            for house_elem in house_elems:
                price = house_elem.find('div', class_="totalPrice")
                name = house_elem.find('div', class_='title')
                on_sale = house_elem.find('div', class_="xiaoquListItemSellCount")

                # 继续清理数据
                price = price.text.strip()
                name = name.text.replace("\n", "")
                on_sale = on_sale.text.replace("\n", "").strip()

                # 作为对象保存
                xiaoqu = XiaoQu(chinese_district, chinese_area, name, price, on_sale)
                xiaoqu_list.append(xiaoqu)
        return xiaoqu_list

    def start(self):
        self.today_path = create_date_path("{0}/hlg".format(SPIDER_NAME), "bj", self.date_string)
        t1 = time.time()  # 开始计时
        self.collect_area_xiaoqu_data(self,"bj","huilongguan2")

        # 计时结束，统计结果
        t2 = time.time()
        print("Total cost {0} second to crawl {1} data items.".format(t2 - t1, self.total_num))
