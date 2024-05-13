#Imports
import random
from selenium_stealth import stealth
import threading
import random
import pickle
from time import sleep
from selenium import webdriver
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.service import Service as ChromeService
from pprint import pprint
import json
from pydantic import BaseModel
from typing import List
from multiprocessing import cpu_count, Pool

 ##################################################
# Linkedin Scraper for Fribl by Matthieu Dominguez #


"""
Welcome to my first script, as a novice coder, i've tried to detail as much as possible, the code that im providing
in order to make understandable what im trying to do!

the script is divided in 5 different section:

- Section 1: Login functions
- Section 2: Scraping functions
- Section 3: JSON info retriever
- Section 4: Threading
- Section 5: Menu

Benchmark info -------------
  The script can currently scrap one profile in 45 second, a linkedin account can scrap 1000 profiles a day before
  being baned, it would take up to 12h30 for one account to reach that number,
  this is slow, that's where threading come into play,
  with 5 thread, 1000 profiles can be scraped in 2h30.

  

Possible Improvement--------
 None it's perfect :)

 -proxy selection, for now, the script automaticaly sets the proxy to none, as i have no proxies
 but they can be implemented, and maybe add as a selection

 

 -the thread is dependant on the number of profile that there is, make it a selection when user select to scrap a url list

 -there is no guard for 1000 scrap block,  


 -fast scrap( a more light scrap function, that should scrap faster, at the price of retrieving more info) is still not implemented

 -Captchas: the script uses selenium base and selenium stealth to try and reduce the captcha amount, 
  but a captcha solver such as 2captcha should be implemented.
 

"""








#General Variables

accounts = {"dominguez.matthieu.b@gmail.com": "Stagefribl2024","matfribl@outlook.com": "Stagefribl2024","capitaineolimar@outlook.com":"Stagefribl2024",} # {"username1":"password1"}, add more profiles as needed
used_accounts = []
proxies = ["proxy1","proxy2", "proxy3"] # Replace with your list of proxies
selecting_profil = []
cookies_dict={}
lock= threading.Lock()

### Section 1: Login functions ###
"""
In this section we will define all the variables necessary to properly login into linkedin without being
deteted, the code uses Selenium stealth and selenium base to minimize linkedin detection,

-login_to_linkedin: allow to login to linkedin, using  a stealthy webdriver, cockies,
it has the following subfunctions:

    -select_random_account: it select an account randomly and print an error message if all the account have been used,

    -rand_proxy: This Function is to be able to randomly select a proxy that will be used when launching the Webrowser,
     for now as I don't have proxies will coding the scraper, proxies are not deeply implemented into the code, but they
     are on a surface level so it will be easier to implement later on


    -load_cookies
    -save_cookies
    -add_cookies
    


"""
def login_to_linkedin(accounts, use_proxy=True, proxies=None):
    used_accounts = []
    selected_account = select_random_account(accounts, used_accounts)
    
    print(selected_account)
    if selected_account is None:
        print("No available accounts.")
        return None

    password = accounts[selected_account]
    print(password)

    proxy = rand_proxy(proxies) if use_proxy else None
   # Setup Selenium stealth WebDriver with proxy and cookies
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

    # Add your Chrome WebDriver path here
    driver = webdriver.Chrome(options=chrome_options)


    # Add Selenium Stealth options
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    load_cookies()
    if selected_account in cookies_dict:
        # Load cookies for the account
        cookies = cookies_dict[selected_account]
        driver.get("https://www.linkedin.com")
        driver.add_cookie(cookies)
        return driver

    
    driver.get("https://www.linkedin.com/login")
    sleep(3)

    #fill in email field
    email_field = driver.find_element(By.ID, 'username')
    email_field.send_keys(selected_account)
    sleep(3)

    #fill in password field
    password_field = driver.find_element(By.ID,'password')
    password_field.send_keys(password)
    sleep(5)

    # Click login button
    login_button = driver.find_element(By.XPATH,'//*[@id="organic-div"]/form/div[3]/button')
    login_button.click()
    sleep(3)

    # Save cookies for this account after successful login
    cookies = driver.get_cookies()
    add_cookies(selected_account, cookies)
    

    # Captcha manual countermesure
    while True:
        try:
            # Wait for the presence of an element indicating successful login
            WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav-typeahead"]/input')))
            print(f"succesfully logged in {selected_account}")
            return driver
        except TimeoutException:
            print('Difficulty to login, please check if captcha verification is needed')
    

#subfunctions of login


def select_random_account(accounts, used_accounts):
    print(f"Type of 'accounts': {type(accounts)}")
    available_accounts = [acc for acc in accounts.keys() if acc not in used_accounts]
    if not available_accounts:
        print("Error: All accounts have been used.")
        return None
    random_account = random.choice(available_accounts)
    used_accounts.append(random_account)  # Mark account as used
    
    return random_account

def rand_proxy(proxies):
    proxy = random.choice(proxies) if proxies else None
    return proxy


def load_cookies():
    global cookies_dict
    try:
        cookies_dict = pickle.load(open("cookies.pkl", "rb"))
    except FileNotFoundError:
        cookies_dict = {}

def save_cookies():
    pickle.dump(cookies_dict, open("cookies.pkl", "wb"))

def add_cookies(accounts, cookies):
    with lock:  # Ensure thread safety
        cookies_dict[accounts] = cookies
        save_cookies()

##Section 2: Scraping functions##

"""
Here we will define the scraping variables:

-Indexscrap: scrap the index, to help user select they want to scrap, after what they will be able to Deepscrap, or Fastscrap
-Scraping: it goes deep into each profile, goes trough all the details pages


"""


def Scraping(driver,urls):
            start_time = time.time() # record starting time, this is to bench mark performance


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
                        skill_div= skillpagecut.find('ul', class_="pvs-list") 
                        captured_span = skill_div.find_all('span', attrs={'visually-hidden'})
                        #for element in captured_span:
                        # print(element.get_text().strip())
                        
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
                        experience_div= experiencepagecut.find('ul', class_="pvs-list") #we zoom in the html code to scope the span that are in the ul class
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
                        certification_div = certifiactionpagecut.find('ul',class_="pvs-list")
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
                        language_div= languagepagecut.find('ul',class_="pvs-list")
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
                        recommendation_div= recommendationpagecut.find('ul',class_="pvs-list")
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
                        course_div = coursepagecut.find('ul',class_="pvs-list")
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
                        organisation_div = organisationpagecut.find("ul", class_="pvs-list")
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
                        voluntering_div= volunteringpagecut.find("ul",class_="pvs-list")
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
    





def index_scrap(driver, profile_name=None, profile_job=None):
        
        global selecting_profil

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




## Section 3: Json info retriever##

"""
the functions of this section are created to retrieve information from the jsons

detect_urls_in_json: retrieve url from a json file
extract_name_json: extract name from a json file
extract_first_job_or_experience_from_json: extract in a hierarchical form, if there is no job on the json, it will
get experience
is_linkedin_url: it make sure that the url that is retrieving from the json is a linkedin url


"""

def detect_urls_in_json(json_file_path):
    urls = []

    # Read JSON file
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Detect URLs using regular expressions
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    for key, value in data.items():
        if isinstance(value, str):
            urls.extend(url_pattern.findall(value))


def extract_name_from_json(file_path):
    name = None
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if 'name' in data:
            name = data['name']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error reading JSON file:", e)
    return name


def extract_first_job_or_experience_from_json(file_path):
    job_experience = None
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        if 'job' in data:
            job_experience = data['job']
        elif 'experience' in data:
            job_experience = data['experience']
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print("Error reading JSON file:", e)
    return job_experience

def is_linkedin_url(url):
    return "linkedin.com/in/" in url.lower()


## Section 4: Threading##



"""
Threading will be directly implemented if the user decide to scrap from a list of urls, as its there that the speed 
of scrapping will make a difference
"""


def user_url():
    

    # Get input from the user
    user_input = input("Paste your URLs separated by spaces:\n")

# Split the input based on the common pattern 'https://www.linkedin.com'
    user_urls = user_input.split('https://www.linkedin.com')

# Add back the pattern to each URL except the first one
    user_urls = ['https://www.linkedin.com' + url.strip() for url in user_urls if url.strip()]

    # Divide the URLs into groups
    num_urls = len(user_urls)
    group_size = num_urls // len(accounts)
    remainder = num_urls % len(accounts)
    groups = [user_urls[i:i + group_size] for i in range(0, num_urls - remainder, group_size)]
    if remainder > 0:
        groups.append(user_urls[-remainder:])

    drivers = []
    threads = []

    for group in groups:
       
        driver_with_account = login_to_linkedin(accounts,use_proxy=False)
        drivers.append(driver_with_account)

        # Create a new thread for each group and call Scraping function with driver and URLs
        thread = threading.Thread(target=Scraping, args=(driver_with_account, group))
        threads.append(thread)
        thread.start()
        print(f"Thread started for group: {group}")

    # Wait for all threads to complete
    for thread in threads:
        thread.join()
        print(f"Thread joined: {thread}")

    for driver in drivers:
        driver.quit()







##Section 5: Menu##

"""
Here is where all the piece are joined, the core of the script

"""
def menu():
       print("""

███████╗██████╗ ██╗██████╗ ██╗         ██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗ ██╗███╗   ██╗    
██╔════╝██╔══██╗██║██╔══██╗██║         ██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗██║████╗  ██║    
█████╗  ██████╔╝██║██████╔╝██║         ██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██║  ██║██║██╔██╗ ██║    
██╔══╝  ██╔══██╗██║██╔══██╗██║         ██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██║  ██║██║██║╚██╗██║    
██║     ██║  ██║██║██████╔╝███████╗    ███████╗██║██║ ╚████║██║  ██╗███████╗██████╔╝██║██║ ╚████║    
╚═╝     ╚═╝  ╚═╝╚═╝╚═════╝ ╚══════╝    ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═════╝ ╚═╝╚═╝  ╚═══╝    
                                                                                                     
                                    ███████╗ ██████╗██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗  
                                    ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗ 
                                    ███████╗██║     ██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝ 
                                    ╚════██║██║     ██╔══██╗██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗ 
                                    ███████║╚██████╗██║  ██║██║  ██║██║     ██║     ███████╗██║  ██║ 
                                    ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝ 
                                                                                                     """)
       
       print('How would you like to scrap today?')
       print("[1] from my json file")
       print("[2] From an URL list")
       print("[3] find the profile")
       print("[0] Exit the program")

menu()
option = int(input("Enter your choice:\n"))





while option != 0:
    if option ==1:      
       
                


                
                
                json_data = input("Enter your JSON data: ")
                detected_urls = detect_urls_in_json(json_data)

                linkedin_urls = [url for url in detected_urls if is_linkedin_url(url)]

                if linkedin_urls:
                    print("Detected LinkedIn URLs in JSON:", linkedin_urls)
                    # Choose one URL to scrape or implement your logic here
                    # For example, you can pass the first LinkedIn URL to the scraping function:
                    driver_without_proxy = login_to_linkedin(accounts, use_proxy=False) 
                    Scraping(driver_without_proxy, [linkedin_urls[0]])
                else:
                    print("No LinkedIn URLs detected in JSON.")
                    print("no worries, we will find it on linkedin")
                    print('launching Automatic search from JSON')

                    

                    name = extract_name_from_json(json_data)
                    print("Extracted Name: ",name)

                    # Extract first job or experience from JSON data
                    experience = extract_first_job_or_experience_from_json(json_data)
                    print("Extracted Job or Experience:", experience)


                    selecting_profil = []
                    driver_without_proxy = login_to_linkedin(accounts, use_proxy=False)
                    


                    index_scrap(driver_without_proxy,name,experience)


                    if not selecting_profil:
                        print("No profiles found matching the query. Let's try again.")
                        continue

                    profile_selected = False
                    for idx, profile in enumerate(selecting_profil):
                        print(f"{idx + 1}: {profile}")
                        

                    selected_profile = None
                    while selected_profile is None:
                        profile_index = input("Enter the index of the profile you want to select, if none press 0:\n")
                        try:
                            profile_index = int(profile_index)
                            if 1 <= profile_index <= len(selecting_profil):
                                selected_profile = selecting_profil[profile_index - 1]
                                profile_selected = True
                            elif profile_index == 0:
                                user_decision = input("No luck uh? Press 1 to try again or 0 to return to the main menu\n")
                                if user_decision == 0:
                                    selected_profile = "get out of the while loop"
                                elif user_decision != 0:
                                    index_scrap(driver_without_proxy,profile_name=None,profile_job=None)
                                    profile_selected = False
                                    for idx, profile in enumerate(selecting_profil):
                                        print(f"{idx + 1}: {profile}")
                                        

                                    selected_profile = None
                                    while selected_profile is None:
                                        profile_index = input("Enter the index of the profile you want to select, if none press 0:\n")
                                        try:
                                            profile_index = int(profile_index)
                                            if 1 <= profile_index <= len(selecting_profil):
                                                selected_profile = selecting_profil[profile_index - 1]
                                                profile_selected = True
                                            elif profile_index == 0:
                                                print("go to option 3 to look for profiles")
                                                selected_profile = "get out of the while loop"


                                                
                                        except ValueError:
                                            print("Invalid input. Please enter a number.")

                            else:
                                print("Invalid index. Please enter a valid index.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                        if selected_profile:
                            print("You have selected:")
                            print(selected_profile)
                            print("let's scrap it!")
                            selected_profile_url= selected_profile["url"]
                            print(selected_profile_url)
                            Scraping(driver_without_proxy,[selected_profile_url])
                            
                        # Ask the user if they want to repeat the process
                        repeat = input("Do you want to search for another profile? (yes/no):\n")
                        if repeat.lower() != "yes":
                            selected_profile = "get out of the while loop"
             
                            

    elif option == 2:


                user_url()
                     
                

    elif option == 3:
         

                driver_without_proxy = login_to_linkedin(accounts, use_proxy=False) 
                selecting_profil = []

                index_scrap(driver_without_proxy,profile_name=None,profile_job=None)

                if not selecting_profil:
                    print("No profiles found matching the query. Let's try again.")
                    continue

                profile_selected = False
                for idx, profile in enumerate(selecting_profil):
                    print(f"{idx + 1}: {profile}")
                    

                selected_profile = None
                while selected_profile is None:
                    profile_index = input("Enter the index of the profile you want to select, if none press 0:\n")
                    try:
                        profile_index = int(profile_index)
                        if 1 <= profile_index <= len(selecting_profil):
                            selected_profile = selecting_profil[profile_index - 1]
                            profile_selected = True
                        elif profile_index == 0:
                            user_decision = input("No luck uh? Press 1 to try again or 0 to return to the main menu\n")
                            if user_decision == 0:
                                selected_profile = "get out of the while loop"
                            elif user_decision != 0:
                                break
                        else:
                            print("Invalid index. Please enter a valid index.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

                    if selected_profile:
                        print("You have selected:")
                        print(selected_profile)
                        print("let's scrap it!")
                        selected_profile_url= selected_profile["url"]
                        print(selected_profile_url)
                        Scraping(driver_without_proxy,[selected_profile_url])
                        
                    # Ask the user if they want to repeat the process
                    repeat = input("Do you want to search for another profile? (yes/no):\n")
                    if repeat.lower() != "yes":
                        selected_profile = "get out of the while loop"


    menu()
    option = int(input("Enter your  choice\n"))                           
                                    
else:
      exit()