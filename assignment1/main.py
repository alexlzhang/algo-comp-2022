#!usr/bin/env python3
import json
import sys
import os

INPUT_FILE = 'testdata.json' # Constant variables are usually in ALL CAPS

class User:
    def __init__(self, name, gender, preferences, grad_year, responses):
        self.name = name
        self.gender = gender
        self.preferences = preferences
        self.grad_year = grad_year
        self.responses = responses


# Takes in two user objects and outputs a float denoting compatibility
def compute_score(user1, user2):
    #if (user2.gender not in user1.preferences or user1.gender not in user2.preferences):
    if (user2.preferences.count(user1.gender) == 0 or user1.preferences.count(user2.gender) == 0):
        return 0
    score = 0
    for i in range(20):
        if (user1.responses[i] == user2.responses[i]):
            score+=0.05
    if (abs(user1.grad_year*user2.grad_year) == 1):
        score*=0.8
    if (abs(user1.grad_year*user2.grad_year) == 2):
        score*=0.6
    if (abs(user1.grad_year*user2.grad_year) == 3):
        score*=0.4
    return score


if __name__ == '__main__':
    # Make sure input file is valid
    if not os.path.exists(INPUT_FILE):
        print('Input file not found')
        sys.exit(0)

    users = []
    with open(INPUT_FILE) as json_file:
        data = json.load(json_file)
        for user_obj in data['users']:
            new_user = User(user_obj['name'], user_obj['gender'],
                            user_obj['preferences'], user_obj['gradYear'],
                            user_obj['responses'])
            users.append(new_user)

    for i in range(len(users)-1):
        for j in range(i+1, len(users)):
            user1 = users[i]
            user2 = users[j]
            score = compute_score(user1, user2)
            print('Compatibility between {} and {}: {}'.format(user1.name, user2.name, score))
