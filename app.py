import time
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from databasesetup import *

app = Flask(__name__)
CORS(app)

#Endpoint to display the graph
@app.route('/Weights')
def weight():
    time = select_time(r"PawsenseDB")
    weights = select_weights(r"PawsenseDB")
    return jsonify({"time_json": time, "weights_json": weights})
    header = "This is the weight line graph"
    return render_template('weight_line_graph.html', data=data, labels=labels, header=header)

@app.route('/pets')
def get_pets():
    pets = select_pets(r"PawsenseDB")
    return (pets)
@app.route('/pets/<int:pet_id>/', methods=['GET'])
def get_pet_id(pet_id):
    pet_by_id = get_by_pet_id(r"PawsenseDB", pet_id)
    return (pet_by_id)

@app.route('/login')
def get_user():
    user = get_users(r"PawsenseDB")
    return user

#Receive file from raspberry pi
@app.route('/upload_data', methods=['POST'])
def upload_data():
    time = ""
    weight = 0
    data_file = request.files['data']
    data_file.save('weight_data.txt')
    with open("weight_data.txt", 'r') as file:
        for line in file:
            parts = line.split(',')
            #split the different parts in each line of the file
            for part in parts:
                if part.strip().startswith("time:"):
                    time = part.strip().replace("time:", "").strip()
                elif part.strip().startswith("weight:"):
                    weight = float(part.strip().replace("weight:", "").strip())
            add_weight(r"PawsenseDB", time, weight)
    open('weight_data.txt', 'w').close() #empty file
    return 'File received successfully'

#Receive weight json object
@app.route('/upload_weight', methods=['POST'])
def upload_weight():
    value = request.json
    add_weight(r"PawsenseDB", value['time'], value['weight'])
    return "Data received successfully"

# create_connection(r"C:\sqlite\db\pawsense.db")

create_connection(r"PawsenseDB")
if __name__ == '__main__':
    app.run()
