"""
The following code scrapes investment information in China from popular venture capital
investment aggregator ITJuzi.com. It successfully obtains all historical investment data for ~7000
investment funds and stores the information in MongoDB.
The user must first set up a MongoDB instance and create a database called ITjuzi.
Cookies have been redacted for privacy reasons but you may put your own browser cookies in the code
to experiment.

"""

# -*- coding: utf-8 -*-
# Source:
import pymongo
import time
from fake_useragent import UserAgent
import socket 
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

ua = UserAgent()
client = pymongo.MongoClient('localhost', 27017)
db = client.ITjuzi
import requests

cookies = {
    """"":"""""
}

headers = {
     """"":"""""
    'Referer': 'https://www.itjuzi.com/investfirm/1',
}

class itjuzi_scraper(object):

    def __init__(self):
        self.session = requests.Session()
        self.retry_times = 3
        self.sleep_time = 0.2

    def get_page(self, id, page):
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
                print('Downloaded id{}，Retry attempt {}'.format(id, page, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
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
                print('Save to mongo id{} succeeded'.format(id))
        except Exception as e:
            print('Save to mongo id{} failed. Error: {}'.format(id, str(e)))


if __name__ == '__main__':
    import ast
    import os
    script_dir = os.path.dirname(__file__) 
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
            print('Save to mongo id{} failed. Error: {}'.format(id, str(e)))
