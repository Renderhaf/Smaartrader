from flask import Flask
import os
import sys

app = Flask(__name__,static_folder='web/static',
                    template_folder='web/templates')

print("Starting Info Package...")
sys.path.append("./views")
import Index
import StockPage
import StockAPI
print("Info Package Started!")

app.config['DEBUG'] = True
app.config['HOST'] = 'localhost'

if __name__ == "__main__":
    port = os.environ.get('PORT') or 5000
    app.run(host='0.0.0.0', port=int(port))
