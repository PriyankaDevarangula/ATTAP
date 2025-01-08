from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from flask_socketio import SocketIO, emit, join_room
import random
import string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Priya@2003',  # Replace with your MySQL password
    'database': 'attap'  # Replace with your database name
}

def get_db_connection():
    """Establish and return a database connection."""
    return mysql.connector.connect(**db_config)

@app.route('/')
def dash():
    return render_template('dash.html')


# Route: Game Selection Page
@app.route('/game_selection')
def game_selection():
    return render_template('game_selection.html')


# Route: Quiz Game Page
@app.route('/quiz_game')
def quiz_game():
    return render_template('quiz_game.html')


# Route: Code Challenge Page (Currently redirects to Quiz Game)
@app.route('/code_challenge')
def code_challenge():
    return redirect(url_for('quiz_game'))


@app.route('/question_selector', methods=['GET', 'POST'])
def question_selector():
    # Initialize empty questions list
    questions = []

    # Retrieve the topic filter from query parameters
    topic = request.args.get('topic')

    if topic:
        try:
            # Establish database connection
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            # Query to fetch questions based on the selected topic
            query = """
                SELECT id, title
                FROM problems
                WHERE topic = %s
            """
            cursor.execute(query, (topic,))
            questions = cursor.fetchall()

            # Close the cursor and connection
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"Database error: {err}")

    return render_template('question_selector.html', questions=questions)

@app.route('/coding_environment/<int:question_id>')
def coding_environment(question_id):
    # Query the database to get question details
    question = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch question details using question_id
        query = "SELECT * FROM problems WHERE id = %s"
        cursor.execute(query, (question_id,))
        question = cursor.fetchone()

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

    # Render coding environment template
    return render_template('coding_environment.html', question=question)

from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
import random
import string

socketio = SocketIO(app)

# Helper function to generate a random room ID
def generate_room_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route('/create_room', methods=['GET', 'POST'])
def create_room():
    room_name = None
    room_id = None 
    if request.method == 'POST':
        room_name = request.form['room_name']
        
        # Generate a unique room ID
        room_id = generate_room_id()
        
        # Emit the room ID and other details to the client using WebSocket
        socketio.emit('room_created', {'room_id': room_id, 'room_name': room_name})

        return render_template('create_room.html', room_name=room_name, room_id=room_id)

    return render_template('create_room.html', room_name=room_name, room_id=room_id)

# Route for joining a room via the quiz game page (client side)
@app.route('/join_room')
def join_room():
    # Redirect to the student room page
    return redirect(url_for('student_room'))

@app.route('/student_room')
def student_room():
    return render_template('student_room.html')


if __name__ == '__main__':
    socketio.run(app, debug=True)
