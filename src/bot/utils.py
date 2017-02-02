import smtplib

fa16_id = 'irwl7o7shzu70z'
su16_id = 'ipkfex1ne3p56y'
sp16_id = 'ij5ddqc0arp6r4'
fa15_id = 'id52tzq2i7yfx'
sp15_id = 'i4q8ow8g8bv7oa'
fa14_id = 'hx2jz3h2i112h8'

test_id = 'ismb1h6mwl618w'

id_vs_year = {fa16_id: 'fa16', su16_id: 'su16', sp16_id: 'sp16', fa15_id: 'fa15',
        sp15_id: 'sp15', fa14_id: 'fa14', test_id: 'test'}

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
    """ This function tries to get a post and translate it. It will
    try 3 times. If all 3 times failed then it will be very sad.

    network: the network used to get the post
    class_id: the class id of the post. Used for translating the dictionary
              to a Post object
    post_id: the id of the post. Used for getting the post
    """
    for i in range(3):
        try:
            print '[bot] scrapping {0} from {1}'.format(post_id, id_to_year(class_id))
            dic = network.get_post(post_id)
            return post_to_json(class_id, post_id, dic), dic['id']
        except:
            pass
    print '[bot] getting {0} failed'.format(post_id))

def post_to_json(class_id, post_id, og_post):
    """This function translate a dictionary OG_POST to a json object
    specified in the README.
    For now it only gets the most recent version of the post.

    class_id: the class id of the post. Used for constructing the Post object
    post_id: the id of the post. Used for constructing the Post object
    og_post: the dictionary version of the original post. Freshly returned
             from the network and parsed by json.
    """
    question = None
    if 'history' in og_post:
        latest = og_post['history'][-1]
        question = {
                'title': latest['subject'] if 'subject' in latest else None,
                'text': latest['content'] if 'content' in latest else None,
                'last_update': latest['created'] if 'created' in latest else None,
                'authors': None
                'good_question_count': len(latest['tag_good']) if 'tag_good' in latest else 0,
                'categories': latest['tags'] if 'tags' in latest else None
                }
    # TODO finish the rest
    st_answer, ta_answer = None, None
    if 'children' in og_post:
        for child in og_post['children']:
            if child['type'] == 's_answer':
                latest = child['history'][-1]
                st_answer = Answer(
                        latest['content'] if 'content' in latest else None,
                        latest['created'],
                        None,
                        len(latest['tag_endorse']) if 'tag_endorse' in latest else 0,
                        latest['is_tag_endorse'] if 'is_tag_endorse' in latest else None
                        )
            elif child['type'] == 'i_answer':
                latest = child['history'][-1]
                ta_answer = Answer(
                        latest['content'] if 'content' in latest else None,
                        latest['created'],
                        None,
                        len(latest['tag_endorse']) if 'tag_endorse' in latest else 0,
                        latest['is_tag_endorse'] if 'is_tag_endorse' in latest else None
                        )
    post = Post(class_id, post_id, og_post['type'],
            og_post['status'] == 'private',
            question, st_answer, ta_answer, [], og_post['unique_views'])
    return post

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


