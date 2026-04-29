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

years=[2020,2021,2022,2023,2024]
all_teams = []
for year in years:
        browser.get(f'https://www.basketball-reference.com/leagues/NBA_{year}.html')
        time.sleep(10)


        wait = WebDriverWait(browser, 15)
        table = wait.until(EC.presence_of_element_located((By.ID, "totals-team")))
        team_items = table.find_elements(By.XPATH, './/tbody/tr[@data-row and not(contains(@class, "thead"))]')

        teams_this_year = []

        for item in team_items:
        
                team_cell = item.find_element(By.XPATH, './/td[@data-stat="team"]')
                link_element = team_cell.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute("href")
                name = link_element.text.strip()

                teams_this_year.append({
                'year': year,
                'team_name': name,
                'coach': None,
                'arena': None,
                'team_link': link
                })

        for team_info in teams_this_year:
                browser.get(team_info['team_link'])
                WebDriverWait(browser, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "h1")))
                time.sleep(2)

                try:
                        coach_element = browser.find_element(By.XPATH, "//p[contains(., 'Coach:')]")
                        coach_html = coach_element.get_attribute('innerHTML')
                        start = coach_html.find('>', coach_html.find('<a')) + 1
                        end = coach_html.find('<', start)
                        team_info['coach'] = coach_html[start:end].strip()
                except:
                        team_info['coach'] = "Not Found"
                
                try:
                        arena_element = browser.find_element(By.XPATH, "//p[contains(., 'Arena:')]")
                        arena_html = arena_element.get_attribute('innerHTML')               
                        if 'Arena:</strong>' in arena_html:
                                arena_part = arena_html.split('Arena:</strong>')[1]
                                arena_name = arena_part.split('<')[0]
                                team_info['arena'] = arena_name.strip()
                        else:
                                team_info['arena'] = "Not Found"
                except:
                        team_info['arena'] = "Not Found"
                
        
                all_teams.append(team_info)
                time.sleep(1)
                
        df_teams = pd.DataFrame(all_teams)
                
df_teams.to_csv('all_nba_teams.csv', index=False)
browser.quit()