# This is the launch script to start everything.
import bot.realtime
import bot.scraper
import ml.oracle

def login_prompt():
    import getpass
    username = raw_input('Please enter you username: ')
    password = getpass.getpass('Please enter your password: ')
    return username, password

def parse_login(path):
    f = open(path)
    username, password = f.readline().strip(), f.readline().strip()
    f.close()
    return username, password

def start_realtime(data_path, sems, curr, algo, login):
    """This function starts a realtime bot that runs constantly

    data_path: a string of the path to the main database file
    sems: a list of strings of semesters to be used as database
    curr: a string of the name of the semester, NOT the id of the class
    algo: a string of the algorithm specified to run the bot
    login: a tuple of username and password
    """
    print ('starting realtime bot for semester %s' % curr)

def start_ml(data_path, corpus_path):
    """This function is used to test the Oracle interactively. When type in a question
    it will respond the closest matched question, its answer, and its similarity

    data_path: a string of the path of the main database file
    """
    global o
    o = ml.oracle.Oracle(data_path, corpus_path)
    o.interact()

def start_scraper(data_path, sems, login):
    """This function starts a scraper and scrub the piazza of specific
    semesters listed in SEMS

    data_path: a string of the path to store the scrubbed data json file
    sems: a list of strings of semesters to be scrubbed
    login: a tuple of username and password
    """
    print ('starting scraper for semester %s' % ' '.join(sems))
    global scraper
    scraper = bot.scraper.Scraper(data_path, login)
    scraper.load_databases()
    for sem in sems:
        scraper.scrape(sem)
    scraper.store_databases()

if __name__ == '__main__':
    import argparse
    import sys
    all_sem = ['sp17', 'fa16', 'su16', 'sp16', 'fa15', 'sp15', 'fa14', 'test']
    parser = argparse.ArgumentParser(description='Launch either bots to do your job.')
    parser.add_argument('bot_type', type=str, choices=['realtime', 'scraper', 'oracle'])
    parser.add_argument('current', type=str, nargs='?', choices=all_sem, default='test')
    parser.add_argument('--path', type=str, dest='dbpath', required=True,
            help='A string of the database filepath.')
    parser.add_argument('--sems', dest='sems', nargs='+',
            help='Include specific semesters\' data.',
            choices=all_sem,
            default=all_sem)
    parser.add_argument('--algo', dest='algo',
            help='Specify an algorithm to be used for machine learning.')
    parser.add_argument('--login', dest='login',
            help='Specify the login credential file. Should be 2 lines (username and password)',
            default=None)

    try:
        args = parser.parse_args()
    except:
        sys.exit(1)
    if args.bot_type == 'oracle':
        start_ml(args.dbpath, 'tmp/')
        sys.exit(0)
    login = args.login
    if not login:
        login = login_prompt();
    else:
        login = parse_login(login)
    if args.bot_type == 'scraper':
        start_scraper(args.dbpath, args.sems, login)
    elif args.bot_type == 'realtime':
        start_realtime(args.dbpath, args.sems, args.current, args.algo, login);


