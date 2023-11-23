import time
from datetime import datetime
from flask import Flask, request, render_template, jsonify
#from flask_cors import CORS
from databasesetup import *

app = Flask(__name__)
#CORS(app)

time_data = []
weight_data = []
def read_data(file):
    with open(file, 'r') as file:
        for line in file:
            parts = line.split(',')
            for part in parts:
                if part.strip().startswith("time:"):
                    time = part.strip().replace("time:", "").strip()
                    time_data.append(time)
                elif part.strip().startswith("weight:"):
                    weight = float(part.strip().replace("weight:", "").strip())
                    weight_data.append(weight)

data_file = 'weight_data.txt'
read_data(data_file)
@app.route('/Weights')
def weight():
    time = [datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d %I:%M %p') for time in time_data]
    weights = weight_data
    return jsonify({"time_json": time, "weights_json": weights})
    header = "This is the weight line graph"
    return render_template('weight_line_graph.html', data=data, labels=labels, header=header)

@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/pets')
def get_pets():
    pets = select_pets(r"PawsenseDB")
    return pets

@app.route('/weights')
def get_weights():
    weights = select_weights(r"PawsenseDB")
    return weights

@app.route('/upload_data', methods=['POST'])
def upload_data():
    data_file = request.files['data']
    data_file.save('weight_data.txt')
    return 'File received successfully'

@app.route('/upload_weight', methods=['POST'])
def upload_weight():
    value = request.json
    add_weight(r"PawsenseDB", value['time'], value['weight'])
    return "Data received successfully"

# create_connection(r"C:\sqlite\db\pawsense.db")

create_connection(r"PawsenseDB")
if __name__ == '__main__':
    app.run()
