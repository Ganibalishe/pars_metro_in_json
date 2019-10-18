import json
import requests
from bs4 import BeautifulSoup as bs

headers = {'accept': '*/*',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
           }

base_url = 'https://ru.wikipedia.org/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%B0%D0%BD%D1%86%D0%B8%D0%' \
           'B9_%D0%9C%D0%BE%D1%81%D0%BA%D0%BE%D0%B2%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D0%BC%D0%B5%D1%82%D1%80%D0%BE%D0%BF' \
           '%D0%BE%D0%BB%D0%B8%D1%82%D0%B5%D0%BD%D0%B0'


def get_metro_in_json(base_url, headers):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    metro = {}

    soup = bs(request.content, 'lxml')
    table = soup.find_all('table')[3]
    rows = table.find_all('tr')
    del rows[0]

    lines = []
    line_with_stations = {}
    for row in rows:
        td = row.find_all('td')
        lines.append(td[0]['data-sort-value'])

    clear_lines = []
    for line in lines:
        if line not in clear_lines:
            clear_lines.append(line)

    for line in clear_lines:
        stations = []
        for row in rows:
            td = row.find_all('td')
            station_name = td[1].find('a')
            if td[0]['data-sort-value'] == line:
                stations.append(station_name.text)
        line_with_stations[line] = stations
    metro['stations'] = line_with_stations

    description_lines = []
    for row in rows:
        td = row.find_all('td')
        number_line = td[0]['data-sort-value']
        line_name = td[0].find_all('span')[1]['title']
        description_line = {'number': number_line, 'name': line_name}
        if description_line not in description_lines:
            description_lines.append(description_line)
    metro['lines'] = description_lines

    return metro





def main():
    mos_metro = get_metro_in_json(base_url, headers)
    with open('mos_metro.json', 'w') as file:
        json.dump(mos_metro, file, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
