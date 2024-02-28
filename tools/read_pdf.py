import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()


class ScraperTool():
  @tool("Scrape a website")

  def scrape(url: str):
    "Useful tool to scrape the content of a website given a url and returns a soup object."

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    payload = {
       "url": url
    }

    browserless_token = os.getenv("BROWSERLESS_API_KEY")
    url = "https://chrome.browserless.io/content?token=" + browserless_token

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup.find_all('script'):
            script.decompose()  
        for style in soup.find_all('style'):
            style.decompose()  

        
        text = soup.get_text(strip=True)  
        print("Text", text)
        print("Soup", soup)
        return text
    else:
        return "Failed to retrieve the webpage"