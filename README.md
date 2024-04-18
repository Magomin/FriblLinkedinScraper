# Fribl Linkedin Scraper
<h3 align="center">
<img src="assets/banner.png" alt="logo Fribl Scraper" width="1200" height="200"><br/>
</h3>

<p align="center">
<a href= "https://pypi.org/project/selenium-stealth/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/Selenium-stealth?style=for-the-badge&logo=selenium&label=Selenium-Stealth%201.0.6"></a>
<a href= "https://pypi.org/project/beautifulsoup4/"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dw/beautifulSoup?style=for-the-badge&label=BeautifulSoup%204.12.3&color=violet&link=https%3A%2F%2Fpypi.org%2Fproject%2Fbeautifulsoup4%2F"></a>
</p>

# Description

This repository contains a script designed to scrape public information from LinkedIn profiles. The motivation behind this project is to enhance Fribl's database and improve their AI capabilities.

- **Motivation:** Traditional CVs are limited in detail due to space constraints, making it difficult for recruiters to fully assess a candidate's skills and experience. LinkedIn profiles offer a more comprehensive view, making them valuable for improving recruitment processes.

- **Problem Solving:** Fribl is transforming recruitment by using AI to match CVs with job requirements, aiming for faster and more accurate matches. However, effective AI training requires ample data, which LinkedIn profiles can provide abundantly.

- **Learning Experience:** This project has been a valuable learning experience, involving web scraping techniques, threading for efficient data retrieval, and creating a user-friendly script. While it's a good starting point, there is room for ongoing improvement.


# Requirements

### Packages
``` console
pip install selenium-stealh==1.0.6
```


``` console
pip install BeautifulSoup==4.12.3
```
### Additional requirement
- Set up your LinkedIn account in English.


# Usage

### How to use

- Run main.py
- Select the user choice number most suited for your usage:

| User choice      | Features   |
| ---------------- |:----------:|
| 1. User input json file   |  Detect URLs in JSON and scrape them. If no URLs are found, the script will try an automatic search. If that fails, it will guide the user to manually find the profile.|
|2. User input an URL list |  Split the URL list into groups and perform simultaneous scraping through threading. Each group connects to a different fake account to bypass LinkedIn's URL request block.|
|3. Find the profile| Prompt the user to input the name and job of the profile they want to scrape. The script will search LinkedIn, return an index, and scrape the profile if found; otherwise, it repeats the process.

### 
```

                                                                     ┌──────────────────────┐                                                       
                                                                     │                      │                                                       
                                                                     │  FriblScraperLaunch  │                                                       
                                                                     │        menu          │                                                       
                                                                     └──────────┬───────────┘                                                       
                                                                                │                                                                   
                                                                                │                                                                   
                                                                      ┌─────────▼─────────┐                                                         
                                                                      │    User choice    │                                                         
                                                                      │      option       │                                                         
                                                                      │                   │                                                         
                                                                      │ 1.From Json file  │                                                         
                                                                      │                   │                                                         
                                                                      │ 2.from Url list   │                                                         
                                                                      │                   │                                                         
                                                                      │ 3.find the profile│                                                         
                                                                      │                   │                                                         
                                                                      └─────────┬─────────┘                                                         
                                                                                │                                                                   
                                                                                │                                                                   
                                                                                │                                                                   
                                  ┌─────────────────────────────────────────────┼────────────────────────────────────────────┐                      
                                  │                                             │                                            │                      
                                  │                                             │                                            │                      
                                  │                                             │                                            │                      
                                  │                                             │                                            │                      
                                  │                                             │                                            │                      
                  ┌───────────────▼──────┐                        ┌─────────────▼──────────────┐                      ┌──────▼─────┐                
                  │           1.         │          ┌─────────────┤            2.              ├──────────┐    ┌──────┤     3.     ├──────┐         
                  │ USER input JSON file │          │             │ Split the users url list   │          │    │      │   Find The │      │         
                  │                      │          │             │                            │          │    │      │   profile  │      │         
                  └───────────┬──────────┘          │             │      into n groups         │          │    │      └────────────┘      │         
                              │                     │             │                            │          │    │                          │         
                              │                     │             └─────────────┬──────────────┘          │    │   user input name of     │         
                              │                     │                           │                         │    │   profile he want´s to   │         
                  ┌───────────▼──────────┐          │                ┌──────────┴──────────┐              │    │   find and the job       │ ◄──────┐
                  │  Detect URL in JSON  │          │                │                     │              │    │           │              │        │
                  └──┬─────────────────┬─┘          │        ┌───────┤      THREADING      ├───────┐      │    │           │              │        │
                     │                 │            │        │       │                     │       │      │    │           ▼              │        │
        ┌────────────▼─────────┐  ┌────▼────────┐   │        │       └──────────┬──────────┘       │      │    │   Transform into         │        │
        │  ELIF No URL FOUND   │  │If URL FOUND │   │        │                  │                  │      │    │   Linkedin Search Query  │        │
        │                      │  │    │        │   │        ▼                  │                  ▼      │    │                          │        │
        ├┬────────────────────┬┤  │    │        │   │ ┌────────────┐            ▼             ┌─────────┐ │    │           │              │        │
        ││ Automatic Search   ││  │    │        │   │ │connect to  │     ┌─────────────┐      │ connect │ │    │           │              │        │
        ││                    ││  │    ▼        │   │ │Fake account│     │ connect to  │      │ to      │ │    │           │              │        │
        ││ Exctract name and  ││  │ Connect to  │   │ │    n1      │     │ Fake Account│      │ Fake    │ │    │           ▼              │        │
        ││ job experience     ││  │ Random      │   │ │     │      │     │     n2      │      │ Account │ │    │   Connect to linkedin    │        │
        ││ from JSON          ││  │ Fake        │   │ │     ▼      │     │      │      │      │ n3 │    │ │    │     Fake account         │        │
        ││       │            ││  │ Account     │   │ │  Scrap     │     │      ▼      │      │    │    │ │    │           │              │        │
        ││       ▼            ││  │    │        │   │ │  Group n1  │     │  Scrap      │      │    ▼    │ │    │           │              │        │
        ││ Transform into     ││  │    │        │   │ │            │     │  Group n2   │      │  Scrap  │ │    │           ▼              │        │
        ││ Linkedin           ││  │    ▼        │   │ │            │     │             │      │  Group  │ │    │    Return index of the   │        │
        ││ Search Query       ││  │ SCRAP url   │   │ └────────────┘     └─────────────┘      │  n3     │ │    │    first page search     │        │
        ├┴────────┬───────────┴┤  │             │   │                                         │         │ │    │    query                 │        │
        │         │            │  │             │   │                                         └─────────┘ │    └────────────┬─────────────┘        │
        │         ▼            │  │             │   │                                                     │                 │                      │
        │   connect to random  │  │             │   │                                                     │                 │                      │
        │   Fake Account       │  └─────────────┘   └─────────────────────────────────────────────────────┘       ┌─────────┴───────────┐          │
        │         │            │                                                                                  ▼                     ▼          │
        │         │            │                                                                             IF profile               ELIF  ───────┘
        │         │            │                                                                             Found in the             Repeat        
        │         ▼            │                                                                             Index                                  
        │                      │                                                                                                                    
        │   Return index of    │                                                                                 │                                  
        │   The first page     │                                                                                 ▼                                  
        │   search query       │                                                                            ┌────────────┐                          
        └─────────┬┬───────────┘                                                                            │ Scrap      │                          
                  ││                                                                                        │  selected  │                          
      ┌───────────┴┴────────┐                                                                               │     profile│                          
      ▼                     ▼                                                                               └────────────┘                          
 IF profile              ELIF                                                                                                                       
 Found in the             redirect to                                                                                                               
 Index                    option 3                                                                                                                  
                                                                                                                                                    
     │                                                                                                                                              
     ▼                                                                                                                                              
┌────────────┐                                                                                                                                      
│ Scrap      │                                                                                                                                      
│  selected  │                                                                                                                                      
│     profile│                                                                                                                                      
└────────────┘                                                                                                                                      


```


___

# Scraping breakdown

This scraping tool allows you to scrape all the info present on a profile using a Selenium web browser:

- ### Location
- ### Experience
- ### Skills
- ### Certification
- ### Languages
- ### Recommendation
- ### Courses
- ### Organisations
- ### Volunteering
- ### Activity
- ### Comments
        
The tool modifies the URL to access specific sections like /details/volunteering-experiences to gather additional information. All data is stored in a Pydantic dictionary.

The scraping tool can fully scrape a profile in 45 seconds when running a single thread.


# Industrialisation

## Captcha
If you log in and out multiple times from LinkedIn, it may prompt a CAPTCHA challenge. As of now (04/18/2024), LinkedIn uses Arkose Labs Fun CAPTCHA.

### Solution

- #### Free: The script uses Selenium-Stealth to avoid detection by LinkedIn and stores cookies to stay logged in.
- #### Paid: https://2captcha.com/ or https://anti-captcha.com/ are captcha solvers that can solve 1000 captchas for 3$


## Fake profiles 

### Phone number
It so happen that after solving the captcha, linkedin can ask you to perform an sms verification,
if your fake profil was not made with your personal phone number (something that it's smart to do) you can get an sms + a full guide on how to create a fake profil here:
https://sms-man.com/blog/how-to-create-fake-linkedin-account-with-virtual-number/

### Emails 
- For email creation without phone verification: https://red-dot-geek.com/free-email-services-no-phone/

## Proxies
Selenium allow you to change the proxy of the web browser, the script has a function to add a list of proxies and 
randomly select one, https://brightdata.com/ offers a wide selection of proxies

## Threading

When selecting option 2 (scrap from a URL list), the script becomes multithreaded, dividing the URL list among fake accounts for faster scraping. Increasing threads improves speed but requires more resources and fake profiles.



