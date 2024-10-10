from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Helper function to load and save data
def load_data():
    if os.path.exists('data.json'):
        with open('data.json', 'r') as f:
            return json.load(f)
    else:
        return {'workouts': []}

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', workouts=data['workouts'])

@app.route('/add_workout', methods=['POST'])
def add_workout():
    data = load_data()
    workout = {
        'date': request.form['date'],
        'type': request.form['type'],
        'duration': int(request.form['duration']),
        'calories': int(request.form['calories'])
    }
    data['workouts'].append(workout)
    save_data(data)
    return redirect(url_for('index'))

@app.route('/stats')
def stats():
    data = load_data()
    total_duration = sum(workout['duration'] for workout in data['workouts'])
    total_calories = sum(workout['calories'] for workout in data['workouts'])
    return render_template('stats.html', total_duration=total_duration, total_calories=total_calories)

if __name__ == '__main__':
    app.run(debug=True)