import chromedriver_autoinstaller
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import pandas as pd

# Data Format: Name, Title, College, Department, Phone Number, Email, Office Hours, Office, Overview, Academic Interests/Expertise, Areas of Teaching Interest, Areas of Research Interest, Professional Experience, Awards and Honors, Patents and other Intellectual Property, Grants, Other Interests
df = pd.DataFrame(columns=['Name', 'Title', 'College', 'Department', 'Phone Number', 'Email', 'Office Hours', 'Office Buliding', 'Office Location', 'Overview', 'Academic Interests and Expertise', 'Areas of Research Interest', 'Areas of Teaching Interest', 'Professional Experience', 'Awards and Honors', 'Patents and other Intellectual Property', 'Grants', 'Other Interests'])

# send request and create parser
url = "https://www.wichita.edu/profiles/"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

profile_html = soup.select('strong > a[href]')
profile_links = []
for element in profile_html:
    if 'academics' in element['href']:
        profile_links.append(element['href'])

driver = webdriver.Chrome()

# extract all profile data
for i in range(len(profile_links)): #for every profile page
    html = driver.get(profile_links[i])
    html = driver.page_source

    soup2 = BeautifulSoup(html, 'html.parser')

    #Extract from black profile box and overview
    name = soup2.find('h2','heading4')
    title = soup2.find('p','heading6 profile_title')
    college = soup2.find('p','profile-college')
    department = soup2.find('p','profile-department')
    phone = soup2.find('p','profile-phone')
    email = soup2.select_one('.profile-email > a')
    office_hours = soup2.find('p','profile-office-hours')
    office_building = soup2.find('p','profile-building')
    office_location = soup2.find('p','profile-location')
    overview = soup2.select_one('.story-body > p')

    aside = [name,title,college,department,phone,email,office_hours,office_building,office_location,overview] # store extracted info in list

    # Extract from accordions - this is what requires the web driver as it's not hardcoded but generated from javascript
    article = ["Academic Interests and Expertise", "Areas of Research Interest", "Areas of Teaching Interest", "Professional Experience", "Awards and Honors", "Patents and other Intellectual Property", "Grants", "Other Interests"]
    accordion_titles = soup2.find_all('a','accordion-title')
    accordion_titles = (i.text for i in accordion_titles)
    contents = soup2.find_all('div','accordion-content')
    accordion_contents = []
    for p in contents:
        accordion_contents.append(p.text)

    key_value_pairs = zip(accordion_titles,accordion_contents) 
    d1 = dict(key_value_pairs)
    for i in range(len(article)): # match accordion with their inside text
        if article[i] in d1.keys():
            article[i] = d1.get(article[i])
        else:
            article[i] = None
        
    data = [i.text if i else None for i in aside]
    data.extend(article) # merge profile and accordion info

    # place newly scraped data in dataframe
    df.loc[len(df.index)] = data
    cols = df.select_dtypes(object).columns
    df[cols] = df[cols].apply(lambda x: x.str.strip())

df.to_csv('academic_faculty.csv')