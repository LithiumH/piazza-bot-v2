# The BOT
This directory contains source code for the bot! There are two things here:
1. A scraper that scrubs the piazzas specified
2. A bot that runs constantly to monitor a specific piazza

## The Scrubber
The scraper is a bot that scrubs the piazzas specified. The scraper can be launched
by the scraper script, or imported by the bot if scrubbing is required.

The scraper script takes in a source directory on launch, and it will ask for the 
classes/semesters that we want to scrub. The values are of the following: `fa16`;
`su16`; `sp16`; `fa15`; `sp15`; `fa14`; `test`. The `test` class is created to test
the validity of the answers.

The scraper will generate a json file with a map of class to an array of Posts.
```
[
  {
    'class_id': string,
    'posts': [Post, Post, ...]
  }, ...
]
```

Each `Post` has some information and contains the question and answers.
```
{
  'class_id': string, 
  'post_id': string, 
  'post_cid': int,
  'is_private': boolean,
  'question': Question,
  'st_answer': Answer,
  'ta_answer': Answer,
  'follow_ups': [FollowUp, FollowUp, ...],
  'views': int
}
```

Each `Question` has some information and the text of the question.
```
{
  'title': string,
  'text': string,
  'last_update': string,
  'authors': [string, string, ...],
  'good_question_count': int,
  'categories': [string, string, ...]
}
```

Each `Answer` has some informatino and the text of the answer.
```
{
  'text': string,
  'latest_update': string,
  'authors': [string, string, ...],
  'good_answer_count': int,
  'endorsed': boolean
}
```

## The realtime Bot
The real time bot is suppose to constantly monitor the piazza to answer questions
when available.

The realtime bot script takes in a `class_id`, a data directory, and confidence on launch.
The real time bot will first launch the ml package if available, start an ml bot (either
already trained or not depending on launch configuration). Once the new post is 
discovered the following actions should occur:

1. It will load the question and convert it into a dictionary.
2. It will query the ml bot created from launch and answer (or not answer) the question
   depending on the confidence.
3. It will add the question (and potentially answer) back into the database.
4. It will do some magic to notify some TAs so they will make sure it is correct.




