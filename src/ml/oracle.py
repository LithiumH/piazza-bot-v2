import gensim
import re
import json
import numpy as np

## The Oracle class
class Oracle(object):
    """The Oracle class is the class that preprocesses, trains, and analyzes
    materials and return the closest post in its data
    """
    def __init__(self, dbpath, temp_path):
        """The init function of the preprocessor takes in a string of the location of the
        database file.

        dbpath: string of the location of the database file.
        """
        self.dbpath = dbpath
        self.temp_path = temp_path
        self.clean_re = re.compile("</?[^>]+/?>")
        self.word_re = re.compile("[\w']+")

    def load_databases(self, dbpath=''):
        """Loads the database file to a dictionary. The path should be stored inside
        the bot.

        dbpath: string of an alternative database path.
        """
        if not dbpath:
            dbpath = self.dbpath
        try:
            f = open(dbpath, 'r')
            data = json.load(f)
            f.close()
            self.posts = [(post['question']['title'] + ' ' + post['question']['text'], post) \
                    for classs in data \
                    for post in classs['posts']]
        except:
            print('couldn\'t load databases')

    def preprocess(self):
        print ('Pre-processing data')
        self.build_dict()
        self.build_corpus()

    def build_dict(self):
        """This function cleans the data beautifully and generate a copora dictionary
        later to be used as a bag-of-word model to build the coporus
        """
        self.all_text = [self.word_re.findall(self.clean_re.sub(' ', question.lower())) \
                for question, _ in self.posts]
        self.dict = gensim.corpora.Dictionary(self.all_text)
        self.dict.filter_extremes(0, 0.5, keep_n=9999999)
        self.dict.filter_n_most_frequent(25)
        self.dict.save(self.temp_path + 'quests.dict')

    def build_corpus(self):
        """This function builds the corpus and saves it at the designated location"""
        self.corpus = [self.dict.doc2bow(text) for text in self.all_text]
        gensim.corpora.MmCorpus.serialize(self.temp_path + 'corpus.mm', self.corpus)

    def train(self):
        """This function creates and trains a model for future comparison"""
        print ('training...')
        self.dict = gensim.corpora.dictionary.Dictionary.load(self.temp_path + 'quests.dict')
        mm = gensim.corpora.mmcorpus.MmCorpus(self.temp_path + 'corpus.mm')
        self.tfidf = gensim.models.TfidfModel(mm)
        self.mm_tfidf = self.tfidf[mm]
        self.lsi = gensim.models.LsiModel(self.mm_tfidf, id2word=self.dict, num_topics=50)
        self.index = gensim.similarities.MatrixSimilarity(self.lsi[self.mm_tfidf])

    def nearest_post(self, query):
        """This function returns the nearest post of the given questions based on the
        question alone

        query: a string of a single question
        """
        query = self.word_re.findall(self.clean_re.sub(' ', query))
        query_vec = self.lsi[self.tfidf[self.dict.doc2bow(query)]]
        sims = self.index[query_vec]
        max_index = np.argmax(sims)
        return self.posts[max_index][1], sims[max_index]

    def interact(self):
        """This function enables anyone to interact with this Oracle by launching and
        training itself and constantly waiting for user input. This function does not return
        anything at the moment
        """
        self.load_databases()
        self.preprocess()
        self.train()
        while True:
            query = raw_input("Type the question below:\n")
            if 'exit' in query:
                return
            nearest, conf = self.nearest_post(query.lower())
            question = nearest['question']['title'] + "||" + nearest['question']['text']
            answer = nearest['ta_answer']['text'] if nearest['ta_answer'] is not None else \
                    nearest['st_answer']['text'] if nearest['st_answer'] is not None else ''
            print 'conf:%.3f\nquest:%s\nans:%s\n' % (conf, question, answer)


############
#PLAYGROUND#
############

"""
"""
