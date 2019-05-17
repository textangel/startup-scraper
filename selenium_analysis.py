import pandas as pd
from collections import Counter
import re

def cleanup(string: str):
    pattern = re.compile("[\(\)\\\']")
    string = re.sub(pattern, "", string)
    strings = [s.strip() for s in string.split(',') if s.strip() is not ""]
    return strings

partners_data = pd.read_excel("../selenium_scraper/all_partners_data_2.xlsx", header=0, index_col=0)
schools_list = [cleanup(school) for school in partners_data[partners_data.founder_role == '创始合伙人']["founder_schools"].dropna()]
schools_list = [item for sublist in schools_list for item in sublist]
print(Counter(schools_list))

employers_list = [cleanup(employer) for employer in partners_data[partners_data.founder_role == '创始合伙人']["founder_employers"].dropna()]
employers_list = [item for sublist in employers_list for item in sublist]
print(Counter(employers_list))