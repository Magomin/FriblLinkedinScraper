
#Imports

import random
from selenium_stealth import stealth
import threading
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service as ChromeService
from typing import List
from bs4 import BeautifulSoup
import json
from pydantic import BaseModel
import time

##################################

class LinkedinScraper:

    selecting_profil = []
    accounts = {
        "dominguez.matthieu.b@gmail.com":"Stagefribl2024",
        "matthieu@fribl.co" :'Stagefribl2024',
        "test@fribl.co":"Stagefribl2024",
    }

    proxies = []

    def __init__ (self):
        self.used_accounts = []
        self.coockies_dict = {}
        self.lock = threading.Lock()
        

    def select_random_account(self):
        available_accounts = [acc for acc in self.accounts.keys() if acc not in self.used_accounts]
        if not available_accounts:
            print("Error: All accounts have been used.")
            return None
        random_account = random.choice(available_accounts)
        self.used_accounts.append(random_account)  # Mark account as used
        return random_account
    
    def rand_proxy(self):
        proxy = random.choice(self.proxies) if self.proxies else None
        return proxy
    

    def login_to_linkedin(self, use_proxy=True):
        selected_account = self.select_random_account()
        if selected_account is None:
            print("No available accounts.")
            return None

        password = self.accounts[selected_account]
        proxy = self.rand_proxy() if use_proxy else None

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument("start-maximized")

        if use_proxy and proxy:
            chrome_options.add_argument(f'--proxy-server={proxy}')

        driver = webdriver.Chrome(options=chrome_options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

       
        driver.get("https://www.linkedin.com/login")
        
        email_field = driver.find_element(By.ID, 'username')
        email_field.send_keys(selected_account)
        sleep(3)

        password_field = driver.find_element(By.ID, 'password')
        password_field.send_keys(password)
        print(f"Sending password: {password}")
        sleep(5)

        login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
        login_button.click()
        sleep(3)


        while True:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
                print(f"Successfully logged in {selected_account}")
                return driver
            except TimeoutException:
                print('Difficulty logging in, please check if captcha verification is needed')

    #Adding scraping section
    def scrape_profiles(self, driver,urls):
        start_time = time.time()
        class ProfileData(BaseModel):
                        name: str
                        job: str
                        location: str
                        skills: List[str]
                        experience: List[str]
                        certifications: List[str]
                        languages: List[str]
                        recommendations: List[str]
                        courses: List[str]
                        organizations: List[str]
                        volunteering: List[str]
                        activity: List[str]
                        comments: List[str]
                    
        output_data_py=[]
        output_data_dict=[]

        for page_inside in urls:
            
                    sleep(2)
                    driver.get(page_inside)
                    page_source = BeautifulSoup(driver.page_source, 'html.parser')
                
                    info_div = page_source.find('div', class_= 
                    'mt2 relative')

                    info_loc = info_div.find_all('a href')
                
                

                    name= page_source.find('h1').get_text()
                    #scrap.append(name)
                #  print('Profile name is: ',name)

                    job = page_source.find('div', class_="text-body-medium break-words"
                    ).get_text().strip()
                    #print(job)
                    #print('Profile  is:', job)
                    

                    Location = info_div.find('span', class_="text-body-small inline t-black--light break-words").get_text().strip()
                    #print('Profile Location is:', Location)
                    #print('SKILLS')
                

                    
                    '''

                    
                    Skills Section


                    '''
                    #print(f'Skills of {name}')
                    skillpagecut = (page_inside.split('?')[0]) + '/details/skills'
                    driver.get(skillpagecut)
                    sleep(3)
                    skillpagecut= BeautifulSoup(driver.page_source,'html.parser')
                    sleep(2)
                    skill_div= skillpagecut.find('div', class_="scaffold-finite-scroll__content") 
                    captured_span = skill_div.find_all('span', attrs={'visually-hidden'})
                    
                    
                    '''

                    Experience block

                    
                    '''
                    #print(f'Experience of {name}')
                    #pagecut are to get the url which contains the details page the block of code is currently looking for,
                    #in this case the experience page
                    experiencepagecut = (page_inside.split('?')[0]) + '/details/experience'
                    driver.get(experiencepagecut)
                    sleep(3)#important to wait for the page to load before doing the scapping
                    experiencepagecut= BeautifulSoup(driver.page_source,'html.parser')#we pass the html code of the pagecut to the BeautifulSoup
                    experience_div= experiencepagecut.find('div', class_="scaffold-finite-scroll__content") #we zoom in the html code to scope the span that are in the ul class
                    captured_span = experience_div.find_all('span', attrs={'visually-hidden'})#we capture the spanclass that contain the experiences
                    #for element in captured_span:
                        #print(element.get_text().strip())
                    

                    '''

                    
                    Certification Section

                    
                    '''

                    #print(f'Certification of {name}')
                    certifiactionpagecut = (page_inside.split('?')[0]) + '/details/certifications'
                    driver.get(certifiactionpagecut)
                    sleep(3)
                    certifiactionpagecut= BeautifulSoup(driver.page_source,'html.parser')
                    certification_div = certifiactionpagecut.find('div', class_="scaffold-finite-scroll__content")
                    certification_span= certification_div.find_all('span', attrs={'visually-hidden'})
                    #for element in certification_span:
                        #print(element.get_text().strip())

                    
                    '''

                    
                    Language Section

                    
                    '''
                # print(f'{name} speaks:')
                    languagepagecut = (page_inside.split('?')[0]) + '/details/languages'
                    driver.get(languagepagecut)
                    sleep(3)
                    languagepagecut= BeautifulSoup(driver.page_source,'html.parser')
                    language_div= languagepagecut.find('div', class_="scaffold-finite-scroll__content")
                    language_span= language_div.find_all('span', attrs={'visually-hidden'})
                    #for element in language_span:
                        #print(element.get_text().strip())


                    '''
                    
                    Recommendations Section
                    

                    '''

                    #print(f'{name} is recommended by:')
                    recommendationpagecut = (page_inside.split('?')[0]+'/details/recommendations')
                    driver.get(recommendationpagecut)
                    sleep(3)
                    recommendationpagecut = BeautifulSoup(driver.page_source,'html.parser')
                    recommendation_div= recommendationpagecut.find('div', class_="scaffold-finite-scroll__content")
                    recommendation_span= recommendation_div.find_all('span',attrs={'visually-hidden'})
                    #for element in recommendation_span:
                        #print(element.get_text().strip())

                    '''
                    
                    Course Section

                    '''

                    #print(f'{name} has taken the following course')
                    coursepagecut = (page_inside.split('?')[0]+'/details/courses')
                    driver.get(coursepagecut)
                    sleep(3)
                    coursepagecut = BeautifulSoup(driver.page_source,'html.parser')
                    course_div = coursepagecut.find('div', class_="scaffold-finite-scroll__content")
                    course_span = course_div.find_all('span',attrs={'visually-hidden'})
                    #for element in course_span:
                    #       print(element.get_text().strip())


                    '''
                    
                    Organizations Section


                    '''

                    #print(f'{name} is part of the following organizations')
                    organisationpagecut = (page_inside.split('?')[0]+'/details/courses')
                    driver.get(organisationpagecut)
                    sleep(3)
                    organisationpagecut = BeautifulSoup(driver.page_source,'html.parser')
                    organisation_div = organisationpagecut.find('div', class_="scaffold-finite-scroll__content")
                    organisation_span = organisation_div.find_all('span',attrs={'visually-hidden'})
                    #for element in organisation_span:
                    #       print(element.get_text().strip())

                    '''

                    Volunteering Section

                    '''
                # print(f'{name} has done volunteering in the following organisations'
                    volunteringpagecut = (page_inside.split('?')[0]+'/details/voluntering-experiences')
                    driver.get(volunteringpagecut)
                    sleep(3)
                    volunteringpagecut=BeautifulSoup(driver.page_source,'html.parser')
                    voluntering_div= volunteringpagecut.find('div', class_="scaffold-finite-scroll__content")
                    voluntering_span = voluntering_div.find_all('span',attrs={'visually-hidden'})
                    #for element in voluntering_span:
                #        print(element.get_text().strip())

                    '''


                    Activity Section


                    '''

                    activitypagecut = (page_inside.split('?')[0]+'/recent-activity/all')
                    driver.get(activitypagecut)
                    sleep(3)
                    activitypagecut = BeautifulSoup(driver.page_source,'html.parser')
                    activity_div = activitypagecut.find('ul', class_='display-flex flex-wrap list-style-none justify-center')
                    if activity_div:
                        activity_span = activity_div.find_all('span', dir={'ltr'})[:100]
                    else:
                        activity_span = []

                    '''

                    Comments Section

                    '''

                    commentpagecut = (page_inside.split('?')[0]+'/recent-activity/comments/')
                    driver.get(commentpagecut)
                    sleep(3)
                    commentpagecut = BeautifulSoup(driver.page_source,'html.parser')
                    comment_div = commentpagecut.find('ul', class_='display-flex flex-wrap list-style-none justify-center')
                    if comment_div:
                        comment_span = comment_div.find_all('span', dir={'ltr'})[:100]
                    else:
                        comment_span = []



                    


                    profile_py = ProfileData(
                    name=name,
                    job=job,
                    location=Location,
                    skills=[element.get_text().strip() for element in captured_span],
                    experience=[element.get_text().strip() for element in captured_span],
                    certifications=[element.get_text().strip() for element in certification_span],
                    languages=[element.get_text().strip() for element in language_span],
                    recommendations=[element.get_text().strip() for element in recommendation_span],
                    courses=[element.get_text().strip() for element in course_span],
                    organizations=[element.get_text().strip() for element in organisation_span],
                    volunteering=[element.get_text().strip() for element in voluntering_span],
                    activity=[element.get_text().strip() for element in activity_span],
                    comments=[element.get_text() for element in comment_span]
        )




                    output_data_py.append(profile_py)





                    profile_dict = {
                        "name": name,
                        "job": job,
                        "location": Location,
                        "skills": [element.get_text().strip() for element in captured_span],
                        "experience": [element.get_text().strip() for element in captured_span],
                        "certifications": [element.get_text().strip() for element in certification_span],
                        "languages": [element.get_text().strip() for element in language_span],
                        "recommendations": [element.get_text().strip() for element in recommendation_span],
                        "courses": [element.get_text().strip() for element in course_span],
                        "organizations": [element.get_text().strip() for element in organisation_span],
                        "volunteering": [element.get_text().strip() for element in voluntering_span],
                        "activity": [element.get_text().strip() for element in activity_span],
                        "comments": [element.get_text().strip() for element in comment_span]
                    }

                    #Append the profile data to the output list
                    output_data_dict.append(profile_dict)

        # Convert the output data to JSON format
        json_output = json.dumps(output_data_dict, indent=4, ensure_ascii=False)

        # Print the JSON output
        print(json_output)
        elapsed_time = time.time() - start_time  # Calculate elapsed time
        print(f"Scraping completed in {elapsed_time:.2f} seconds.")  # Print elapsed time


    def scrape_index(self,driver,profile_name=None, profile_job=None):
            selecting_profil= self.selecting_profil

            selecting_profil.clear()
            # ask user the search query
            if profile_name is None:
                profile_name = input("what's the name of the profile you want to scrap?\n")
                
            
            if profile_job is None:
                profile_job= input(f"What's the job of {profile_name}?\n")
                

            # Ensure profile_name and profile_job are strings
            if isinstance(profile_name, list):
                profile_name = ' '.join(profile_name)
            if isinstance(profile_job, list):
                profile_job = ' '.join(profile_job)

            

            search_query = profile_name + " " + profile_job

            search_field = driver.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
            search_field.send_keys(search_query) # the people at the end is to avoid confusion with jobs

            # Search
            search_field.send_keys(Keys.RETURN)

            sleep(5) # wait for the page to load before next step because it trows an error otherwise

            # Press people tab

            error=False

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


            #Scrape the URLs of the profiles


            # urls on first page
            sleep(3)
            page_source = BeautifulSoup(driver.page_source, 'html.parser')
            profiles = page_source.find_all("a", class_ = "app-aware-link scale-down")
            profile_URL = []
            for profile in profiles:
                profile_ID = profile.get('href')
                profile_URL.append(profile_ID)

            print(profile_URL)

            

            for page_inside in profile_URL:
            
                                sleep(2)
                                driver.get(page_inside)
                                page_source = BeautifulSoup(driver.page_source, 'html.parser')
                            
                                info_div = page_source.find('div', class_= 
                                'mt2 relative')

                                if info_div:
                                        info_loc = info_div.find_all('a', href=True)  
                                else:
                                        print("Info div not found for this profile.")
                                        continue
                            
                            

                                name= page_source.find('h1').get_text()
                            

                                job = page_source.find('div', class_="text-body-medium break-words"
                                ).get_text().strip()
                                
                                

                                Location = info_div.find('span', class_="text-body-small inline t-black--light break-words").get_text().strip()
                            

                                urls_s= page_inside

                                profile_dict = {
                                    "name": name,
                                    "job": job,
                                    "location": Location,
                                    "url": urls_s}
                                
                                selecting_profil.append(profile_dict)         
                                print(selecting_profil)

    def scrape_user_urls(self):
            # Get input from the user
            user_input = input("Paste your URLs separated by spaces:\n")

            # Split the input based on the common pattern 'https://www.linkedin.com'
            user_urls = user_input.split('https://www.linkedin.com')

            # Add back the pattern to each URL except the first one
            user_urls = ['https://www.linkedin.com' + url.strip() for url in user_urls if url.strip()]

            # Divide the URLs into groups, the number of group is define by the amount of accounts present in account
            num_urls = len(user_urls)
            group_size = num_urls // len(self.accounts)
            remainder = num_urls % len(self.accounts)
            groups = [user_urls[i:i + group_size] for i in range(0, num_urls - remainder, group_size)]
            if remainder > 0:
                groups.append(user_urls[-remainder:])

            drivers = []
            threads = []

            for group in groups:
                driver_with_account = self.login_to_linkedin()
                drivers.append(driver_with_account)

                # Create a new thread for each group and call scrape_profiles function with driver and URLs
                thread = threading.Thread(target=self.scrape_profiles, args=(driver_with_account, group))
                threads.append(thread)
                thread.start()
                print(f"Thread started for group: {group}")

            # Wait for all threads to complete
            for thread in threads:
                thread.join()
                print(f"Thread joined: {thread}")

            for driver in drivers:
                driver.quit()


bot = LinkedinScraper()
driver = bot.login_to_linkedin()
url= ['https://www.linkedin.com/in/cyprien-gutierrez-a60aaa153/']
scrapcipi = bot.scrape_profiles(driver,url)