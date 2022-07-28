from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys as surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

# responses = []  # list for user responses

response_key = "responses"

# surveys = {
#     "satisfaction": satisfaction_survey,
#     "personality": personality_quiz,
# }

@app.get('/')
def show_surveys():
    """ Give multiple survey options and let user choose which survey to take """

    return render_template("surveys.html", surveys = surveys)


@app.get('/start')
def show_start():
    """show home page to begin a survey"""

    session[response_key] = []

    return render_template("survey_start.html", survey=survey)


@app.post('/begin')
def start_survey():
    """redirects to first question of survey"""

    return redirect('/questions/0')


@app.get('/questions/<int:number>')  # if invalid number, redirect #call question id
def show_question(number):
    """shows a question from survey question list"""

    if (number) != len(session[response_key]):
        number = len(session[response_key])
        flash("Stop trying to mess with the question order!")
        return redirect(f"/questions/{number}")


    return render_template("question.html",
                    question=survey.questions[(number)])


@app.post("/answer")  # take answer for q1 and redirect to a get for q2
def log_response_and_redirect():
    """record answer for survey and redirect to next question
        or completion page if complete
    """

    responses = session[response_key]  # have to do this for sessions when appending
    # do this because you have to send a new cookie (rebinding on line 54)
    responses.append(request.form["answer"])
    session[response_key] = responses

    next_question_index = len(session[response_key])

    if next_question_index < len(survey.questions):
        return redirect(f"/questions/{next_question_index}")
    else:
        flash("Thanks for your input! We appericate you! I love you!")
        return redirect("/complete")

@app.get("/complete")
def show_completion():
    """show a completion page"""
    return render_template("completion.html")

# if you flash before render_template, it will flash multiple times
