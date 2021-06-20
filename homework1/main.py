import requests
import re
from bs4 import BeautifulSoup

URL = 'https://codeforces.com/contests?complete=true&locale=en'


def parse_name(cell):
    return cell.text.split('\n')[1]


def parse_writers(cell):
    writers = []
    for writer in cell.select('a'):
        writers.append(writer.text)
    return writers


def parse_start(cell):
    return cell.text.split('\n')[1]


def parse_length(cell):
    return cell.text.strip()


def parse_participants(cell):
    return int(cell.text.strip()[1:])


def parse_row(row):
    cells = row.select('td')
    if len(cells) != 6:
        return None

    parsed_data = dict()

    parsed_data['name'] = parse_name(cells[0])
    parsed_data['writers'] = parse_writers(cells[1])
    parsed_data['start'] = parse_start(cells[2])
    parsed_data['length'] = parse_length(cells[3])
    parsed_data['participants'] = parse_participants(cells[5])

    return parsed_data


def main():
    r = requests.get(URL)
    print('Status code is {}'.format(r.status_code))
    print()

    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.select_one('.contests-table').select_one('.datatable').select_one('table')
    for row in table.select('tr'):
        parsed = parse_row(row)

        if parsed is None:
            continue

        print('Name: {}'.format(parsed['name']))
        print('Writers: {}'.format(', '.join(parsed['writers'])))
        print('Start: {}'.format(parsed['start']))
        print('Length: {}'.format(parsed['length']))
        print('Participants: {}'.format(parsed['participants']))
        print()


if __name__ == '__main__':
    main()
