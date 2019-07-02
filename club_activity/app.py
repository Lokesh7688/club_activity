import os
from flask import Flask, render_template, request, flash, json, session, redirect, url_for
from cse_club_func import lb_check_for_user, lb_update_player_score, lb_sorted, good_answer, lb_winner

app = Flask(__name__)
app.secret_key = 'secret'
all_users = []
ranking = []

with open("cs_question/questions.json", "r") as json_data:
    questions = json.load(json_data)


@app.route('/', methods=["GET", "POST"])
def index():
    session['next-answer'] = 0

    if 'user' not in session:
        return redirect(url_for("user"))
    if session['user'] == "":
        return redirect(url_for("user"))

    session['good-answer'] = 'none'
    user_answer = 'none'

    if request.method == "POST":
        session['good-answer'] = good_answer(request.form["answer"], session['current_question'], questions)
        session['next-answer'] = good_answer(request.form["answer"], session['current_question'], questions)
        user_answer = request.form["answer"]

        if session['next-answer'] and len(questions) != session['current_question']:
            session['current_question'] = session['current_question']

        if not session['next-answer']:
            session['bad_answers'] += 1
        else:
            session['score'] += 3 - session['bad_answers']


        if session['bad_answers'] == 3:
            session['next-answer'] = True
            session['bad_answers'] = 0

        if session['next-answer']:
            session['current_question'] += 1

        if session['current_question'] == len(questions):
            session['current_question'] = 0

        if session['next-answer']:
            flash("{}".format('Next Question'))
        elif request.form["answer"] == "":
            flash("{}".format(''))
        else:
            flash("{}".format('Bad Answer'))
    ranking = []

    if not lb_check_for_user(session["user"], all_users):
        user_and_score = [session["user"], session["score"]]
        all_users.append(user_and_score)
    else:
        lb_update_player_score(session["user"], session["score"], all_users)
        if all_users != []:
            ranking = lb_sorted(all_users)

    return render_template("home.html",
                           active_page='index',
                           question=questions[session['current_question']]["question"],
                           question_number=session['current_question'],
                           score=session['score'],
                           users=ranking,
                           user_answer=user_answer,
                           good_answer=session['good-answer'],
                           last_question=len(questions),
                           user_name=session['user'],
                           winner=lb_winner(all_users),
                           check=lb_check_for_user(all_users, session["user"])
                           )


@app.route('/user', methods=["GET", "POST"])
def user():
    session["score"] = 0
    session["bad_answers"] = 0
    session['current_question'] = 0
    if request.method == "POST":
        session['user'] = request.form["answer"]
        if session['user'] != "" and not lb_check_for_user(session['user'], all_users):
            user_and_score = [session["user"], session["score"]]
            all_users.append(user_and_score)
            return redirect(url_for("index"))
        if lb_check_for_user(session['user'], all_users):
            flash("{}".format('User already in leaderboard'))
    ranking = []
    ranking = lb_sorted(all_users)
    return render_template("home.html", question_number=0,
                           question='Whats Your name?',
                           winner=lb_winner(all_users),
                           users=ranking,
                           last_question=5)


@app.route('/reset')
def reset():
    session['current_question'] = 0
    session['bad_answers'] = 0
    session['score'] = 0
    return redirect(url_for("index"))


@app.route('/lb_reset')
def lb_reset():
    session['current_question'] = 0
    session['bad_answers'] = 0
    session['score'] = 0
    global all_users, ranking
    all_users = []
    ranking = []
    return redirect(url_for("index"))


@app.route('/about')
def about():
    return render_template("about.html", active_page='about')


if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True, threaded=True)

