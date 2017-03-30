import smtplib

sp17_id = 'ixj56cq4o911qa'
fa16_id = 'irwl7o7shzu70z'
su16_id = 'ipkfex1ne3p56y'
sp16_id = 'ij5ddqc0arp6r4'
fa15_id = 'id52tzq2i7yfx'
sp15_id = 'i4q8ow8g8bv7oa'
fa14_id = 'hx2jz3h2i112h8'

test_id = 'ismb1h6mwl618w'

id_vs_year = {fa16_id: 'fa16', su16_id: 'su16', sp16_id: 'sp16', fa15_id: 'fa15',
        sp15_id: 'sp15', fa14_id: 'fa14', test_id: 'test', sp17_id: 'sp17'}

def id_to_year(class_id):
    """This function takes in a class id string and return the year string

    class_id: the string of class id, such as ismb1h6mwl618w
    returns: the string of class/semester, such as test
    """
    return id_vs_year[class_id]

def year_to_id(year):
    """This function takes in a semester string and return the class id

    year: the string of the year, such as test
    returns: the string of class id, such as ismb1h6mwl618w
    """
    for class_id in id_vs_year:
        if year == id_vs_year[class_id]:
            return class_id

def get_post(network, class_id, post_id):
    """This function tries to get a post without translating it. It will
    try 3 times. If all 3 times failed returns None

    network: the Network used to get the post
    class_id: the class id of the post. Depracated.
    post_id: the id of the post. Used for getting the post

    returns: a dictionary returned from the network.get_post call
    """
    for i in range(3):
        try:
            print ('[bot] scrapping {0} from {1}'.format(post_id, id_to_year(class_id)))
            return network.get_post(post_id)
        except:
            pass
    print ('[bot] getting {0} failed'.format(post_id))

def translate_post(class_id, post):
    """This function translates an original post dictionary returned by
    the API to the post dictionary specified in the README.

    post: an original post dictionary.

    returns: a translated dictionary specified by the README
    """
    latest = post['history'][-1]
    question = {
            'title': latest['subject'],
            'text': latest['content'],
            'last_update': latest['created'],
            'good_question_count': len(post['tag_good']),
            'categories': post['tags']
            }
    ta_answer = st_answer = None
    if 'children' in post:
        for child in post['children']:
            if child['type'] != 'i_answer' and child['type'] != 's_answer':
                continue
            latest = child['history'][-1]
            answer = {
                    'text': latest['content'],
                    'latest_update': latest['created'],
                    'good_answer_count': len(child['tag_endorse']),
                    'endorsed': child['is_tag_endorse']
                    }
            if child['type'] == 'i_answer':
                ta_answer = answer
            else:
                st_answer = answer
    return {
            'class_id': class_id,
            'post_id': post['id'] if 'id' in post else None,
            'post_cid': post['nr'] if 'nr' in post else None,
            'is_private': post['status'] == 'private',
            'question': question,
            'st_answer': st_answer,
            'ta_answer': ta_answer,
            'views': post['unique_views']
           }

def send_email(to_user, subject, text, login, server=None):
    """This function sends an email to a specific user.
    This function may require the .login file to default the user and password
    of the sender. The third line should be the email address
    and the fourth line should be the password.

    to_user: a string email address of the receipiant of the email
    subject: a string of subject of the email
    text: a string of the text to be included into the email.
    login: a tuple of strings of a email and password pair.
    server: a smtplib.SMTP server, or None to establish a default gmail connection
    """
    message = "From: {0}\nTo: {1}\nSubject: {2}\n\n{3}"\
            .format(user, to_user, subject, text)

    if not server:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(*login)
    server.sendmail(user, to_user, message)
    server.close()


