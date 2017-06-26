# The MachineLearning (ML) Bot
This is the source code for the ml bot!

# Structure

## Pre-start up
Before starting the Oracle there will be a pre-processing step of all the data that was
stored in the database. If the data is already pre-processed (i.e. there is a file) then it
loads the file.

The schema of the data taken into the pre-processing stage is described
[here](../bot/README.md)

The pre-processing of the data is separated into these steps:
1. Load the database and break them into (question, post) pairs. `post` is passed by reference
   and question is a string.
2. Use ALL the questions to build a dictionary.
3. (Extra) Add other features
4. Use the dictionary to build vectors.

## Start Up
After creating the corpus, the bot will train on the data by transforming the vector and then
create models that fits the data.

## Query
The bot will take in a question as the query (Feature: take in tag as well) and then nearest
post to this query.

## Algorithm
TF-IDF transformation
LSI models

# Testing Structure
How is the bot tested and how do we evaluate how accurate the bot is

## Integration tests
1. Find 200 random questions
2. Move the words around, use similar words and such.
3. Create a test set and evaluete the algorithm with the test set.
