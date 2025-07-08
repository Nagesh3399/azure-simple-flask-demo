from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

USERNAME = 'nagesh'
PASSWORD = 'churn'

login_template = '''
<!DOCTYPE html> 
<html>
<head>
    <title>Admin Login</title>
    <style>
        body {
            background-color: #121212;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h1 {
            margin-bottom: 40px;
            font-size: 28px;
            color: #00bcd4;
        }
        form {
            background-color: #1e1e1e;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 0 20px rgba(0, 188, 212, 0.3);
        }
        input {
            padding: 10px;
            margin: 10px 0;
            width: 250px;
            border: none;
            border-radius: 6px;
            font-size: 16px;
        }
        input[type="submit"] {
            background-color: #00bcd4;
            color: white;
            cursor: pointer;
            font-weight: bold;
            margin-left: 10px;
        }
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Integrated Decision Support Tool for Churn Analysis</h1>
    <form method="POST">
        <div><input type="text" name="username" placeholder="Username" required></div>
        <div><input type="password" name="password" placeholder="Password" required></div>
        <div><input type="submit" value="Login"></div>
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}
    </form>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template_string(login_template, error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return "<h2>Welcome to the Dashboard!</h2>"

if __name__ == "__main__":
    app.run(debug=True)
