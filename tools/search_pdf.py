import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from habanero import Crossref
load_dotenv()

import time


cr = Crossref()

def convert_apostrophes(text):
    converted_text = text.replace("'", "\\'")
    return converted_text

def fetch_pdf_link(scihub_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
   
    payload = {
       "url": scihub_url
    }
    browserless_token = os.getenv("BROWSERLESS_API_KEY")
    url = f"https://chrome.browserless.io/content?token={browserless_token}"
    response = requests.post(url, json=payload, headers=headers)
   
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        for script in soup.find_all('script'):
            script.decompose()  
        for style in soup.find_all('style'):
            style.decompose()  
        
        link = soup.find_all('iframe')[1]['src']
        print('Soupzsk', link)
        return link
    else:
        return "Failed to retrieve the webpage"


class FetchPDFTool():
  @tool("Get the pdf contents of an article given the article title")
  def read_pdf(article_title: str):
    "Useful for getting the pdf contents from an article."

    article_title = convert_apostrophes(article_title)
    doi = cr.works(query=article_title)['message']['items'][0]['DOI']

    print("Reached DOI", doi)

    url = fetch_pdf_link(f"https://sci-hub.wf/{doi}")

    print("URLZSK", url)

    response = requests.get(url)
    
    # Check if the response is successful (status code 200)
    if response.status_code == 200:
        # Check for content type to ensure PDF file is received
        if response.headers['Content-Type'] == 'application/pdf':
            # Write the PDF content to a file
            with open('temp.pdf', 'wb') as f:
                f.write(response.content)

            reader = PdfReader('temp.pdf')
            output = ""

            for page in reader.pages:
                output += page.extract_text()

            reader.stream.close()

            os.remove('temp.pdf')
            print("Outputzsk", output)
            return output
        else:
            print("Content received is not a PDF.")
            return None
    else:
        print("Failed to fetch PDF content.")
    return None