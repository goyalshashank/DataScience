import requests
from bs4 import BeautifulSoup
from urllib.request import unquote
import re

url  = 'https://www.mca.gov.in/MinistryV2/monthlyinformationbulletin.html'
agents = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}

response = requests.get(url,headers=agents)
content = BeautifulSoup(response.text, 'lxml')

all_urls = content.find_all('a')

pdf_urls = []

for url in all_urls:
    try:
        if 'pdf' in url['href']:
            if re.search('MIB',url['href']) and re.search('202[0-1]',url['href']):
                pdf_url = ''
                if 'https' not in url['href']:
                    pdf_url = 'https://www.mca.gov.in/' + url['href']
                else:
                    pdf_url = url['href']

                pdf_response = requests.get(pdf_url,headers=agents)
                filename = unquote(pdf_response.url).split('/')[-1].replace(' ','_')
                print(filename) 
                with open('./pdf/'+filename, 'wb') as f:
                    f.write(pdf_response.content)

            

    except Exception as e:
        print("Error: ", e)