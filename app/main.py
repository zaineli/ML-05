import requests
from bs4 import BeautifulSoup
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

def scrape_search_results(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []

    for item in soup.find_all('h3'):
        parent = item.find_parent('a')
        if parent:
            links.append(parent['href'])

    return links[:10]

@app.get("/search")
def search(query: str):
    results = scrape_search_results(query)
    results = [ link.replace('/url?q=', '') for link in results]
    return results