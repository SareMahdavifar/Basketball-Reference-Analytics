from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
import time
import pandas as pd
import warnings
import requests
warnings.filterwarnings('ignore')

try:
    response = requests.get("https://www.google.com", timeout=10)
    print("Internet is connected")
except:
    print("No Connection")
    exit()

chrome_setting = Options()
chrome_setting.add_argument('--ignore-certificate-errors')
chrome_setting.add_argument('--ignore-ssl-errors')
chrome_setting.add_argument('--allow-insecure-localhost')
chrome_setting.add_argument('--disable-web-security')
chrome_setting.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_setting.add_argument("--lang=en-US")
chrome_setting.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_setting.add_argument('--no-sandbox')
chrome_setting.add_argument('--disable-dev-shm-usage')
chrome_setting.add_argument('--disable-gpu')
chrome_setting.add_argument('--disable-extensions')

chrome_setting.add_argument('--lang=pt-BR,en-US')
chrome_setting.add_argument('--accept-lang=pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7')

chrome_setting.add_experimental_option('prefs', {
    'profile.default_content_setting_values.images': 2,  
    'profile.managed_default_content_settings.images': 2,
    'intl.accept_languages': 'pt-BR,pt,en-US,en',
})

from selenium.webdriver.chrome.service import Service

service = Service()
service.start_timeout = 30 
browser = webdriver.Chrome(service=service, options=chrome_setting)
browser.set_page_load_timeout(20) 

df_teams = pd.read_csv(r'D:/Quera/Week7/Teams_Table/Teams_Final.csv')

team_index = 0
salary_table = [] 

# link='https://www.basketball-reference.com/teams/IND/2024.html'
for link in df_teams['team_link']:
    browser.get(link)
    time.sleep(10)
    wait = WebDriverWait(browser, 15)

    salary_div = browser.find_element(By.ID, "div_salaries2")
    rows = salary_div.find_elements(By.CSS_SELECTOR, 'tbody tr')

    for row in rows:
        cells = row.find_elements(By.XPATH, './/th | .//td')
        if len(cells) >= 3: 
            try:
                player_link = cells[1].find_element(By.TAG_NAME, 'a')
                player_name = player_link.get_attribute('textContent').strip()
            except:
                player_name = cells[1].text.strip() 
                
            salary_info = {
                'rank': cells[0].text.strip(),
                'player_name': player_name,
                'salary': cells[2].text.strip(),
                'season': df_teams.iloc[team_index]['season'],
                'team_name': df_teams.iloc[team_index]['team_name'] 
            }
            salary_table.append(salary_info)

    team_index += 1  

        
browser.quit()

df_all = pd.DataFrame(salary_table)  
df_all.to_csv('salar.csv', index=False, encoding='utf-8-sig')
