##############################
# Machine Learning Interface #
##############################

class Learner:
    """ This class defines a machine learning object that incorporates
    the machine learning algorithms and return answers.
    """
    def __init__(self, data):
        """The constructor. notice the data is pass by reference so we do not
        create duplicated copies of the data.

        data: a list of dictionaries defined by README in src/bot.
        """
        self.data = data

    def answer(self, post):
        """This method takes in a full post containing a question, and returns
        another post that was answered from previous semesters and is closest to
        this POST.

        Note that right not it just returns a dummy post with the original question
        and the answer as "I do not know"

        post: a dictionary which structure is defined by the README.
        returns: a dictionary of the same structure but must contain an answer, and
                 a confidence level from 0 to 1
        """
        return {
                'class_id': 'undefined'
                'post_id': 'undefined'
                'post_cid': 0
                'is_private': False
                'question': post['question']
                'st_answer': None
                'ta_answer': {
                    'text': 'I do not know'
                    'latest_update': '03-30-2017'
                    'good_answer_count': 0
                    'endorsed': False
                    }
                'views': 1
                }, 1
