from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://pypi.org/simple/'
total_pkgs = 0
pkg_names = []
pkg_links = []
response = requests.get(url)
data = response.text
soup = BeautifulSoup(data, 'html.parser')

body_tag = soup.find('body')
list_of_all_pkg_tags = list(body_tag.find_all('a'))

for pkg_tag in list_of_all_pkg_tags:
    pkg_names.append(pkg_tag.text)

df = pd.DataFrame({'Package Name': pkg_names})
df.to_csv('../data/pypi_pkg_names.csv')
