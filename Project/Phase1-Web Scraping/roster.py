from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

chrome_setting = Options()
chrome_setting.add_argument('--ignore-certificate-errors')
chrome_setting.add_argument('--ignore-ssl-errors')
chrome_setting.add_argument('--allow-insecure-localhost')
chrome_setting.add_argument('--disable-web-security')
chrome_setting.add_argument('--disable-features=NetworkService')
chrome_setting.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_setting.add_argument("--lang=en-US")
chrome_setting.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
chrome_setting.add_argument('--no-sandbox')
chrome_setting.add_argument('--disable-dev-shm-usage')
from selenium.webdriver.chrome.service import Service

service = Service()
browser = webdriver.Chrome(service=service, options=chrome_setting)

df_teams = pd.read_csv('D:\Quera\Week7\Teams_Table\Teams_Final.csv')

team_index = 0
all_rosters = []

# for link in df_teams['team_link']:
link='https://www.basketball-reference.com/teams/ATL/2020.html'
browser.get(link)
time.sleep(10)
wait = WebDriverWait(browser, 15)
table = wait.until(EC.presence_of_element_located((By.ID, "div_roster")))
rows = browser.find_elements(By.CSS_SELECTOR, '#roster tbody tr')
    
for row in rows:
    cells = row.find_elements(By.XPATH, './/th | .//td')
        
    if len(cells) >= 9:
        try:
            height_cell = row.find_element(By.CSS_SELECTOR, 'td[data-stat="height"]')
            height_inches = height_cell.get_attribute('csk')
        except:
            height_cell = cells[3]
            height_inches = height_cell.get_attribute('csk')
    

        if height_inches and height_inches.strip():
            try:
                height_cm = float(height_inches) * 2.54
            except:
                height_cm = None
        else:
            height_text = height_cell.text.strip()
            if height_text and '-' in height_text:
                try:
                    feet, inches = height_text.split('-')
                    height_cm = (int(feet) * 12 + int(inches)) * 2.54
                except:
                    height_cm = None
            else:
                height_cm = None

        
        try:
            player_link = cells[1].find_element(By.TAG_NAME, 'a')
            player_name = player_link.get_attribute('textContent').strip()
        except:
            player_name = cells[1].text.strip()
        
        
        player_info = {
            'number_player': cells[0].text.strip(),
            'player_name':player_name,
            'position': cells[2].text.strip(),
            'height_cm': round(height_cm) if height_cm else None, 
            'weight': cells[4].text.strip(),
            'birth_date': cells[5].text.strip(),
            'birth_country': cells[6].text.strip().replace('us', '').replace('ca', '').replace('de', '').strip(),
            'experience': cells[7].text.strip(),
            'college': cells[8].text.strip(),
            'season': df_teams.iloc[team_index]['season'],
            'team_name':df_teams.iloc[team_index]['team_name']
        }
        
        all_rosters.append(player_info)
    
team_index += 1

browser.quit()

df_all = pd.DataFrame(all_rosters)  
df_all.to_csv('tst.csv', index=False, encoding='utf-8-sig')