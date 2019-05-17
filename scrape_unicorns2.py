"""
The following code scrapes investment information in China from popular venture capital
investment aggregator ITJuzi.com. It successfully obtains all historical investment data for ~7000
investment funds and stores the information in MongoDB.
The user must first set up a MongoDB instance and create a database called ITjuzi.
Cookies have been redacted for privacy reasons but you may put your own browser cookies in the code
to experiment.

"""

# -*- coding: utf-8 -*-
import pymongo
import time
from fake_useragent import UserAgent
import socket
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import pandas as pd

ua = UserAgent()
client = pymongo.MongoClient('localhost', 27017)
db = client.ITjuzi
import requests

cookies = {

}

headers = {
    
}


class Unicorn:
    def __init__(self, id_):
        self.id = id_
        self.name = None
        self.rongzi = None

    def set_name(self, name):
        self.name = name
    def set_rongzi(self, table):
        self.rongzi = table


class itjuzi_scraper(object):

    def __init__(self):
        self.session = requests.Session()
        self.retry_times = 3
        self.sleep_time = 0.2

    def get_invest_data(self, id):

        retrytimes = self.retry_times

        while retrytimes:
            try:

                params = (
                    ('type', 'invst'),
                )

                response = requests.get('https://www.itjuzi.com/api/companies/'+id, headers=headers, params=params,
                                        cookies=cookies)
                rsp_json = response.json()
                print(rsp_json)
                rsp_json = rsp_json["data"]["invst"]
                info = []
                for invst_event in rsp_json:
                    info += (invst_event["date"], invst_event["round"] , invst_event["money"] , invst_event["investors"])
                df = pd.DataFrame(info)
                return df
            except socket.timeout:
                print('Downloaded id{}，Retry attempt {}'.format(id, retrytimes))
                retrytimes -= 1
            except IndexError as e:
                print('IndexError: {}'.format(str(e)))


    def save_to_file(self, path, data):
        with open(path, "w+") as f:
            f.write(str(data))



if __name__ == '__main__':
    spider = itjuzi_scraper()
    list_unicorns = ["18092", "2031", "24348", "157", "16470", "10886", "33165", "27142", "16575", "519", "32620864",
                     "55383", "5241", "32578945", "30970", "17422", "23029", "79793", "32755239", "14937", "42886",
                     "10160", "17975", "1606", "167410", "32785726", "3171", "12137", "33415435", "16850", "2143",
                     "10292", "29250", "10722", "32811184", "19911", "51361", "1213", "8811", "18756", "286", "16274",
                     "9271", "32755515", "27873", "4233", "32375926", "6128", "81076", "21412", "17167", "79563",
                     "3491", "42747", "1491", "3749", "18710", "26546", "53406", "25430", "60276", "62758", "33457298",
                     "4566", "3151", "24897", "17314", "20673807", "4403", "10567", "1795", "1926", "17099", "1340",
                     "43551", "279", "42608", "24210", "8705", "48235", "28041", "8", "28984", "4967", "7887",
                     "7699961", "32766436", "73326", "9017", "13846", "18664", "9986", "23347", "37944", "21897",
                     "6454", "1485", "20383", "1862", "21616", "6454", "3364177", "55077", "43479", "9844", "6715",
                     "7017", "54716", "30584", "12911", "4483", "16082", "12621", "22703", "11382", "849", "38", "1418",
                     "16184", "10782", "454", "8833", "1786", "44471", "2624", "27182", "6696134", "32112", "2315",
                     "11553", "13923", "23578", "14078", "7672235", "81102", "73599", "56299", "1821", "33359265",
                     "31889", "25503", "60647", "17847", "32542952", "34189", "63", "34864", "32786293", "9459",
                     "71236", "31389", "44499", "10602", "28997", "6054", "2549", "101", "30244", "30766", "20253",
                     "16916", "22038", "1925", "21150", "28255", "10382", "26049", "17081", "31905080", "5760",
                     "33572186", "1393", "32655", "1971", "53629", "6957", "28104", "80887", "7237", "1634", "38479",
                     "335", "58692", "32962717", "25188", "1556", "60225", "8840", "43928", "1155", "44840", "5798",
                     "33613042", "12203", "70", "11646", "33148", "107", "4887", "59787", "18031", "18266", "303",
                     "29631", "11157", "32992613", "7239", "846", "934", "32827078", "57532"]
    # list_unicorns = ["18092"]
    datas = []
    import pickle
    for id in list_unicorns:
        data = spider.get_invest_data(id)
        time.sleep(2)
        datas.append(data)
        print(data)
    with open("unicorn.bin", "wb+") as f:
        pickle.dump(datas,f)


