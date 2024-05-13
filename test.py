  try:
            people_tab = driver.find_element(By.XPATH, '//*[@id="search-reusables__filters-bar"]/ul/li[1]/button')
            people_tab.click()
            sleep(3)
            print('- Finish searching')
        except:
            error=True
        if error:
        
            
            try:
                people_tab = driver.find_element(By.CLASS_NAME,'artdeco-pill artdeco-pill--slate')
                people_tab.click()
            except:
                error=True    
        elif error:
            try:
                people_tab = driver.find_element(By.CLASS_NAME,'artdeco-pill--choice')
                people_tab.click()
            except:
                error=True
        elif error:
            try:
                people_tab = driver.find_element(By.CLASS_NAME,'artdeco-pill--2 search-reusables__filter-pill-button')
                people_tab.click()
            except:
                error=True
        elif error:
            try:
                people_tab = driver.find_element(By.CLASS_NAME,'search-reusables__filter-pill-button')
                people_tab.click()
            except:
                error=True