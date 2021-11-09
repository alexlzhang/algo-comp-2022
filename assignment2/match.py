import numpy as np
from typing import List, Tuple
from collections import deque

def run_matching(scores: List[List], gender_id: List, gender_pref: List) -> List[Tuple]:
    """
    TODO: Implement Gale-Shapley stable matching!
    :param scores: raw N x N matrix of compatibility scores. Use this to derive a preference rankings.
    :param gender_id: list of N gender identities (Male, Female, Non-binary) corresponding to each user
    :param gender_pref: list of N gender preferences (Men, Women, Bisexual) corresponding to each user
    :return: `matches`, a List of (Proposer, Acceptor) Tuples representing monogamous matches

    Some Guiding Questions/Hints:
        - This is not the standard Men proposing & Women receiving scheme Gale-Shapley is introduced as
        - Instead, to account for various gender identity/preference combinations, it would be better to choose a random half of users to act as "Men" (proposers) and the other half as "Women" (receivers)
            - From there, you can construct your two preferences lists (as seen in the canonical Gale-Shapley algorithm; one for each half of users
        - Before doing so, it is worth addressing incompatible gender identity/preference combinations (e.g. gay men should not be matched with straight men).
            - One easy way of doing this is setting the scores of such combinations to be 0
            - Think carefully of all the various (Proposer-Preference:Receiver-Gender) combinations and whether they make sense as a match
        - How will you keep track of the Proposers who get "freed" up from matches?
        - We know that Receivers never become unmatched in the algorithm.
            - What data structure can you use to take advantage of this fact when forming your matches?
        - This is by no means an exhaustive list, feel free to reach out to us for more help!
    """

    # changing scores matrix based on certain metrics of gender compatibility
    N = len(scores)
    for i in range(N):
        for j in range(i+1, N):
            if (gender_id[i] == 'Nonbinary'):
                if ((gender_pref[i] == 'Men' and gender_id[j] == 'Female') or (gender_pref[i] == 'Women' and gender_id[j] == 'Male')):
                    scores[i][j] *= 0.5
                if (gender_id[j] == 'Nonbinary'):
                    scores[i][j] *= 0.9
            else:
                if (gender_pref[i] == 'Bisexual'):
                    if (gender_id[j] != 'Male' and gender_id[j] != 'Female'):
                        scores[i][j] *= 0.5
                if ((gender_pref[i] == 'Men' and gender_id[j] != 'Male') or (gender_pref[i] == 'Women' and gender_id[j] != 'Female')):
                    scores[i][j] *= 0.1
    # list of sets that contain the set of Receivers each Proposer has already proposed to
    already_proposed = []
    for i in range(N//2, N):
        already_proposed.append(set())
    # list of Proposers each Receiver is currently matched with
    curr_matchings = []
    for i in range(N//2):
        curr_matchings.append(-1)
    # queue of currently free Proposers
    proposers_queue = deque()
    for i in range(N//2, N):
        proposers_queue.append(i)
    # implementation of Gale-Shapley
    while (proposers_queue):
        curr_proposer = proposers_queue.popleft()
        curr_receiver = find_max_unproposed(scores, already_proposed[curr_proposer-N//2], curr_proposer)
        already_proposed[curr_proposer-N//2].add(curr_receiver)
        if curr_matchings[curr_receiver] == -1:
            curr_matchings[curr_receiver] = curr_proposer
        elif scores[curr_receiver][curr_matchings[curr_receiver]] < scores[curr_receiver][curr_proposer]:
            proposers_queue.append(curr_matchings[curr_receiver])
            curr_matchings[curr_receiver] = curr_proposer
        else:
            proposers_queue.append(curr_proposer)
    # putting finalized matches into matches array and returning
    matches = [()]
    for i in range(N//2):
        matches.append((i, curr_matchings[i]))
    return matches

# finds the Receiver of highest preference for a certain person who has not yet been proposed to by that person
# I'm sure there are more efficient ways of finding this than what I did (e.g. making a list of pairs of Receivers and associated preference for each Proposer and then sorting these lists by decreasing preference, but I don't currently have enough experience with Python to implement it this way)
def find_max_unproposed(scores: List[List], already_proposed_set: set, person: int):
    N = len(scores)
    currmax = 0
    currperson = 0
    for i in range(N//2):
        if scores[person][i] > currmax and i not in already_proposed_set:
            currmax = scores[person][i]
            currperson = i
    return currperson

if __name__ == "__main__":
    raw_scores = np.loadtxt('raw_scores.txt').tolist()
    genders = []
    with open('genders.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            genders.append(curr)

    gender_preferences = []
    with open('gender_preferences.txt', 'r') as file:
        for line in file:
            curr = line[:-1]
            gender_preferences.append(curr)

    gs_matches = run_matching(raw_scores, genders, gender_preferences)
    print(gs_matches)

# wrote this function just to brute force check if the matching was stable (i.e. my program worked on the test data and my modifications to the scores matrix)
def is_stable_matching(scores: List[List], curr_matchings: List):
    N = len(scores)
    for i in range(N//2):
        for j in range(N//2, N):
            j_position = -1
            for k in range(N//2):
                if curr_matchings[k] == j:
                    j_position = k
                    break
            if scores[i][j] > scores[i][curr_matchings[i]] and scores[j][i] > scores[j][j_position]:
                print(i)
                print(j)
                print("FALSE")
                return
    print("TRUE")
    return 