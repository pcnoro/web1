from flask import Flask, request,render_template, render_template_string
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import subprocess
import re


app = Flask(__name__)


limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["5 per minute"],  # Default rate limit
    storage_uri="memory://",  # Store rate limits in memory
)




@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

# Hidden endpoint
@app.route('/here_we_go', methods=['GET', 'POST'])
@limiter.limit("20 per minute")
def hidden_endpoint():
    output = None
    if request.method == 'POST':
        user_input = request.form.get('input')
        user_input = re.sub(r"[;&|$()]", "", user_input)
        try:
            # Vulnerable command execution
            command = f"bash -c 'cowsay {user_input}'"
            output = subprocess.check_output(
                command,
                shell=True,  # This is the vulnerability!
                stderr=subprocess.STDOUT
            ).decode()
        except subprocess.CalledProcessError as e:
            output = f"🧙‍♂️ Abracadabra! Your spell failed! (I'm using filtration to block special characters. Can you bypass it?)"

    return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hidden Endpoint</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    flex-direction: column;
                }}
                .container {{
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    width: 300px;
                    text-align: center;
                }}
                input[type="text"] {{
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                }}
                input[type="submit"] {{
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                input[type="submit"]:hover {{
                    background-color: #0056b3;
                }}
                .output {{
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #e9ecef;
                    border-radius: 4px;
                    white-space: pre-wrap;
                    text-align: left;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Generator</h2>
                <form method="POST">
                    <input type="text" name="input" placeholder="Enter text">
                    <input type="submit" value="Submit">
                </form>
                {f'<div class="output"><strong>Output:</strong><br>{output}</div>' if output else ''}
            </div>
        </body>
        </html>
    '''

@app.route('/you_just_wasting_time', methods=['GET'])
def wasting_time():
    return '''
        <h1 style="text-align: center;"> i realy mean it, you just wasting time</h1>
    '''


@app.errorhandler(429)
def ratelimit_handler(e):
    return "Too many requests! Try again later.", 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
