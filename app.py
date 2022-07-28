from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []  # list for user responses


@app.get('/')
def show_home():
    """show home page to begin a survey"""

    session["responses"] = []

    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survey():
    """redirects to first question of survey"""

    return redirect('/questions/0')


@app.get('/questions/<number>')  # if invalid number, redirect
def show_question(number):
    """shows a question from survey question list"""

    if int(number) != len(session["responses"]):
        number = len(session["responses"])
        flash("Stop trying to mess with the question order!")
        return redirect(f"/questions/{number}")


    return render_template("question.html",
                    question=survey.questions[int(number)])


@app.post("/answer")  # take answer for q1 and redirect to a get for q2
def log_response_and_redirect():
    """record answer for survey and redirect to next question
        or completion page if complete
    """

    responses = session["responses"]  # have to do this for sessions when appending
    responses.append(request.form["answer"])
    session["responses"] = responses

    next_question_index = len(session["responses"])

    if next_question_index < len(survey.questions):
        return redirect(f"/questions/{next_question_index}")
    else:
        flash("Thanks for your input! We appericate you! I love you!")
        return redirect("/complete")

@app.get("/complete")
def show_completion():
    """show a completion page"""
    return render_template("completion.html")

