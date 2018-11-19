import json, os

from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

class lyrics():
    def __init__(self):
        self.config = {}
        self.commands = {
            'lyrics': self.get_lyrics
        }
        self.default_config = {
            'GENIUS_ACCESS_TOKEN': ''
        }
        self.description = "Search lyrics on <a href='https://genius.com'>Genius</a>!"
        self.help_text = "Write /lyrics &lt;song name&gt; to search for a song's lyrics on <a href='https://genius.com'>Genius</a>"


    def get_lyrics(self, bot, update, args):
        if len(args)==0:
            return
        song_name = " ".join(args)
        bot.send_chat_action(chat_id=update.message.chat_id, action='typing')
        try:
            lyrics = self.scrape(self.search_song_url(song_name))
            songdata = self.search(song_name)
            if "default" not in songdata['result']['header_image_url']:
                bot.send_photo(chat_id=update.message.chat_id, photo=songdata['result']['header_image_url'], caption=songdata['result']['full_title'])
            else:
                bot.send_message(chat_id=update.message.chat_id, text=songdata['result']['full_title'])
            bot.send_message(chat_id=update.message.chat_id, 
                text=lyrics.replace("[", "<b>[").replace("]", "]</b>"), 
                parse_mode='HTML')
        except IndexError:
            bot.send_message(chat_id=update.message.chat_id, 
            text="Lyrics not found for your song :(")
            pass


    def request(self, song_query):
        return requests.get(f"http://api.genius.com/search?access_token={self.config['GENIUS_ACCESS_TOKEN']}&q={song_query}")


    def search_song_url(self, song_query):
        # Generate search request
        response = self.request(song_query)# , headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})
        search_json = json.loads(response.text)
        song_url = search_json['response']['hits'][0]['result']['url']
        return song_url


    def search_title(self, song_query):
        # Generate search request
        response = self.request(song_query)
        search_json = json.loads(response.text)
        song_title = search_json['response']['hits'][0]['result']['full_title']
        return song_title


    def search(self, song_query):
        # Generate search request
        response = self.request(song_query)
        search_json = json.loads(response.text)
        return search_json['response']['hits'][0]


    # scrape a Genius song page for the full lyrics
    def scrape(self, song_url):
        # Get raw lyrics for first song result
        response = requests.get(song_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'})

        # Clean up html
        soup = BeautifulSoup(response.text, "html.parser")
        soup = soup.find("div", class_="lyrics")
        lyrics = soup.get_text().strip()

        return lyrics
