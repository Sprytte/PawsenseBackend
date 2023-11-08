import time
from flask import Flask, request
from flask_cors import CORS
from databasesetup import *

app = Flask(__name__)
CORS(app)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/pets')
def get_pets():
    pets = select_pets(r"PawsenseDB")
    return pets

@app.route('/upload_data', methods=['POST'])
def upload_data():
    data_file = request.files['data']
    data_file.save('weight_data.txt')
    return 'Data received successfully'

# create_connection(r"C:\sqlite\db\pawsense.db")
#
# create_connection(r"PawsenseDB")
if __name__ == '__main__':
    app.run()


