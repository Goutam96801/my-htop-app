from flask import Flask, render_template_string
import subprocess
import datetime
import pytz
import os

app = Flask(__name__)

def get_top_output():
    """Gets the output of the 'top' command."""
    try:
        result = subprocess.run(['top', '-b', '-n', '1'], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error running top: {e}"

@app.route('/htop')
def htop_endpoint():
    """Displays system information and top output."""

    username = os.environ.get('USER', 'Unknown User')

    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.datetime.now(ist)
    server_time_ist = now.strftime('%Y-%m-%d %H:%M:%S %Z%z')

    top_output = get_top_output()
    
    my_name = "Goutam Kumar Choudhary" 


    template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>htop Output</title>
        <style>
            body {
                font-family: monospace;
                white-space: pre; /* Crucial for preserving top's formatting */
            }
        </style>
    </head>
    <body>
        <h1>System Information</h1>
        <p>Name: {{ name }}</p>
        <p>user: {{ username }}</p>
        <p>Server Time (IST): {{ server_time }}</p>
        <h2>TOP output:</h2>
        <pre>{{ top_output }}</pre>
    </body>
    </html>
    """

    return render_template_string(template, name=my_name, username=username, server_time=server_time_ist, top_output=top_output)
  
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000, debug=False) 