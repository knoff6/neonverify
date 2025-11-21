import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'neon_verify_secret_key_cyberpunk_2077'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect('neonverify.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()

        # VULNERABILITY: SQL Injection
        # Directly formatting the string allows ' OR 1=1 -- style attacks
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        
        try:
            cursor.execute(query)
            user = cursor.fetchone()
            conn.close()

            if user:
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('dashboard'))
            else:
                flash('Access Denied: Invalid Credentials', 'danger')
        except Exception as e:
            flash(f'System Error: {str(e)}', 'danger')
            
    return render_template('login.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        if file:
            # VULNERABILITY: No file extension validation
            # Allows uploading .php, .py, .sh, etc.
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # VULNERABILITY: Remote Code Execution (RCE)
            # The system "verifies" the file by executing it.
            # This is a massive security flaw allowing attackers to run arbitrary code.
            try:
                # Using subprocess to run the file. 
                # If it's a python script, we run it with python.
                # If it's a shell script, we run it with sh.
                # For simplicity in this CTF, we'll just try to execute it if it's a .py file
                if filename.endswith('.py'):
                    import subprocess
                    subprocess.Popen(['python', filepath])
                    flash(f'Verification process started for {filename}...', 'success')
                else:
                    flash(f'File {filename} uploaded. Verification pending manual review.', 'warning')
            except Exception as e:
                flash(f'Error during verification: {str(e)}', 'danger')

            return redirect(url_for('dashboard'))

    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible if needed, debug=False for "production" feel but True helps dev
    app.run(host='0.0.0.0', port=5000, debug=True)
