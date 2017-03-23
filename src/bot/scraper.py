import json
from piazza_api import Piazza
from bot.utils import id_to_year, year_to_id, send_email

class Scraper(object):
    """This Scraper class defines a scraper that will scrape the piazza
    and generate a json file to be used by the realtime bot"""

    def __init__(self, dbpath, login):
        """Initiates a bot with predefined values, all of them required

        dbpath: a string of the filepath of the database
        sems: a list of strings of semesters to scrub, recognized by year_to_id func
        login: a tuple of (username, password) pair
        """
        self.dbpath = dbpath
        self.p = Piazza()
        self.p.user_login(*login)
        self.data = []

    def load_databases(self, data=[]):
        """Loads the database file to a dictionary. The path should be stored inside
        the bot."""
        if data:
            self.data = data
        else:
            f = open(self.dbpath)
            self.data = json.load(f.read())
            f.close()

    def store_databases(self):
        """Writes the entire database to the file, OVERWRITING the entire file!
        Caution is advised as this function is highly destructive, and it is designed
        that way"""
        f = open(self.dbpath)
        result = json.dumps(self.data)
        f.write(result)
        f.close()

    def scrape(self, sem):
        """Scrape a particular semester and store/update it in the database

        sem: a string of the semester name, e.g. fa16
        """
        class_id = year_to_id(sem)
        network = self.p.network(class_id)
        limit = 999999
        feed = network.get_feed(limit=999999, offset=0)
        cids = [(post['nr'], post['id']) for post in feed['feed']]
        cids = cids[:limit]
        for cidn, cid in cids:
            pass




