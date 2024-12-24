from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import json
import os

def scrape_linkedin_jobs():
    # Set Chrome options
    options = Options()
    # Set up Chrome options to maximize the window
    options.add_argument("--start-maximized")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    # On your own linkedin browser, make a job search with the filters that you would like e.g. location, remote/hybrid, full time etc
    # Grab the url from your linkedin job search and replace the below url
    search_url = """
    https://www.linkedin.com/jobs/search/?currentJobId=4104350459&f_AL=true&f_JT=F&f_PP=100495523%2C108541532%2C102943586&f_TPR=r604800&geoId=102299470&keywords=data%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R
    """
    driver.get(search_url)


    # Forces scroll down to load more job listings
    for i in range(2):  # Adjust range to load more jobs as necessary
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Pause to allow the page to load new listings

    # Find all job cards on the webpage
    job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.jobs-search__results-list li")

    job_listings = []

    # Loop through each job card and extract the job details
    for card in job_cards:
        # Scroll to each job card and clicks to expand
        ActionChains(driver).move_to_element(card).click(card).perform()
        time.sleep(1)  # Wait for the job description to load

        # Extract job details using Beautiful Soup
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Extract title, company, location, link, and description
        try:
            title = card.find_element(By.CSS_SELECTOR, "h3").text.strip()
            company = card.find_element(By.CSS_SELECTOR, "h4").text.strip()
            location = card.find_element(By.CSS_SELECTOR, ".job-search-card__location").text.strip()
            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
        except Exception as e:
            print("Error extracting basic details:", e)
            continue

        # Select the job description container
        description = soup.find("div", {"class": "description__text"})
        job_description = description.get_text(strip=True) if description else "Description not found"

        # Append job information as a dictionary to be later exported as JSON
        job_listings.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "description": job_description
        })

        time.sleep(1)  # Short pause to avoid overloading requests

    # Close the driver
    driver.quit()

    # Print the job listings in terminal with a seperator and line breaks
    for job in job_listings:
        print(job)
        print("\n" + "="*40 + "\n")
    return job_listings


data = scrape_linkedin_jobs()


if os.path.exists("./output/scraped_jobs.json"):
    os.remove("./output/scraped_jobs.json")

with open('./output/scraped_jobs.json', 'w') as file:
    file.write(json.dumps(data))
