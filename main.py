from flask import Flask, render_template, request, url_for, redirect
import sqlite3
import random

app = Flask(__name__)

def connect_to_db():
    connect = sqlite3.connect("quiz.db")
    connect.row_factory = sqlite3.Row
    return connect

@app.route('/', methods=['GET', 'POST'])
def index():
    connect = connect_to_db()
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM quizes")
    auizes = cursor.fetchall()
    return render_template('index.html', quizes=auizes)


@app.route('/test/',methods=['GET', 'POST'])

def test():
    if request.method == "GET":
        global i
        i = 0
        id = request.args.get("id")
        connect = connect_to_db()
        cursor = connect.cursor()
        cursor.execute("""
             SELECT 
            questions.id,
            questions.question, 
            questions.right_answer,
            questions.wrong_answer1, 
            questions.wrong_answer2, 
            questions.wrong_answer3
            FROM connection_quiz_quest, questions
            WHERE connection_quiz_quest.id_quiz == (?)
            AND questions.id == connection_quiz_quest.id_question
        """, [id])
        questions = cursor.fetchall()
        cursor.execute("""SELECT  * FROM quizes WHERE id==(?)""",[id])
        quizname = cursor.fetchall()
        # quests = []
        # for quest in questions:
        #     answers = list(quest)
        #     random.shuffle(answers)
        #     answers.remove(quest[0])
        #     answers.remove(quest[1])
        #     answers.insert(0, quest[0])
        #     answers.insert(1, quest[1])
        #     quests.append(answers)
        # print(quests)
        for quest in questions:
            quest = list(quest)
        quest = questions[int(i)]
        return render_template('test.html', quest=quest, quizname=quizname)
    elif request.method == "POST":
        if i == 0:
            global count
            count = 0
        if "right_answer" in str(request.form):
            count+=1
        else:
            count += 0
        i+=1
        id = request.args.get("id")
        connect = connect_to_db()
        cursor = connect.cursor()
        cursor.execute("""
                     SELECT 
                    questions.id,
                    questions.question, 
                    questions.right_answer,
                    questions.wrong_answer1, 
                    questions.wrong_answer2, 
                    questions.wrong_answer3
                    FROM connection_quiz_quest, questions
                    WHERE connection_quiz_quest.id_quiz == (?)
                    AND questions.id == connection_quiz_quest.id_question
                """, [id])
        questions = cursor.fetchall()
        cursor.execute("""SELECT  * FROM quizes WHERE id==(?)""", [id])
        quizname = cursor.fetchall()
        # quests = []
        # for quest in questions:
        #     answers = list(quest)
        #     random.shuffle(answers)
        #     answers.remove(quest[0])
        #     answers.remove(quest[1])
        #     answers.insert(0, quest[0])
        #     answers.insert(1, quest[1])
        #     quests.append(answers)
        # print(quests)
        for quest in questions:
            quest = list(quest)
        try:
            quest = questions[int(i)]
        except IndexError:
            res =  int(count)/int(len(questions))
            return redirect(url_for('result', res=res))
        return render_template('test.html', quest=quest, quizname=quizname)


@app.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == "GET":
        res =request.args.get("res")
    return str(res)

app.run(debug=True)