import sqlite3
import random

connection = sqlite3.connect("quiz.db")

cursor = connection.cursor()
# cursor.execute("DROP TABLE IF EXISTS connection_quiz_quest")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        question TEXT NOT NULL,
        right_answer TEXT NOT NULL, 
        wrong_answer1 TEXT NOT NULL,
        wrong_answer2 TEXT NOT NULL,
        wrong_answer3 TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS quizes(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name VARCHAR(100) NOT NULL,
        age_from INTEGER,
        age_to INTEGER
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS connection_quiz_quest(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        id_question INTEGER,
        id_quiz INTEGER,
        FOREIGN KEY (id_question) REFERENCES questions(id)
        FOREIGN KEY (id_quiz) REFERENCES quizes(id)
    )
""")
cursor.execute('''PRAGMA foreign_keys=on''')



# cursor.execute("""
#     INSERT INTO questions(question, right_answer, wrong_answer1, wrong_answer2, wrong_answer3)
#     VALUES ("Що таке паляниця?", "Хліб", "Клубніка", "Танк", "Біолабороторія")
# """)
# questions = [
#     ["Хто був першим президентом України?", "Леонід Кравчук", "Володимир Зеленський", "Віктор Янукович", "Віктор Ющенко"],
#     ["Яку столицю має Австралія?", "Канберра", "Сідней", "Мельбурн", "Аделаїда"],
#     ["Хто був режисером фільму \"Престиж\"?", "Крістофер Нолан", "Стівен Спілберг", "Квентін Тарантіно", "Дін Росс"],
#     ["Хто був автором пісні \"Bohemian Rhapsody\"?", "Фредді Меркьюрі", "Джон Леннон", "Роджер Тейлор", "Брайан Мей"],
#     ["Як імпортувати sqlite?", "import sqlite3", "import sqlite", "import mysql", "import sqlite4"],
#     ["Який відсоток населення України проживає в містах?", "75%", "25%", "50%", "90%"],
#     ["В якому році Україна стала незалежною державою?", "1991", "2001", "2011", "1981"],
#     ["Який метод використовується для виконання запитів до бази даних?", "execute()", "cursor()", "fetchall()", "commit()"],
#     ["Який фільм від Marvel вийшов у лютому 2023", "Людина-мураха та Оса: Квантоманія", "Тор: Любов і грім", "Доктор Стрендж у мультивсесвіті божевілля", "Аватар 2: шлях води"]
# ]

quest_request = """
    INSERT INTO questions(question, right_answer, wrong_answer1, wrong_answer2, wrong_answer3)
    VALUES (?, ?, ?, ?, ?)
"""
quiz_request = """
    INSERT INTO quizes(name, age_from, age_to)
    VALUES (?, ?, ?)
"""
# quizes = [
#     ["Патріотична вікторина", 0, 100],
#     ["Розумники та розумниці", 10 , 30],
#     ["Потужність знань", 15, 70]
# ]
# cursor.executemany(request, questions)
# cursor.executemany(quiz_request, quizes)
connect_request = """
    INSERT INTO connection_quiz_quest (id_question, id_quiz)
    VALUES (?, ?)
"""
# cursor.execute(connect_request, [1, 1])
# cursor.execute(connect_request, [2, 1])
# cursor.execute(connect_request, [7, 1])
# cursor.execute(connect_request, [8, 1])
# cursor.execute(connect_request, [3, 2])
# cursor.execute(connect_request, [10, 2])
# cursor.execute(connect_request, [4, 3])
# cursor.execute(connect_request, [5, 3])
# cursor.execute(connect_request, [9, 3])
# cursor.execute(connect_request, [6, 3])
connection.commit()

choice = int(input("Оберіть вікторину яку б ви хотіли пройти: "))
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
""", [choice])
# cursor.execute("SELECT * FROM connection_quiz_quest")
data = cursor.fetchall()
for i in data:
    print(i[0])
    answers = list(i)
    random.shuffle(answers)
    answers.remove(i[0])
    right = answers.index(i[1])+1
    for i in range(len(answers)):
        print(str(i+1)+") "+answers[i])
    answ = int(input("Правильна відповідь (введіть число): "))
    print("\n")
    if answ == right: print("Вірно! :)")
    else: print("Неправильно :(")
    print("\n")

