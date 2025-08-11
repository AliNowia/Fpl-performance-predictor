from selenium import webdriver
import time

driver = webdriver.Chrome()

driver.get('https://fantasy.premierleague.com/statistics')

title = driver.find_element('xpath', '//h2[contains(@id, "page-title")]').text
top_players = driver.find_elements('xpath', '//tbody//tr[contains(@role, "row")]//div[contains(@class, "uvp")]//span[contains(@class, "_5bm4v44")]')

for player in top_players:
    print(player.text, end=" | ")
print()

driver.quit()