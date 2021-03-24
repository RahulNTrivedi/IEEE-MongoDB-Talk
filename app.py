import pymongo
import jsonify
from pymongo import MongoClient
from flask import Flask, request, jsonify

app = Flask(__name__)
client = MongoClient('')

@app.route('/list', methods=['GET'])
def listOfCharacters():
    db = client.show
    characters = db['characters']
    list = []
    for document in characters.find({}, {"_id": 0}):
        list.append(document)
    return jsonify(list)

@app.route('/character', methods=['GET'])
def getCharacter():
    input =  request.args.get("name")
    db = client.show
    characters = db['characters']
    character = characters.find_one({"name": input})
    returnVal = {
        "name": character["name"],
        "age": character["age"],
        "bending": character["bending"]
    }
    return jsonify(returnVal)

@app.route('/addCharacter', methods=['POST'])
def addCharacter():
    input = request.get_json()
    dict = {
        "name": input["name"],
        "age": input["age"],
        "bending": input["bending"]
    }
    db = client.show
    characters = db['characters']
    characters.insert_one(dict)
    return "success"

@app.route('/removeCharacter', methods=['POST'])
def removeCharacter():
    input = request.get_json()
    db = client.show
    characters = db['characters']
    characters.delete_one({"name": input["name"]})
    return "success"

@app.route('/updateCharacter', methods=['POST'])
def updateCharacter():
    input = request.get_json()
    db = client.show
    characters = db['characters']
    doc = characters.find_one({"name" : input["name"]})
    details = {
        "age": input["age"],
        "bending": input["bending"]
    }
    characters.update_one( doc, {"$set":details})
    return "success"


if __name__ == "__main__":
    app.run()
