import logging
from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import RelevanceFilters, TimeFilters, TypeFilters, ExperienceLevelFilters, RemoteFilters
import csv


logging.basicConfig(level = logging.INFO)

jobs=[]
def on_data(data: EventData):
    print('[ON_DATA]', data.title, data.company, data.date, data.link, len(data.description))
    jobs.append({data.title})


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path=None,
    chrome_options=None, 
    headless=True, 
    max_workers=1, 
    slow_mo=3.3,
    
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)
queries = [
    Query(
        options=QueryOptions(
            optimize=True,  
            limit=27  
        )
    ),
    Query(
        query='',
        options=QueryOptions(
            locations=['France'],
            optimize=False,
            
            limit=5,
            filters=QueryFilters(
                relevance=RelevanceFilters.RECENT,
                time=TimeFilters.MONTH,
                type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                experience=None,                
            )
        )
    ),
]

scraper.run(queries)
with open('output.csv', 'w', newline='') as f:
    write = csv.writer(f, delimiter=';',  quoting=csv.QUOTE_MINIMAL)
    write.writerows(jobs)
