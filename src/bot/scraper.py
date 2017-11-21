import json
from piazza_api import Piazza
from bot.utils import id_to_year, year_to_id, send_email, get_post, translate_post

class Scraper(object):
    """This Scraper class defines a scraper that will scrape the piazza
    and generate a json file to be used by the realtime bot"""

    def __init__(self, dbpath, login):
        """Initiates a bot with predefined values, all of them required

        dbpath: a string of the filepath of the database
        login: a tuple of (username, password) pair
        """
        self.dbpath = dbpath
        self.p = Piazza()
        self.p.user_login(*login)
        self.data = []

    def load_databases(self, dbpath=''):
        """Loads the database file to a dictionary. The path should be stored inside
        the bot.

        dbpath: string of an alternative database path.
        """
        if not dbpath:
            dbpath = self.dbpath
        try:
            f = open(dbpath, 'r')
            self.data = json.load(f)
            f.close()
        except:
            print('couldn\'t load databases')

    def store_databases(self, dbpath=''):
        """Writes the entire database to the file path stored inside the bot. Or an alternative
        database file given to this function.

        dbpath: string of an alternative database path.
        """
        if not dbpath:
            dbpath = self.dbpath
        f = open(dbpath, 'w')
        result = json.dumps(self.data)
        f.write(result)
        f.close()

    def scrape(self, sem):
        """Scrape a particular semester and storeit in the database.
        Notice if the semester is already scraped then it ignores this semester.
        The reason is we don't know whether some of the posts are already in the
        database, so to avoid double scraping we ignore the ones we already scraped.

        sem: a string of the semester name, e.g. fa16
        """
        class_id = year_to_id(sem)
        for c in self.data:
            if c['class_id'] == class_id:
                return
        network = self.p.network(class_id)
        try:
            feed = network.get_feed(limit=99999, offset=0)
        except:
            print('error getting feed from {0}'.format(sem))
            return
        result = {'class_id': class_id, 'posts': []}
        self.data += [result]
        cids = ((post['nr'], post['id']) for post in feed['feed'])
        for cidn, cid in cids:
            post = get_post(network, class_id, cid)
            if post is not None and post['type'] == 'question':
                post = translate_post(class_id, post)
                result['posts'].append(post)




