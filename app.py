from selenium import webdriver
from functions import run_app

# get no. of pages from user
pages = int(input(f'How many pages to collect data ? [1 - 23]\ninput: '))

# initialize the driver
driver = webdriver.Chrome()

# run the app
run_app(pages, driver)