from flask import Flask
import subprocess

app = Flask(__name__)

# Start virtual mouse
@app.route('/start')
def start_virtual_mouse():
    global process
    process = subprocess.Popen(["python", "src/mouse_control.py"])
    return "Virtual Mouse Started"

# Stop virtual mouse
@app.route('/stop')
def stop_virtual_mouse():
    process.terminate()
    return "Virtual Mouse Stopped"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
