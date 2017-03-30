from bot.utils import id_to_year, year_to_id, send_email

class RealTimeBot(object):
    """This class defines a real time bot that would be constantly running
    and looking for new posts to be answered. Good boy good boy."""

    def __init__(self, dbpath, login):
        """Initializes a bot with predefined values.

        dbpath: a string of the filepath of the database
        login: a tuple of (username, password) pair
        """
        self.dbpath = dbpath
        self.p = Piazza()
        self.p.user_login(*login)
        try:
            f = open(self.dbpath, 'r')
            self.data = json.load(f)
            f.close()
        except:
            print("Cannot load database. Bot cannot be created")

