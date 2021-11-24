import re
import sys

import en_core_web_sm
import locationtagger
import nltk
import wikipedia
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import sent_tokenize
from nltk.util import ngrams

error_answer = "Sorry, I can't answer that."


# Function to parse through wikipedia and returns summary of the entity input.
def answer_wiki(question):
    try:
        ans = (wikipedia.summary(question,auto_suggest=True, sentences=30))
        if ans:
            return str(ans)
        else:
            return "ERROR"
    except Exception:
        return "ERROR"


# Retrieves the entity and the verb within the input
# Returns a string of entity and verbs
def entity(question):
    nlp = en_core_web_sm.load()
    nlp_quest = nlp(question)
    ent_ = []
    verb_ = []
    for ent in nlp_quest.ents:
        ent_.append(ent.text)
    if not ent_:
        for word in nlp_quest:
            if word.pos_ == 'PROPN' or word.pos_ == 'NOUN':
                ent_.append(word.text)
    for word in nlp_quest:
        if word.pos_ == 'VERB':
            verb_.append(word.text)
    return ent_, verb_


# Retrieves the entity and the verb within the input
# Returns a spacy object of entity and verbs
def entity_by_obj(question):
    nlp = en_core_web_sm.load()
    nlp_quest = nlp(question)
    ent_obj_ = []
    verb_obj_ = []
    for ent in nlp_quest.ents:
        ent_obj_.append(ent)
    for word in nlp_quest:
        if word.pos_ == 'VERB':
            verb_obj_.append(word)
    return ent_obj_, verb_obj_


# Function generates ngrams from the excerpt extracted from the the wikipedia response.
def generate_n_grams(ans_wiki):
    formatted_text = ans_wiki.lower()
    n_grams = ngrams(nltk.word_tokenize(formatted_text), 5)
    return [' '.join(grams) for grams in n_grams]


def get_ngrams(quest_type, text, filtered_question, ans_wiki):
    return generate_n_grams(ans_wiki)


# Function to extract answers for 'who' questions
def get_entity_by_key_names(sentences, ans_grams, filtered_question):
    filtered_gram = []
    key = ' '.join(filtered_question)
    ent_, verb_ = entity(key)
    if not verb_:
        return error_answer
    for sentence in sentences:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in verb_:
                ent_obj_, verb_obj_ = entity_by_obj(sentence)
                for ent in ent_obj_:
                    if ent.label_ == 'PERSON':
                        filtered_gram.append(ent.text)
    if not filtered_gram:
        answer = error_answer
        return answer
    answer = ' and '.join(filtered_gram) + ' ' + verb_[0] + ' ' + ent_[0] + '.'
    return answer


# Function to extract answers for 'when' questions
def get_entity_by_key_dates(sentences, ans_grams, filtered_question, preposition):
    filtered_gram = []
    key = ' '.join(filtered_question)
    ent_, verb_ = entity(key)
    verb = ""
    if verb_:
        verb = verb_[0]
    if not verb_:
        ent_obj_, verb_obj_ = entity_by_obj(sentences[0])
        for ent in ent_obj_:
            if ent.label_ == 'DATE':
                filtered_gram.append(ent.text)
    else:
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in verb_:
                    ent_obj_, verb_obj_ = entity_by_obj(sentence)
                    for ent in ent_obj_:
                        if ent.label_ == 'DATE':
                            filtered_gram.append(ent.text)
    if not filtered_gram:
        answer = error_answer
        return answer
    answer = ent_[0] + ' ' + preposition + ' ' + verb + ' on ' + filtered_gram[0] + '.'
    return answer


# Function to extract answers for 'where' questions
def get_entity_by_key_places(sentences, ans_grams, filtered_question, preposition):
    filtered_gram = []
    key = ' '.join(filtered_question)
    ent_, verb_ = entity(key)
    verb = ""
    if verb_:
        verb = verb_[0]
    if not verb_:
        ent_obj_, verb_obj_ = entity_by_obj(sentences[0])
        for ent in ent_obj_:
            if ent.label_ == 'GPE':
                filtered_gram.append(ent.text)
    else:
        for sentence in sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in verb_:
                    ent_obj_, verb_obj_ = entity_by_obj(sentence)
                    for ent in ent_obj_:
                        if ent.label_ == 'GPE':
                            filtered_gram.append(ent.text)
    if not filtered_gram:
        answer = error_answer
        return answer
    response = ' , '.join(filtered_gram)
    place_entity = locationtagger.find_locations(text=response)
    loc = []
    if place_entity.cities and place_entity.cities[0] not in loc:
        loc.append(place_entity.cities[0])
    if place_entity.regions and (place_entity.regions[0] not in loc):
        loc.append(place_entity.regions[0])
    if place_entity.countries and (place_entity.countries[0] not in loc):
        loc.append(place_entity.countries[0])
    if loc:
        answer = ent_[0] + ' ' + preposition + ' ' + verb + ' in ' + ', '.join(loc) + '.'
        return answer
    else:
        return error_answer


def main():
    logfile = str(sys.argv[1])
    mylogfile = open(logfile, 'w', encoding="utf-8")
    print("This is a QA system by Team 1.")
    print("It will try to answer questions that start with Who, What, When or Where.")
    print("Enter \"exit\" to close the program.")

    # List of allowed question types
    allowed_questions = ['who', 'what', 'when', 'where']

    # Keep reading in questions and finding answers until user types 'exit'
    while True:
        print("Type your question")
        question = input()
        mylogfile.write("\nQuestion: {}\n".format(question))
        if str(question) == "exit":
            break

        # Validate if the question starts with allowed keywords
        first_word = str(question).split()[0].lower()
        if first_word not in allowed_questions:
            reply = "=> The question has to start with Who, What, When or Where."
            print(reply)
            mylogfile.write("Reply:\n {}\n".format(reply))
            continue
        # Preprocess questions inputed by user
        tokenizer = RegexpTokenizer(r'\w+')
        question_tokens = tokenizer.tokenize(question)
        preposition = question_tokens[1]
        question_words = [word for word in question_tokens if word.isalpha()]
        words = [word for word in question_words]
        stop_words = set(stopwords.words('english'))
        filtered_question = []
        for w in words:
            if w not in stop_words:
                filtered_question.append(w)
        ent_, verb_ = entity(question)
        # Identifies search term
        search_query = ''
        if verb_:
            search_query += verb_[0]
            search_query += ' '
            search_query += ent_[0]
        else:
            search_query = ent_[0]
        # Write search term to log file
        mylogfile.write("Search term: {}\n".format(search_query))
        # Write raw results to log file
        ans_wiki = answer_wiki(search_query)
        mylogfile.write("Raw result: {}\n".format(ans_wiki))

        if ans_wiki == 'ERROR':
            mylogfile.write("Response: {}\n".format(error_answer))
            print(error_answer)
            continue
        formatted_text = re.sub(r'\[[0-9]*]', ' ', ans_wiki)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        sentences = sent_tokenize(formatted_text)
        quest_type = str(question).split()[0].lower()
        ans_grams = get_ngrams(quest_type, ent_[0], filtered_question, ans_wiki)
        # Determine response based on question type
        resp = ""
        if quest_type == 'who':
            if not verb_:
                resp = sentences[0]
            else:
                resp = get_entity_by_key_names(sentences, ans_grams, filtered_question)
        # Use sentence summary
        elif quest_type == 'what':
            resp = sentences[0]
        elif quest_type == 'when':
            resp = get_entity_by_key_dates(sentences, ans_grams, filtered_question, preposition)
        elif quest_type == 'where':
            resp = get_entity_by_key_places(sentences, ans_grams, filtered_question, preposition)
        print(resp)
        mylogfile.write("Response: {}\n".format(resp))
    print("Thank you for using the QA system. Have a great day!")
    mylogfile.close()


if __name__ == '__main__':
    main()