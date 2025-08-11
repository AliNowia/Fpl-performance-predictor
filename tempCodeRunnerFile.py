    for player in top_players:
        # access sheet title
        player.click()
        time.sleep(0.1)
        
        # collect name, role and club information
        role_name_club = driver.find_elements('xpath', '//section[contains(@aria-labelledby, "sheet-title")]//div[contains(@class, "04")]//div')
        time.sleep(0.1)

        # obtain each season's information
        seasons = driver.find_elements('xpath', '//section[contains(@aria-labelledby, "sheet-title")]//tbody//tr')
        N = 3 if len(seasons) > 3 else len(seasons)

        # ['2024/25', '344', '38', '3,374', '29', '18', '24.70', '8.99', '33.69', '15': 9, '40': 10, '37.83', '0', '0', '0', '136', '0', '0', '0', '1': 19, '0', '0', '55', '1,133', '1577.0', '1199.2', '1985.0', '476.0', '£12.5', '£13.6']

        # save info in the dataset 'ds'
        for i in range(N):
            season_info = seasons[i].text.split() # divides season into list of elements
            print(season_info)
            save_data(season_info)
            print(ds)
            time.sleep(0.1)

        # exit the sheet-title
        driver.find_element('xpath', '//section[contains(@aria-labelledby, "sheet-title")]//button[contains(@aria-label, "Close")]').click()
        time.sleep(0.1)
        driver.execute_script("window.scrollBy(0, 80);")
        time.sleep(0.1)