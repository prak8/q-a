# Question & Answer System

## Project Information

AIT 526
Programming Assignment 2
Author: Team 1 - Alice Chen, Hrishikesh Karambelkar, Prakriti Panday, Sean Park

## Description of the problem to be solved

The objective of this assignment involves building a question and answer system. Similar to a chatbot, this system will take a question as an input and provide back a one sentence answer. The questions have to be either who/what/where/when questions. In that way, the answer returned will simply respond to the specific detail requested in the question. The system developed utlizes a wikipedia package from python that facilitates with searching an answer to the factual question. This system incorporates chatbot style system entailing re expressions and token extraction, along with named entity recognition for deciphering the content of the question and finally text summarization in order to give back a user friendly response.

** Python suggest multiple downloads.

## An actual example of program output and usage

Figure A below shows the log output of the question answer system

Figure B shows the system repsonse and the actual response

Usage Instruction

Upon running the file qa-system.py, the user is prompted with a greeting and a brief description of the type of questions recognized by the system. Next, the user is allowed to type in their question. As the system responds with an answer, the script of the entire exchange between the user and the system for a particular session can be accessed as a text file on the same directory as the original file. If the system is unable to decipher the content of the question, it will respond with a 'sorry' message. Finally, by typing in 'exit', the user can end a session. 



## Algorithm 

Description

* Enter the question
* Tokenize the question and extract the entities, nouns and verbs
* Apply the extracted object into a search field on wikipedia
* Parse the summary on wikipedia, locating the entity, noun and verb token associated with the question
* If succesfully with locating the provided tokens, print the associated entity object, along with the verb placement as scripted.


A flowdiagram of the QA system


<img width="1261" alt="Screen Shot 2021-11-22 at 1 44 28 PM" src="https://user-images.githubusercontent.com/90986120/142917702-1fa8bc97-3dcb-4678-826f-2efdce0c4626.png">
