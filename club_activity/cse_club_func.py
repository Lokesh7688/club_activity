from flask import json

with open("/home/ubuntu/club_activity/club_activity/cs_question/questions.json", "r") as json_data:
    questions = json.load(json_data)

points = 0
last_question = len(questions)
all_users = []



def question(question_number):
    question = questions[question_number]['question']
    return question


def good_answer(user_answer, question_number, questions):
    test = False
    if user_answer == questions[question_number]['answer']:
        test = True
    else:
        test = False
    return test


def next_answer(bad_answers, good_answer):
    if good_answer == 1:
        return True
    if bad_answers == 3:
        bad_answers = 0
        return True
    return False


def score(bad_answers):
    global points
    points += 3 - bad_answers
    return points


def activity_over(question):
    if question == last_question:
        return True
    else:
        False



def lb_add_stats(player, score, all_users):
    user_and_score = [player, score]
    all_users.append(user_and_score)
    return all_users


def lb_check_for_user(session_user, user_list):
    test = False
    for user in user_list:
        if user[0] == session_user:
            test = True
    return test


def lb_update_player_score(session_user, score, user_list):
    for user_stats in user_list:
        if user_stats[0] == session_user:
            user_stats[1] = score
    return user_list


def lb_winner(user_list):
    max = 0
    user = ''
    for user_points in user_list:
        if max < user_points[1]:
            max = user_points[1]
            user = user_points
    return user


def lb_sorted(user_list):
    ranking = []  # sorted list
    unsorted = 0
    unsorted = list(user_list)

    while lb_winner(unsorted) in unsorted:
        ranking.append(lb_winner(unsorted))
        unsorted.remove(lb_winner(unsorted))
    return ranking


def lb_position(player_name, user_list):
    my_list_len = len(user_list)
    for i in range(0, my_list_len):
        if user_list[i][0] == player_name:
            return i
