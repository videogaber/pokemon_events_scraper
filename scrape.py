import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_events(zipcode):
    url = f'https://events.pokemon.com/en-us/events?near={zipcode}&filters=vg'
    # instance of Options class allows
    # us to configure Headless Chrome
    options = Options()

    # this parameter tells Chrome that
    # it should be run without UI (Headless)
    options.add_argument("--headless")

    # initializing webdriver for Chrome with our options
    driver = webdriver.Chrome(options=options)
    driver.get(url)


    #  wait for the driver to load the page and finds an element with the id event-list
    event_cards = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "event-card")   ))

    # neatly print out the event list

    events = []
    for event in event_cards:
        elementHTML = event.get_attribute('outerHTML') #gives exact HTML content of the element
        soup = BeautifulSoup(elementHTML,'html.parser') # type: ignore

        name = soup.find('div', attrs={'data-testid': 'event-name'})
        name = name.text if name else 'TBD'

        when = soup.find('div', attrs={'data-testid': 'when'})
        when = when.text if when else 'TBD'

        location = soup.find('div', attrs={'data-testid': 'address'})
        location = location.text if location else 'TBD'

        events.append({'name': name, 'location': location, 'date': when, })

    driver.close()

    print(events)

if __name__ == "__main__":
    get_events()
