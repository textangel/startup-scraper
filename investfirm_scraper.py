"""
The following code scrapes investment information in China from popular venture capital
investment aggregator ITJuzi.com. It successfully obtains all historical investment data for ~7000
investment funds and stores the information in MongoDB.
The user must first set up a MongoDB instance and create a database called ITjuzi.
Cookies have been redacted for privacy reasons but you may put your own browser cookies in the code
to experiment.

"""

# -*- coding: utf-8 -*-
# Source: #Source website: https://www.makcyun.top/web_scraping_withpython7.html#more
import pymongo
import time
from fake_useragent import UserAgent
import socket  # 断线重试
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

# 随机ua
ua = UserAgent()
# mongodb数据库初始化
client = pymongo.MongoClient('localhost', 27017)
# 获得数据库
db = client.ITjuzi
# 获得集合
import requests

cookies = {
    'acw_tc': '781bad0615506315578642175e01e284fd58f011855246a37b57f67e88c1a4',
    'gr_user_id': 'd9ca1f69-2205-4772-8852-56cc8ed685a8',
    '_ga': 'GA1.2.1180394379.1550739279',
    'MEIQIA_VISIT_ID': '1ILAVuFFs0UCLU7rY3bp0SxfFpB',
    'juzi_user': '660423',
    '_gid': 'GA1.2.173669602.1552832184',
    'juzi_token': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3Lml0anV6aS5jb21cL2FwaVwvdXNlcnNcL3VzZXJfaGVhZGVyX2luZm8iLCJpYXQiOjE1NTI1NjY3NjEsImV4cCI6MTU1MjgzNTc4NCwibmJmIjoxNTUyODMyMTg0LCJqdGkiOiJncTlYQ3UycTVCSGppMnZqIiwic3ViIjo2NjA0MjMsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.Dtis4kfCFDDWvL2uqKtavjgw8Sp7WukYhqfn0oUsZNI',
    'Hm_lvt_1c587ad486cdb6b962e94fc2002edf89': '1551787316,1552318576,1552715067,1552832189',
    'gr_session_id_eee5a46c52000d401f969f4535bdaa78': '58eccb2c-7e7e-4d77-a625-cc52105a2e2f',
    'gr_session_id_eee5a46c52000d401f969f4535bdaa78_58eccb2c-7e7e-4d77-a625-cc52105a2e2f': 'true',
    '_gat_gtag_UA_59006131_1': '1',
    'Hm_lpvt_1c587ad486cdb6b962e94fc2002edf89': '1552835182',
}

headers = {
    'Pragma': 'no-cache',
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,es-419;q=0.8,es;q=0.7,zh-CN;q=0.6,zh;q=0.5,ja;q=0.4',
    'CURLOPT_FOLLOWLOCATION': 'true',
    'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczpcL1wvd3d3Lml0anV6aS5jb21cL2FwaVwvdXNlcnNcL3VzZXJfaGVhZGVyX2luZm8iLCJpYXQiOjE1NTI1NjY3NjEsImV4cCI6MTU1MjgzNTc4NCwibmJmIjoxNTUyODMyMTg0LCJqdGkiOiJncTlYQ3UycTVCSGppMnZqIiwic3ViIjo2NjA0MjMsInBydiI6IjIzYmQ1Yzg5NDlmNjAwYWRiMzllNzAxYzQwMDg3MmRiN2E1OTc2ZjcifQ.Dtis4kfCFDDWvL2uqKtavjgw8Sp7WukYhqfn0oUsZNI',
    'Accept': 'application/json, text/plain, */*',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
    'Connection': 'keep-alive',
    'Referer': 'https://www.itjuzi.com/investfirm/1',
}

class itjuzi_scraper(object):

    def __init__(self):
        self.session = requests.Session()
        self.retry_times = 3
        self.sleep_time = 0.2

    def get_page(self, id, page):
        """
        1 获取投融资事件网页内容
        """
        params = (
            ('id', str(id)),
            ('page', str(page)),
        )

        retrytimes = self.retry_times
        while retrytimes:
            try:
                response = self.session.get('https://www.itjuzi.com/api/search', headers=headers, params=params,
                                             cookies=cookies)
                return response
            except socket.timeout:
                print('下载id{}第{}页，第{}次网页请求超时'.format(id, page, retrytimes))
                retrytimes -= 1
        return None

    def get_all_pages(self,id,numpages):
        items = {}
        for page in range(1,numpages+1):
            response = self.get_page(id, page)
            if response is not None:
                rsp_json = response.json()["data"]
                if "page" in rsp_json.keys():
                    del rsp_json["page"]
                for k,v in rsp_json.items():
                    items[str(int(str(page - 1) + k))] = v
                print("Processed {} pages".format(page))
            time.sleep(self.sleep_time)
        self.save_to_file("test.txt", items)
        return items

    def get_address(self, id):
        retrytimes = self.retry_times
        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/invst_left_info/' + str(id), headers=headers, cookies=cookies)
                rsp_json = response.json()
                rsp_json = rsp_json["data"]["address"]
                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_num_pages(self, id):
        params = (
            ('id', str(id)),
            ('page', '1'),
        )

        retrytimes = self.retry_times
        while retrytimes:
            try:
                response = self.session.get('https://www.itjuzi.com/api/search', headers=headers, params=params,
                                             cookies=cookies)
                rsp_json = response.json()
                rsp_json=rsp_json["data"]["page"]["totalPages"]
                return int(rsp_json)
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_graph_data(self, id):
        retrytimes = self.retry_times
        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/investment_record_infos/'+str(id), headers=headers,
                                        cookies=cookies)
                rsp_json = response.json()
                rsp_json=rsp_json["data"]
                rsp_json = {k : v for k,v in rsp_json.items() if k in ["y_right_arr", "y_left_arr", "x_arr"]}
                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_sector_data(self, id):
        params = (
            ('type', 'all'),
        )
        retrytimes = self.retry_times
        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/investment_records/'+str(id), headers=headers,
                                        cookies=cookies, params=params)
                rsp_json = response.json()
                rsp_json=rsp_json["data"]
                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_coinvest_data(self, id):
        params = (
            ('id', str(id)),
        )
        retrytimes = self.retry_times

        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/invst_news_info', headers=headers, params=params,
                                        cookies=cookies)
                rsp_json = response.json()
                rsp_json=rsp_json["data"]
                for key in ["invst_news_info", "financing_consultant", "invst_person_info"]:
                    if key in rsp_json.keys():
                        del rsp_json[key]
                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_basic_info(self, id):
        retrytimes = self.retry_times

        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/investments/'+str(id), headers=headers, cookies=cookies)
                rsp_json = response.json()
                rsp_json=rsp_json["data"]
                rsp_json = {k: v for k, v in rsp_json.items() if k in ["name","des","year","num","id","single_investment_scale","investment_round"]}

                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))

    def get_partners_data(self):

        retrytimes = self.retry_times

        while retrytimes:
            try:
                response = requests.get('https://www.itjuzi.com/api/get_invst_person_detail/1', headers=headers,
                                        cookies=cookies)
                rsp_json = response.json()
                rsp_json = rsp_json["data"]
                rsp_json = {k: v for k, v in rsp_json.items() if
                            k in ["name", "des", "year", "num", "id", "single_investment_scale", "investment_round"]}

                return rsp_json
            except socket.timeout:
                print('下载id{}，第{}次网页请求超时'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))


    def save_to_file(self, path, data):
        with open(path, "w+") as f:
            f.write(str(data))



    def compile_data(self,id):
        data = {}
        data["summary_data"] = {}
        data["basic_info"] = self.get_basic_info(id)
        data["basic_info"]["address"] = self.get_address(id)
        data["summary_data"]["graph_data"] = self.get_graph_data(id)
        data["summary_data"]["sector_data"] = self.get_sector_data(id)
        data["coinvest_data"] = self.get_coinvest_data(id)
        numpages = self.get_num_pages(id)
        data["all_investments"] = self.get_all_pages(id, numpages)
        return data

    def save_to_mongo(self, database, data, id):
        try:
            data['_id'] = str(id)
            if database.insert_one(data):
                print('存储id{}到mongodb成功'.format(id))
        except Exception as e:
            print('存储id{}到mongodb失败. Error: {}'.format(id, str(e)))


if __name__ == '__main__':
    import ast
    import os
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    abs_file_path = os.path.join(script_dir, "files/idlist.txt")

    spider = itjuzi_scraper()
    start_id = 1571
    with open(abs_file_path, "r") as f:
        str_list = f.read()
        id_list = ast.literal_eval(str_list)
        id_list.sort()

    id_list = [id for id in id_list if id >= start_id]
    for id in id_list:
        try:
            data = spider.compile_data(id)
            spider.save_to_mongo(db.investfirm_detail, data, id)
        except Exception as e:
            print('存储id{}到mongodb失败. Error: {}'.format(id, str(e)))
