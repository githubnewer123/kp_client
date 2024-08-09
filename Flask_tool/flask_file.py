import logging  
from flask import Flask ,render_template

app = Flask(__name__)  
app.logger.setLevel(logging.DEBUG)  

@app.route('/')  
def home():  
    try:  
        return render_template('index.html')  
    except Exception as e:  
        app.logger.error(f"Error rendering template: {e}")  
        return "An error occurred", 500  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=3000, debug=True)