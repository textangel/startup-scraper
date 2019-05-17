# coding=utf8
from selenium_scraper.utils import append_df_to_excel
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import pandas as pd

class EmployeesDatabase:
    def __init__(self):
        self.invest_firms = {'1': '红杉资本中国', '2': 'IDG资本', '3': '创新工场', '4': '真格基金', '5': 'KPCB凯鹏华盈中国', '6': '北极光创投', '7': '经纬中国', '8': '蓝驰创投', '9': '君联资本', '10': '启明创投', '11': '金沙江创投', '12': '晨兴资本', '13': 'DCM中国', '14': '今日资本', '15': 'Redpoint Ventures红点全球基金', '16': '宽带资本CBC', '17': 'PreAngel', '18': '高通Qualcomm Ventures', '19': '九合创投', '20': 'GGV纪源资本', '21': '清科创投', '22': '险峰长青', '23': '光速中国', '25': '阿米巴资本', '26': '挚信资本', '28': '深创投', '29': '天使湾', '31': '鼎晖投资', '32': 'Ventech China银泰资本', '33': '青松基金', '34': '戈壁创投', '35': '成为资本', '36': '祥峰投资', '39': '策源创投', '40': '中路资本', '41': 'CA创投', '42': '盘古创富VANGOO', '45': '腾讯', '47': '德同资本', '48': '阿里巴巴', '51': '苏河汇', '52': '乐搏资本', '54': '华映资本', '55': 'Cherubic Ventures心元资本', '56': '芳晟股权投资基金', '58': '时尚传媒(时尚资本)', '59': '创新谷Innovalley', '60': '盛大资本', '61': '松禾资本', '62': '奇虎360', '65': '顺为资本', '66': '美国中经合集团', '68': '华创资本', '69': '纽信创投', '70': '联创永宣', '71': '赛富基金', '72': '达晨创投', '75': '用友幸福投资', '76': 'SIG海纳亚洲', '77': '传媒梦工场', '79': '携程', '80': '新浪微博基金', '81': '德迅投资', '82': '同创伟业', '87': '原子创投', '94': '信中利资本', '96': '隆领投资', '97': '平安创新投资基金', '100': '天图投资', '102': '源渡创投', '103': '亚商资本', '104': '汉理资本', '106': '创业工场VenturesLab', '107': '英特尔投资Intel Capital', '109': '德鼎创新基金(德丰杰龙脉)', '111': '东方弘道(弘合基金)', '112': '人人公司(千橡集团)', '114': '创业接力(创业基金会)', '119': '风和投资', '120': '云锋基金', '125': '光线传媒', '126': '东方富海', '129': '网易', '130': '紫辉创投', '131': '猎豹移动', '133': '联想之星', '134': '好未来(学而思)', '135': '架桥资本', '139': '新进创投', '142': '华谊兄弟', '146': 'NEA恩颐投资', '148': '软银中国', '150': '斯道资本(富达亚洲)', '151': '新东方', '153': '诺基亚成长基金', '155': 'ClearVue锴明投资', '157': '兰馨亚洲', '158': '华睿投资', '160': 'DST', '163': '华平投资', '164': '蓝色光标', '165': '凯辉基金', '166': '创东方投资', '167': '招商局资本', '168': 'LB投资(LB Investment)', '169': 'TCL资本', '170': '凯雷亚洲基金', '172': 'Temasek淡马锡', '174': '薛蛮子(蛮子基金)', '176': '极客帮创投', '178': 'Infinity Venture Partners（IVP）', '179': '奥飞娱乐', '181': '英诺天使基金', '183': '泰岳梧桐资本', '185': '乐视网', '188': '九鼎投资', '190': '方广资本', '191': '苏宁', '192': '弘毅投资', '193': '复星锐正资本', '194': '浙商创投', '196': '景林投资', '197': '明势资本', '198': 'Tiger老虎基金(中国)', '199': '中信产业基金', '200': '嘉御基金', '204': '云天使基金', '205': '丰厚资本', '209': '抱团创投', '212': '元禾控股', '214': '盈动资本', '218': '真顺基金', '221': '银杏谷资本', '223': '中兴合创', '224': '京东', '225': '清流资本', '231': '华软投资', '232': '中国文化产业投资基金', '233': '高榕资本', '237': '钟鼎创投', '240': '唯品会', '242': '英飞尼迪Infinity', '245': '凯欣亚洲投资Crescent Group', '246': '北软天使基金', '250': '重山资本', '252': '汉能投资', '255': '高盛集团(中国)', '257': '中信资本', '258': '高瓴资本', '262': '朗玛峰创投', '263': '中科招商', '264': '普思资本', '265': '启赋资本', '268': '老鹰基金', '269': '天堂硅谷', '270': '好望角投资', '271': '秉鸿资本', '272': '梧桐树资本', '273': '五岳资本', '274': '创业邦天使基金', '276': '开物投资', '283': '国泰创投', '298': '合力投资', '299': '常春藤资本', '300': '新天域资本', '309': '华山资本WestSummit Capital', '311': '雷雨资本(微投VChello)', '364': 'Star VC', '374': '华兴资本', '497': '和君资本', '588': 'Sequoia Capital（红杉海外）', '613': '硅谷银行Silicon Valley Bank', '708': 'Coatue Management', '779': '天星资本', '781': '合鲸资本', '835': '厚朴基金', '843': '华盖资本', '844': '国科嘉和', '845': '力合科创（力合创投）', '846': '梅花创投', '848': '普华资本', '939': '天神娱乐', '992': '暾澜投资', '1022': '复星集团', '1036': '盛景网联(盛景嘉成)', '1091': '海通开元', '1092': '广发信德', '1107': '华人文化产业投资基金', '1114': 'BWVC泽厚资本', '1119': 'H Capital', '1179': '深圳厚德前海基金', '1223': '和玉资本', '1240': '坚果资本', '1250': '中文在线', '1312': '优酷', '1329': 'NextBig三万弘合投资', '1332': '线性资本', '1333': '丹华资本', '1336': '远镜创投', '1343': '如山资本', '1344': '中金公司', '1345': '源码资本', '1349': '825新媒体产业基金', '1352': '清控科创控股', '1356': '志成资本', '1357': '光合创投(光合基金)', '1359': '云启资本', '1362': '蓝湖资本', '1363': '知卓资本', '1364': '弘晖资本', '1365': '力合清源', '1366': '无穹创投', '1374': '暴龙资本', '1375': '赛伯乐投资', '1376': '58同城', '1379': '毅达资本', '1382': '娱乐工场', '1383': '龙腾资本', '1386': '伯藜创投', '1387': '达泰资本', '1393': '易一天使', '1398': '洪泰基金', '1408': '源政投资', '1409': '联想创投集团', '1413': '易车网', '1416': '以太创服（以太资本）', '1418': '天使投资人王刚', '1432': '信天创投', '1455': 'GIC新加坡政府投资公司', '1459': ' 青山资本', '1460': '博派资本', '1466': '万达集团', '1474': 'MindWorks Ventures概念资本', '1477': '京北投资', '1481': '湖畔山南资本', '1491': '艾瑞资本(艾瑞)', '1492': '黑马基金', '1493': '起源资本', '1495': '元璟资本', '1496': '金石投资', '1499': '正和岛正和磁系资本', '1504': '米仓资本', '1508': '陶石资本', '1511': '安芙兰资本', '1512': '赛领资本', '1525': '基石资本', '1550': '德沃基金', '1557': '海尔', '1558': '光信资本', '1559': '凯风创投', '1589': '涌铧投资', '1600': '光大集团', '1604': '众海投资', '1605': '乐游资本', '1606': '执一资本', '1607': '游族网络', '1608': '昆仑万维', '1611': '创享投资', '1616': '浅石创投', '1617': '熊猫资本', '1619': '唯猎资本', '1621': '长石资本', '1625': '微光创投', '1631': '分众传媒', '1633': '迭代资本', '1638': '熙金资本', '1639': '愉悦资本', '1643': '飞马基金-飞马旅', '1649': '麦星投资', '1651': '挚盈资本', '1653': '乾明投资', '1656': '界石投资', '1661': '春华资本Primavera', '1663': '联新资本', '1672': '小村资本', '1673': '协立投资', '1682': '磐谷创投', '1685': '天风证券(天风天睿)', '1689': '远翼投资', '1691': '大河创投', '1692': '动域资本', '1699': '华旦天使投资', '1700': '光源资本', '1701': '六禾创投', '1706': '千合资本', '1715': '星瀚资本', '1718': '风云资本', '1719': '逐鹿资本', '1729': '上海掌门科技', '1736': '分布式资本', '1745': '初心资本', '1753': '春晓资本', '1756': '晨晖资本', '1762': '顺丰速运', '1769': '零一创投', '1773': '磐石资本', '1778': '蓝象资本', '1779': '盈信资本', '1783': '玖富', '1784': '双湖资本', '1785': '天使汇', '1794': '阿尔法公社', '1796': '琢石投资', '1801': '涌金集团', '1803': '分享投资', '1804': '杭州多牛资本', '1809': '长安私人资本', '1815': '中关村发展集团', '1830': '盛世景投资', '1831': '众诚资本', '1835': '峰瑞资本', '1848': '东方证券(东方星晖)', '1850': '青骢资本', '1852': '蚂蚁金服(阿里巴巴)', '1856': '国金投资', '1862': '耀途资本', '1865': '济峰资本', '1871': 'MFund魔量基金', '1874': '创势资本', '1877': '龙翌资本', '1879': '和盟创投', '1883': '国泰君安', '1900': '东湖天使基金', '1904': '泰有投资', '1912': '普洛斯GLP', '1916': '麦腾创投', '1917': '紫牛基金', '1918': '辰德资本', '1922': '天天投', '1925': '滴滴', '1927': '今日头条', '1928': '知初资本', '1929': '中科创星', '1930': '荣正投资', '1934': '华兴新经济基金', '1935': '顺融资本', '1944': '领沨资本', '1946': '中美创投', '1961': '优客工场', '1962': '创客总部', '1985': '众为资本', '1987': '帮实资本', '1988': '大道至简资本', '1994': '聚秀资本', '1999': '辰海资本', '2014': '三行资本', '2021': '集结号资本', '2069': '礼来亚洲基金', '2073': '天鹰资本', '2082': '赫斯特Hearst Ventures', '2085': '海泉基金(胡海泉)', '2090': '点亮资本', '2102': '歌斐资产', '2105': '有成资本', '2120': '西科天使基金', '2124': '湖杉资本', '2127': '北汽产业投资基金', '2132': '德联资本', '2134': '红星美凯龙', '2137': '中卫基金', '2139': '金浦投资', '2148': '启迪之星（启迪孵化器）', '2170': '国开金融(国开开元)', '2173': '青锐创投', '2176': '道生资本', '2180': '东方汇富', '2185': '发现创投', '2189': '孝昌水木投资', '2203': '远瞻资本', '2207': '治平资本', '2208': '微影资本(微影时代)', '2209': '南山资本', '2215': '道彤投资', '2221': '星河互联', '2263': '嘉道谷投资(龚虹嘉)', '2309': '金慧丰投资', '2325': '水木清华校友基金', '2329': '天创资本', '2332': '明嘉资本', '2333': '创丰资本', '2343': '臻云创投', '2362': '约印创投', '2365': '中信证券', '2381': '元生资本', '2385': '山行资本', '2401': '安赐资本', '2413': '华泰证券', '2416': '中华开发', '2428': '上汽投资-尚颀资本', '2431': '创大资本', '2435': '招商银行', '2440': '尚势资本', '2442': '集素资本', '2446': '寒武创投', '2459': '头头是道投资基金', '2488': '鼎聚投资', '2493': '考拉基金(拉卡拉)', '2498': '博将资本', '2506': 'Integral雄厚资本', '2521': '贵格天使', '2524': '汉富控股', '2527': '莲花资本', '2531': '玖创资本', '2557': '飞图创投', '2564': '青桐资本', '2579': '前海梧桐并购基金', '2581': '乔景资本', '2592': '凯泰资本', '2609': '唯嘉资本', '2615': '尚珹资本', '2624': '雅瑞资本', '2631': '富士康', '2642': '亦联资本(YY多玩)', '2654': '朗盛投资', '2661': '如川投资', '2668': '立元创投', '2669': '齐一资本', '2672': '云起资本', '2674': '远毅资本', '2677': '凯盈资本', '2681': 'AC加速器', '2697': '鼎翔资本', '2714': '磐霖资本', '2721': '越秀产业基金', '2722': '芒果文创基金', '2726': '澎湃资本', '2734': '建信资本', '2738': 'EMC媒体基金', '2746': '云九资本', '2762': '宜信财富', '2779': '宁波天使投资引导基金', '2903': '优势资本', '2923': '阿里巴巴创业者基金', '2971': '国科投资', '3026': '火橙资本', '3033': '曦域资本', '3097': '高达投资', '3154': '国投创新', '3213': '正心谷创新资本', '3302': '元禾原点创投', '3304': '药明康德', '3358': '前海母基金', '3376': '泛城资本', '3422': '方正和生投资', '3426': '中信建投资本', '3460': '猎鹰创投', '3551': '新龙脉控股', '3568': 'XVC创投', '3628': '永柏资本PGA Ventures', '3669': '众麟资本', '3734': '金科君创', '3775': '博裕资本', '3793': '海丰至诚', '3812': '本草资本', '4008': '君上资本', '4194': '远望资本', '4355': '复朴投资', '4540': '索道投资', '4731': '昆仲资本', '4823': '招银国际', '4824': 'TF Capital泰福资本', '4847': '领势投资', '5022': '中民投', '5053': '创世资本', '5177': '武岳峰资本', '5179': '华业天成(华诺创投)', '5243': '清控银杏创投', '5341': '建银国际', '5406': '苹果天使APU', '5442': '鼎兴量子', '5449': '嘉实投资-嘉实基金', '5651': '晨山资本', '5678': '源星资本', '6042': '中航信托', '6081': '国家中小企业发展基金（国中创投）', '6441': '襄禾资本', '6443': '兴旺投资', '6463': '雅惠精准医疗基金', '6479': '火山石资本', '6504': '点亮基金', '6508': '沸点资本', '6513': '晨晖创投', '6515': '名川资本', '6525': '将门创投', '6529': '红点创投中国基金', '6531': '水木资本', '6539': '翊翎资本', '6568': 'Plug and Play', '6574': '壹号资本', '6578': '伽利略资本', '6582': '浩方创投', '6596': '璀璨资本', '6601': '追远创投', '6611': '创世伙伴资本', '6634': '嘉程资本', '6636': '晟道投资', '6640': '百度风投', '6659': '澜亭资本', '6673': '金沙江联合资本', '6687': '硬币资本INBlockchain', '6699': '蓝图创投', '6700': '星合资本', '6702': '不惑创投', '6737': '真成投资', '6749': '元生创投', '6788': '险峰旗云', '6797': '节点资本', '6819': '科银资本Collinstar Capital', '6875': '了得资本', '6879': '挑战者资本', '6886': '51信用卡', '6889': '哔哩哔哩bilibili', '6890': '科大讯飞', '6896': '火币网', '6902': '光谷人才基金', '6904': '麓谷高新创投', '6909': '达安基因', '6910': '达安创谷', '6928': '广发乾和', '6937': '启迪种子', '6942': '龙磐投资', '6944': '国投创业', '7092': 'JRR Crypto', '7117': '追梦者基金', '7201': '海尔资本', '7221': '火币全球生态基金', '7381': '北塔资本'}
        self.current_batch = pd.DataFrame([], columns=["id", "name", "founder_name","founder_role","founder_link","founder_bio","founder_schools","founder_employers"])

    def reset_current_batch(self):
        self.current_batch = pd.DataFrame([], columns=["id", "name", "founder_name", "founder_role", "founder_link",
                                                       "founder_bio", "founder_schools", "founder_employers"])

def login(browser, login_path, username, password):
    browser.get("https://www.itjuzi.com/login")
    browser.find_element_by_css_selector('[name^="account"]').send_keys(username)
    browser.find_element_by_css_selector('[name^="password"]').send_keys(password)
    browser.find_element_by_css_selector('.btn.btn-primary.submit-btn.w-100.mt-3').click()
    time.sleep(3)

def get_employee_info(browser, id, db:EmployeesDatabase):
    # Go to desired website
    browser.get("https://www.itjuzi.com/investfirm/"+str(id))
    # Wait 20 seconds for page to load
    timeout = 10
    try:
        # Wait until the final element [Avatar link] is loaded.
        # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
        # the last things to be loaded.
        WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="member"]/div[2]/div[1]/div/p[1]/a[1]')))
        employees = browser.find_elements_by_xpath('//*[@id="member"]/div[2]/div')
        if employees[-1].text == "展开全部":
            employees[-1].click()
        employees = browser.find_elements_by_xpath('//*[@id="member"]/div[2]/div')
        for emp in employees:
            emp_name = emp.find_element_by_xpath('.//div/p[1]/a[1]/b').text
            emp_role = emp.find_element_by_xpath('.//div/p[1]/a[1]/span[1]').text
            emp_bio = emp.find_element_by_css_selector('.person-intro.w-100').text
            emp_link = emp.find_element_by_xpath('.//div/p[1]/a[1]').get_attribute("href")

            emp_data = {
                "id": [id],
                "name": [db.invest_firms[id]],
                "founder_name": [emp_name],
                "founder_role": [emp_role],
                "founder_link": [emp_link],
                "founder_bio": [emp_bio],
                "founder_schools": [""],
                "founder_employers": [""],
            }
            db.current_batch = db.current_batch.append(pd.DataFrame.from_dict(emp_data, orient="columns"))
        
    except TimeoutException:
        print("Timed out waiting for page to load")
        pass
    except NoSuchElementException:
        pass
    except Exception as e:
        print("Another error occured", e.__traceback__.tb_lasti)
        pass

def setup(username = "m1408786@nwytg.net", password = "123456"):
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-dev-shm-usage')
    option.add_argument('--incognito')
    option.add_argument("--window-size=550x900")
    
    # Create new Instance of Chrome in incognito mode
    option.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    browser = webdriver.Chrome(executable_path='/Users/zhengyuanma/Library/Application Support/Google/chromedriver',
                               chrome_options=option)
    login(browser, "https://www.itjuzi.com/login", username, password)
    return browser

def scrape_employee_data():
    browser = setup()

    db = EmployeesDatabase()
    cnt = 1
    for firm_id in db.invest_firms.keys():
        get_employee_info(browser, firm_id, db)
        cnt += 1
        if cnt == 1:
            append_df_to_excel("all_firms_employees_temp.xlsx", db.current_batch)
            db.reset_current_batch()
        if cnt%10 == 0:
            append_df_to_excel("all_firms_employees_temp.xlsx", db.current_batch, header=None)
            db.reset_current_batch()

def get_educational_info(browser, link, firm_name):
    # Go to desired website
    browser.get(link)
    # Wait 20 seconds for page to load
    timeout = 10
    try:
        # Wait until the final element [Avatar link] is loaded.
        # Assumption: If Avatar link is loaded, the whole page would be relatively loaded because it is among
        # the last things to be loaded.
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, '//h2[translate(text(), " ", "") ="教育经历"]')))
        time.sleep(2)
        employemnt = browser.find_elements_by_xpath('//h2[translate(text(), " ", "") ="工作经历"]/following::div[1]/ul/li')
        jobs = []
        for job in employemnt:
            job = job.text.strip()
            if job != "" and job != "暂无收录":
                jobs.append(job)
        jobs = tuple(jobs)

        education = browser.find_elements_by_xpath('//h2[translate(text(), " ", "") ="教育经历"]/following::div[1]/ul/li')
        schools = []
        for school in education:
            school = school.text.strip()
            if school != "" and school != "暂无收录":
                schools.append(school)
        schools = tuple(schools)

        # other_firms = browser.find_element_by_xpath('//ul[@class="list mb-1"]/li').text
        # # other_roles = browser.find_element_by_xpath('//ul[@class="list mb-1"]/li/text()')
        # # other_firms_roles = dict(zip(other_firms, other_roles))
        # firms = []
        # for firm in other_firms:
        #     firm = firm.text.strip()
        #     if firm != firm_name:
        #         firms.append(firm)
        # firms = tuple(firms)

        # return jobs, schools, firms
        return jobs, schools

    except TimeoutException:
        print("Timed out waiting for page to load")
        pass
    except NoSuchElementException:
        pass
    

def scrape_education_data():
    user_pw = {
        0: ("j5246866@nwytg.net", "123456"),
        1: ("bsr09987@ebbob.com", "123456"),
        2: ("tsx89350@iencm.com", "123456")
    }
    c = 0
    browser = setup(username=user_pw[c][0], password=user_pw[c][1])
    employee_data = pd.read_excel("all_firms_employees_master.xlsx", header=None)
    employee_data.columns = ["0", "id", "name", "founder_name", "founder_role", "founder_link", "founder_bio"]
    partners_data = employee_data[employee_data.founder_role.str.contains(r"创|合伙|[^副]*董事长")]
    partners_data["founder_schools"] = ""
    partners_data["founder_employers"] = ""
    partners_data = pd.read_excel("all_partners_data_2.xlsx", header=0, index_col=0)
    partners_data = partners_data.drop("0", axis = "columns")
    cnt = 1
    cutoff = 0
    for index, partner in partners_data.iterrows():
        if index < cutoff:
                continue
        try:
            jobs, schools = get_educational_info(browser, partner["founder_link"], partner["name"])
            jobs, schools = str(jobs), str(schools)

            partners_data.at[index, "founder_schools"] = schools
            partners_data.at[index, "founder_employers"] = jobs
            if cnt%20 == 0:
                partners_data.to_excel("all_partners_data_3.xlsx")
            if cnt%100 ==0:
                time.sleep(180)
                c = (c+1)%3
                browser.close()
                browser = setup(username=user_pw[c][0], password=user_pw[c][1])
            cnt += 1
        except TypeError as e:
            print(e)
            pass

scrape_education_data()
