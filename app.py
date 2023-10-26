import time
from flask import Flask
from flask_cors import CORS
from databasesetup import *

app = Flask(__name__)
CORS(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}


print("???")
# create_connection(r"C:\sqlite\db\pawsense.db")
#
# create_connection(r"PawsenseDB")
if __name__ == '__main__':
    app.run()


