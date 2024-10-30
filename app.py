from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

# Add this line to configure the Jinja2 environment
app.jinja_env.globals['now'] = datetime.utcnow

DATABASE = 'trick_or_treaters.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trick_or_treaters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database before running the app
if not os.path.exists(DATABASE):
    init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM trick_or_treaters')
    count = c.fetchone()[0]
    conn.close()
    return render_template('index.html', count=count)

@app.route('/add', methods=['POST'])
def add_trick_or_treater():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO trick_or_treaters (timestamp) VALUES (?)', (datetime.now().isoformat(),))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_data():
    if request.form.get('confirm') == 'yes':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM trick_or_treaters')
        conn.commit()
        conn.close()
        flash('Data has been reset.')
    return redirect(url_for('index'))

@app.route('/export')
def export_data():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM trick_or_treaters')
    data = c.fetchall()
    conn.close()

    filename = 'trick_or_treaters.csv'
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['ID', 'Timestamp'])
        csvwriter.writerows(data)

    return send_file(filename, as_attachment=True)

@app.route('/graphs')
def graphs():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT timestamp FROM trick_or_treaters ORDER BY timestamp')
    timestamps = [datetime.fromisoformat(row[0]) for row in c.fetchall()]
    conn.close()

    if not timestamps:
        # No data to display
        return render_template('graphs.html', data_available=False)

    # Prepare data for cumulative graph (5-minute bins)
    cumulative_data = get_binned_data(timestamps, bin_size_minutes=5, cumulative=True)

    # Prepare data for count graph (15-minute bins)
    count_data = get_binned_data(timestamps, bin_size_minutes=15, cumulative=False)

    return render_template(
        'graphs.html',
        data_available=True,
        cumulative_data=cumulative_data,
        count_data=count_data
    )

def get_binned_data(timestamps, bin_size_minutes, cumulative):
    # Determine the time range
    start_time = timestamps[0].replace(second=0, microsecond=0)
    end_time = timestamps[-1].replace(second=0, microsecond=0) + timedelta(minutes=bin_size_minutes)

    # Create bins
    bins = []
    labels = []
    current_time = start_time
    while current_time <= end_time:
        bins.append(current_time)
        labels.append(current_time.strftime('%H:%M'))
        current_time += timedelta(minutes=bin_size_minutes)

    # Initialize counts
    counts = [0] * (len(bins) - 1)

    # Count trick-or-treaters in each bin
    idx = 0
    for timestamp in timestamps:
        while idx < len(bins) - 1 and timestamp >= bins[idx + 1]:
            idx += 1
        if idx < len(counts):
            counts[idx] += 1

    if cumulative:
        cumulative_counts = []
        total = 0
        for count in counts:
            total += count
            cumulative_counts.append(total)
        return {'labels': labels[:-1], 'counts': cumulative_counts}
    else:
        return {'labels': labels[:-1], 'counts': counts}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
