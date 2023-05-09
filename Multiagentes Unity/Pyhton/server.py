from flask import Flask, request, jsonify
from main_SinkoPeso_Ver1 import *

index_count = -1

parameters = {  
    'gridsize': 23,
    'cars': 20,
    'steps': 1000,
    'turn_chance': 0.5,
    'car_chance': 0.1,
    'min_time_light': 10,
    'max_time_light': 15,
}

model = IntersectionModel(parameters)
results = model.run()
position = model.json

app = Flask("Test")

def curr_position(position,index_count):

    json = {}

    json["parameters"] = position["parameters"]

    json["step"] = index_count
    
    for car in position["step"][index_count]["car"]:
        new_car = {}
        new_car["x"] = car["x"]
        new_car["y"] = car["y"]
        new_car["id"] = car["id"]
        new_car["new"] = car["new"]
        json["car_" + str(car["id"])] = new_car

    for light in position["step"][index_count]["traffic_light"]:
        new_light = {}
        new_light["id"] = light["id"]
        new_light["light_state"] = light["light"]
        json["light_" +str(light["id"])] = new_light

    return json

@app.route('/', methods=['GET'])
def agents_position():
    if request.method == 'GET':
        global index_count
        global position
        global parameters
        if index_count < parameters['steps']:
            index_count += 1
            return curr_position(position,index_count)
        return jsonify({"model": "NA"})

@app.route('/1', methods=['GET'])
def agents_position2():
    if request.method == 'GET':
        global index_count
        global position
        global parameters
        aux = index_count+1
        if aux < parameters['steps']:
            return curr_position(position,aux)
        return jsonify({"model": "NA"})


if __name__=='__main__':
    app.run(host="localhost", port=8080, debug=True)