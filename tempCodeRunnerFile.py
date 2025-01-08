from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Priya@2003',  # Replace with your MySQL password
    'database': 'attap'  # Replace with your database name
}

# Connect to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Home route
@app.route('/')
def home():
    return render_template('dash.html')  # This is your home page

# Route for Game Selection Page
@app.route('/game_selection')
def game_selection():
    return render_template('game_selection.html')  # This is the page for game selection

# Route for Quiz Game Page
@app.route('/quiz_game')
def quiz_game():
    return render_template('quiz_game.html')  # This renders quiz_game.html page

# Route for Quiz Host Page
@app.route('/quiz_host')
def quiz_host():
    return render_template('quiz_host.html')  # This renders quiz_host.html page

@app.route('/quiz_options.html')
def quiz_options():
    # Handle the request for quiz_options.html here
    return render_template('quiz_options.html')

@app.route('/add_questions')
def add_questions():
    return render_template('add_questions.html')

@app.route('/select_questions')
def select_questions():
    selected_topics = request.args.get('topics', '').split(',')

    if not selected_topics:
        return redirect(url_for('game_selection'))

    # Fetch questions for the selected topics
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query the database to fetch questions for the selected topics
    query = """
        SELECT question_id, topic, question, option1, option2, option3, option4
        FROM quiz_questions
        WHERE topic IN (%s)
    """ % ','.join(['%s'] * len(selected_topics))  # Create placeholders for topic parameters

    cursor.execute(query, selected_topics)
    questions = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('select_questions.html', topics=selected_topics, questions=questions)

@app.route('/fetch_questions', methods=['GET'])
def fetch_questions():
    topic = request.args.get('topic')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT question_id, topic, question, option1, option2, option3, option4, correct_answer 
            FROM quiz_questions 
            WHERE topic = %s
        """
        cursor.execute(query, (topic,))
        questions = cursor.fetchall()

        return jsonify({"questions": questions})
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({"questions": []})
    finally:
        cursor.close()
        connection.close()



if __name__ == '__main__':
    app.run(debug=True)