import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import requests

def get_alpha_num(text):
    return re.sub(r'\W+', '', text)


def process_text(text):
    text = re.sub('\n+', '\n', text)
    text = re.sub('\t+', '\t', text)
    text = re.sub('[ ]+', ' ', text)
    return text

url = "https://durhamcollege.ca/programs-and-courses"

response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

program_row = soup.find('tbody').find_all('tr')

program_df = {
    'URL': [],
    'Length': [],
    'Credential': [],
    'Location': [],
    'Next Intake': [],
    'International': [],
    'Hidden Keywords': []
}

for row in program_row:
    tds = row.find_all('td')
    program_df['URL'].append(tds[0].a.attrs.get('href'))
    program_df['Length'].append(tds[1].text)
    program_df['Credential'].append(tds[2].text)
    program_df['Location'].append(tds[3].text)
    program_df['Next Intake'].append(tds[4].text)
    program_df['International'].append(tds[5].text)
    program_df['Hidden Keywords'].append(tds[0].find('span', {"class": "visuallyhidden program-search-keywords"}).text)

program_df = pd.DataFrame(program_df)

new_data = []
failed_df = []

for i, row in program_df.iterrows():
    print()
    time.sleep(1)
    record = row.to_dict()
    try:

        p_link = row['URL']
        print(i, ':', p_link, end=' ')
        response = requests.get(p_link)
        soup = BeautifulSoup(response.content, "html.parser")

        ocas = get_alpha_num(soup.find('dt', string=re.compile(r'OCAS Code')).parent.dd.text)
        faculty = get_alpha_num(soup.find('dt', string=re.compile(r'Faculty')).parent.dd.text)
        faculty_link = soup.find('dt', string=re.compile(r'Faculty')).parent.dd.a.attrs.get('href')
        delivery = soup.find('dt', string=re.compile(r'Delivery')).parent.dd.text
        record.update({
            'OCAS Code': ocas,
            'Faculty': faculty,
            'Faculty URL': faculty_link,
            'Delivery': delivery
        })
        program_info_index = soup.find('ul', {'id': 'deeplinked-tabs', 'class': 'desktop-tabs'})
        tab_titles = program_info_index.find_all('li', {'class': 'tabs-title'})
        for tab in tab_titles:
            post_fix = tab.a.attrs.get('href')
            print(post_fix,end=' ')
            if post_fix != '#tabConnect':
                nurl = p_link + post_fix
                response = requests.get(nurl)
                soup1 = BeautifulSoup(response.content, "html.parser")
                main_section = soup1.find('section', {'id': 'dc-programs-container'})
                tab_cat = soup1.find('div', {'id': post_fix[1:]})
                tab_title = process_text(tab_cat.h2.text)
                tab_info = process_text(tab_cat.text)
                record[tab_title] = tab_info
        new_data.append(record)
    except Exception as e:
        print('Error : ',e)
        failed_df.append(record)
df = pd.DataFrame(new_data)
df.to_csv('DC.csv')

f_df = pd.DataFrame(failed_df)
f_df.to_csv('failed_data.csv')
