import re
import requests
import openpyxl
import pandas as pd
import time, random
from bs4 import BeautifulSoup
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


headers = {
    'user-agent' : ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36'),
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.basketball-reference.com/players/'
    }

session = requests.Session()
session.headers.update(headers)

team_url = 'https://www.basketball-reference.com/teams/'

response = session.get(team_url)
soup = BeautifulSoup(response.text, 'html.parser')


names = soup.select('div#all_teams_active table a[href^="/teams/"]')

result = []
for name in names:
    a = name['href']
    full_name = name.text
    abbr_name = re.search(r'(?<=/teams/)[A-Z]{3}(?=/)', a).group()

    result.append({'full_name': full_name, 'abbr_name': abbr_name})


teams_name = pd.DataFrame(result)

print(teams_name)

with pd.ExcelWriter('./player_stats.xlsx', engine='openpyxl', mode='a') as writer:
    teams_name.to_excel(writer, sheet_name='teams_name', index=False)







