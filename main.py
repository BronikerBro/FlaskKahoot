from flask import Flask, render_template
import sqlite3


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

@app.route('/test/<id>',methods=['GET', 'POST'])
def test(id):
    connect = connect_to_db()
    cursor = connect.cursor()
    cursor.execute("""
         SELECT 
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
    cursor.execute("""SELECT * FROM quizes WHERE id==(?)""",[id])
    quizname = cursor.fetchall()
    return render_template('test.html', quiestions=questions, quizname=quizname)

@app.route('/result/', methods=['GET', 'POST'])
def result():
    return "Result"

app.run(debug=True)