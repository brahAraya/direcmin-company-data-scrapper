import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
from string import ascii_lowercase as alc

regex = re.compile(r'(https://www\.direcmin\.com/.*?/informacion-de-contacto)')
file_name = 'direcmin_empresas.xlsx'
search_url = 'https://www.direcmin.com/home/resultados'
company_urls = []
companies = []

print('\n1. Fetching company urls')
for letter in alc:
  print(f'searching for letter {letter}')
  data = { 'buscar': letter }
  result_page = requests.post(search_url, data)
  company_urls = company_urls + regex.findall(result_page.text)

# remove duped data
company_urls = list(set(company_urls))

print('\n2. Getting corporate data')
for i, url in enumerate(company_urls):
  print(f'[{i + 1} of {len(company_urls)}]  getting corporate data from {url}')
  company_data = {}
  company_page = requests.get(url)
  soup = BeautifulSoup(company_page.text, 'html.parser')
  company_data['Nombre'] = soup.find_all('h1')[1].string
  table = soup.find_all('table')[2]
  rows = table.find_all('tr')
  for row in rows:
    columns = row.find_all('td')
    if len(columns) > 1 and columns[0].string != 'Ubicación:':
      key = columns[0].string.replace(':', '')
      value = columns[1].string
      company_data[key] = value
  print(f'result: {company_data}\n')
  companies.append(company_data)

df = pd.DataFrame(companies)
df.to_excel(file_name, index=False)
print(f'\n Companies data retrieved and saved in file {file_name}')
