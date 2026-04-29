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


opts = Options()
opts.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36')
opts.add_argument('--lang=en-US')
opts.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})


def extract_player_stats(browser, selected_season):

    browser.get(f'https://www.basketball-reference.com/leagues/NBA_{str(selected_season)}_totals.html')

    WebDriverWait(browser, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table#totals_stats'))
    )

    # season = browser.find_element(By.CSS_SELECTOR, 'div#meta h1 span').text.strip()
    season = f'{selected_season-1}-{selected_season-2000}'
    total_stats_table = browser.find_element(By.CSS_SELECTOR, 'table#totals_stats')
    total_stats_header = total_stats_table.find_elements(By.CSS_SELECTOR, 'thead tr th')
    total_stats_body = total_stats_table.find_elements(By.CSS_SELECTOR, 'tbody tr:not(.thead):not(.norank)')

    header_list = []

    for header in total_stats_header:
        head = header.text.strip() or None
        header_list.append(head)

    header_list.insert(1, 'player_url')
    header_list.insert(2, 'season')  

    print(header_list)      

    tr_data = []
    for tr in total_stats_body:
        print("Hiiiiiiii")
        rank = tr.find_element(By.CSS_SELECTOR, 'th').text.strip()
        player_url = tr.find_element(By.CSS_SELECTOR, 'td[data-stat="name_display"] a').get_attribute('href')
        td_data = [rank, player_url, season] 
        all_td = tr.find_elements(By.CSS_SELECTOR, 'td')
        for td in all_td:
            td_data.append(td.text.strip())
        tr_data.append(td_data)

    player_stats_df = pd.DataFrame(tr_data, columns=header_list)

    return player_stats_df


seasons = [2020, 2021, 2022, 2023, 2024, 2025]

browser = webdriver.Chrome(options=opts)
all_players_stats = []

for season in seasons:
    time.sleep(random.uniform(1, 4))
    all_players_stats.append(extract_player_stats(browser, season))

browser.quit()

all_players_stats_df = pd.concat(all_players_stats)

all_players_stats_df.to_csv('./player_stats.csv', index=False)








