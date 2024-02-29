import requests
import os
from PyPDF2 import PdfReader


# pdf_url = 'https://sci-hub.se/downloads/2019-02-17/f0/caffau2015.pdf'
pdf_url = 'https://dacemirror.sci-hub.se/journal-article/81bc9c0ec91963a241166184b5484700/west2016.pdf#navpanes=0&view=FitH'

response = requests.get(pdf_url)
with open('temp.pdf', 'wb') as f:
    f.write(response.content)

reader = PdfReader('temp.pdf')
number_of_pages = len(reader.pages)
output = ""

for page in reader.pages:
    output += page.extract_text()

reader.stream.close()

os.remove('temp.pdf')

print(output)
