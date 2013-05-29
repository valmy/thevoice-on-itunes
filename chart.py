from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

US = {
    'url': 'http://www.itunescharts.net/us/charts/songs/',
    'song_name': '(The Voice Performance)'
    }

AUS = {
    'url': 'http://www.itunescharts.net/aus/charts/songs/',
    'song_name': '(The Voice 2013 Performance)'
    }

class Chart(object):

    def __init__(self, country):
        if country == 'us':
            self.url = US['url']
            self.song_name = US['song_name']
        elif country == 'aus':
            self.url = AUS['url']
            self.song_name = AUS['song_name']

    def read(self, date_str):

        res = requests.get(self.url + date_str)
        chart = SoupStrainer(id='chart')
        soup = BeautifulSoup(res.text, parse_only=chart)
        entries = soup.find_all('li')
        results = []
        for entry in entries:
            no_tag = entry.find('span', class_ = 'no')
            artist_tag = entry.find('span', class_ = 'artist')
            song_tag = entry.find('span', class_ = 'entry')
            if 'The Voice' in song_tag.get_text():
                no = int(no_tag.get_text())
                artist = artist_tag.get_text().strip()
                song = song_tag.get_text().strip()
                song = song[:-len(self.song_name)].strip()
                results.append({ 'rank': no,
                        'artist': artist,
                        'song': song })
        return results

def main():
    chart = Chart('us')
    chart_list = chart.read('2013/05/21')
    print chart_list

if __name__ == '__main__':
    main()
