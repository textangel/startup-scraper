# coding=utf8
import time
import pandas as pd
from selenium_scraper.utils import append_df_to_excel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

list_unicorns = ["18092", "2031", "24348", "157", "16470", "10886", "33165", "27142", "16575", "519", "32620864", "55383", "5241", "32578945", "30970", "17422", "23029", "79793", "32755239", "14937", "42886", "10160", "17975", "1606", "167410", "32785726", "3171", "12137", "33415435", "16850", "2143", "10292", "29250", "10722", "32811184", "19911", "51361", "1213", "8811", "18756", "286", "16274", "9271", "32755515", "27873", "4233", "32375926", "6128", "81076", "21412", "17167", "79563", "3491", "42747", "1491", "3749", "18710", "26546", "53406", "25430", "60276", "62758", "33457298", "4566", "3151", "24897", "17314", "20673807", "4403", "10567", "1795", "1926", "17099", "1340", "43551", "279", "42608", "24210", "8705", "48235", "28041", "8", "28984", "4967", "7887", "7699961", "32766436", "73326", "9017", "13846", "18664", "9986", "23347", "37944", "21897", "6454", "1485", "20383", "1862", "21616", "6454", "3364177", "55077", "43479", "9844", "6715", "7017", "54716", "30584", "12911", "4483", "16082", "12621", "22703", "11382", "849", "38", "1418", "16184", "10782", "454", "8833", "1786", "44471", "2624", "27182", "6696134", "32112", "2315", "11553", "13923", "23578", "14078", "7672235", "81102", "73599", "56299", "1821", "33359265", "31889", "25503", "60647", "17847", "32542952", "34189", "63", "34864", "32786293", "9459", "71236", "31389", "44499", "10602", "28997", "6054", "2549", "101", "30244", "30766", "20253", "16916", "22038", "1925", "21150", "28255", "10382", "26049", "17081", "31905080", "5760", "33572186", "1393", "32655", "1971", "53629", "6957", "28104", "80887", "7237", "1634", "38479", "335", "58692", "32962717", "25188", "1556", "60225", "8840", "43928", "1155", "44840", "5798", "33613042", "12203", "70", "11646", "33148", "107", "4887", "59787", "18031", "18266", "303", "29631", "11157", "32992613", "7239", "846", "934", "32827078", "57532"]
unicorns_bins = [list_unicorns[0:70], list_unicorns[70:140], list_unicorns[140:211]]

class Unicorn:
    def __init__(self, id_):
        self.id = id_
        self.name = None
        self.rongzi = None

    def set_name(self, name):
        self.name = name
    def set_rongzi(self, table):
        self.rongzi = table


def login(browser, login_path, username, password):
    browser.get("https://www.itjuzi.com/login")
    browser.find_element_by_css_selector('[name^="account"]').send_keys(username)
    browser.find_element_by_css_selector('[name^="password"]').send_keys(password)
    browser.find_element_by_css_selector('.btn.btn-primary.submit-btn.w-100.mt-3').click()
    time.sleep(3)


def setup(username = "13120211207", password = "123456"):
    # Specifying incognito mode as you launch your browser[OPTIONAL]
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--incognito')
    option.add_argument("--window-size=550x1200")
    # option.add_argument("user-data-dir=/Users/zhengyuanma/Library/Application Support/Google/Chrome/Default")

    # Create new Instance of Chrome in incognito mode
    option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    browser = webdriver.Chrome(executable_path='/Users/zhengyuanma/Library/Application Support/Google/chromedriver',
                               chrome_options=option)
    login(browser, "https://www.itjuzi.com/login", username, password)
    return browser

def scrape_employee_data():
    # list_unicorns = ["18092"]
    unis = []
    for bin_no in [2]:
        browser = setup()
        for id_ in unicorns_bins[bin_no]:
            uni = Unicorn(id_)
            browser.get("https://www.itjuzi.com/company/" + id_)
            name = None
            rongzi_df = None
            timeout = 10
            try:
                WebDriverWait(browser, timeout).until(
                    EC.visibility_of_element_located((By.XPATH, '//h2[translate(text()," ","")="融资"]/parent::div/following-sibling::table/tbody/tr')))

                name = browser.find_element_by_xpath('//div[@class="juzi-nav-cont"]/span').text.replace(">", "").strip()
            except:
                pass
            try:
                browser.find_element_by_xpath('//td[translate(text()," \n","")="加载更多"]').click()
            except:
                pass
            data = []
            try:
                rongzi = browser.find_elements_by_xpath('//h2[translate(text()," ","")="融资"]/parent::div/following-sibling::table/tbody/tr')
                if rongzi[-1].text.strip() == "加载更多":
                    rongzi = rongzi[0:-1]
                for row in rongzi:
                    row_text = [elements.text for elements in row.find_elements_by_xpath(".//td")]
                    data += [row_text]
            except:
                pass
            rongzi_df = pd.DataFrame(data)
            uni.set_name(name)
            uni.set_rongzi(rongzi_df)
            unis += [uni]

            full_df = pd.concat([pd.DataFrame([["====", name, id_]]),rongzi_df])
            append_df_to_excel("unicorns2.xlsx", full_df)
            print(full_df)
            time.sleep(0.5)

        import pickle
        with open(f"unis_{bin_no}.bin", "wb+") as f:
            pickle.dump(unis, f)
        input()


scrape_employee_data()

