from flask import Flask
import os
import sys

app = Flask(__name__)

sys.path.append("./views")
import Index
import StockPage

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'

if __name__ == "__main__":
    port = os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))
