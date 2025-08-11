import pandas as pd
import time

ds = {
    'role': [],
    'name': [],
    'club': [],
    'season': [],
    'points': [],
    'games-started': [],
    'minutes-played': [],
    'goals-scored': [],
    'assists': [],
    'clean-sheets': [],
    'goals-conceded': [],
    'defensive-contribution': [],
    'own-goals': [],
    'penalties-saved': [],
    'saves': [],
    'bonus': [],
    'red-cards': [],
    'ict-index': [],
    'current-price': []
}

def load_site(driver):
    # access fantasy premier league statistics webpage
    driver.get('https://fantasy.premierleague.com/statistics')
    time.sleep(1)

    # accept site cookies
    driver.find_element(
        'xpath', '//button[contains(@id, "onetrust-accept-btn-handler")]').click()
    time.sleep(1)

def save_data(season_info, driver, header_info):
    ds['current-price'].append(driver.find_elements(
        'xpath', '//section[contains(@aria-labelledby, "sheet-title")]//div[contains(@class, "hi")]//span[contains(@id, "value")]')[0].text)
    ds['role'].append(header_info[0].text)
    ds['name'].append(header_info[1].text + ' ' + header_info[2].text)
    ds['club'].append(header_info[-1].text)
    ds['season'].append(season_info[0])
    ds['points'].append(int(season_info[1]))
    ds['games-started'].append(int(season_info[2]))
    ds['goals-scored'].append(int(season_info[4]))
    ds['assists'].append(int(season_info[5]))
    ds['minutes-played'].append(int(season_info[3].replace(',', '')))
    ds['clean-sheets'].append(int(season_info[9]))
    ds['goals-conceded'].append(int(season_info[10]))
    ds['defensive-contribution'].append(int(season_info[15]))
    ds['own-goals'].append(int(season_info[16]))
    ds['penalties-saved'].append(int(season_info[17]))
    ds['red-cards'].append(int(season_info[20]))
    ds['saves'].append(int(season_info[21]))
    ds['bonus'].append(int(season_info[22]))
    ds['ict-index'].append(float(season_info[27]))

def inspect_players(players, driver):
    for player in players:
        # access sheet title
        player.click()
        time.sleep(0.1)

        # collect name, role and club information
        header_info = driver.find_elements(
            'xpath', '//section[contains(@aria-labelledby, "sheet-title")]//div[contains(@class, "04")]//div')
        time.sleep(0.1)

        # obtain each season's information
        seasons = driver.find_elements(
            'xpath', '//section[contains(@aria-labelledby, "sheet-title")]//tbody//tr')
        N = 3 if len(seasons) > 3 else len(seasons)

        # save info in the dataset 'ds'
        for i in range(N):
            # divides season into list of elements
            season_info = seasons[i].text.split()
            save_data(season_info, driver,  header_info)
            print(ds)
            time.sleep(0.1)

        # scroll to next player
        driver.find_element(
            'xpath', '//section[contains(@aria-labelledby, "sheet-title")]//button[contains(@aria-label, "Close")]').click()
        time.sleep(0.1)
        driver.execute_script("window.scrollBy(0, 60);")
        time.sleep(0.1)

def run_app(pages, driver):
    # load chrome driver
    load_site(driver)

    # access all pages one by one
    for i in range(pages):
        # get player cards
        players = driver.find_elements(
            'xpath', '//tbody//tr[contains(@role, "row")]//div[contains(@class, "uvp")]//button[contains(@aria-label, "information")]')
        inspect_players(players, driver)

        # enter next page
        if i < pages - 1:
            driver.find_element(
                'xpath', '//button[contains(@aria-label, "Next")]').click()
            time.sleep(0.1)
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(0.5)

    # save dataset into csv file
    pd.DataFrame(ds).to_csv(
        f'data/{pages}_page{'s' if pages > 1 else ''}_stats.csv')
    driver.quit()
