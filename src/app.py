from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash
from bson import json_util, ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/pythonmongodb'

mongo = PyMongo(app)

@app.route('/users', methods=['POST'])
def create_user():

    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    if username and email and password:
        
        hashed_password = generate_password_hash(password)
        id = mongo.db.users.insert_one(
            {
                "username": username,
                "password": hashed_password,
                "email": email
            }
        )

        response = {
            "id": str(id),
            "username": username,
            "password": hashed_password,
            "email": email
        }

        return response
    else:
        return not_found(), 404

@app.route('/users', methods=['GET'])
def get_user():
    users = mongo.db.users.find()
    response = json_util.dumps(users)

    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['GET'])
def get_byID(id):
    obj = ObjectId(id)
    users = mongo.db.users.find({'_id': obj})
    response = json_util.dumps(users)

    return Response(response, mimetype='application/json')

@app.route('/users/<id>', methods=['DELETE'])
def delete_byID(id):
    user = mongo.db.users.delete_one({'_id': ObjectId(id)})

    response = jsonify({
        'message': 'User' + id + 'Deleted Successfully'
    })

    return response

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resouce not found' + request.url,
        'status': 404
    }

    return message

@app.route('/users/<id>', methods=['PUT'])
def upadate_user(id):

    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    if username and password and email and id:
        hashed_password = generate_password_hash(password)

        mongo.db.update_one({'id':ObjectId(id)}, {'$set': {
            'username': username,
            'password': password,
            'email': email
        }})

        response = jsonify({'message': 'User' + id + 'Updated Successfully'})

if __name__=='__main__':
    app.run(debug=True)