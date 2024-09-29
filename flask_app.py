from flask import Flask
import threading
from outlawmark1 import main as bot_main  # Import the main function from your bot script

app = Flask(__name__)

@app.route('/')
def index():
    return 'Bot is running!'

def run_flask():
    app.run(host='0.0.0.0', port=5001)

if __name__ == '__main__':
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Run the bot in the main thread
    bot_main()

