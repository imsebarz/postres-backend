from flask import Flask, request, jsonify
from flask_pymongo import PyMongo, ObjectId
from flask_cors import CORS

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/postrespedrodb'
mongo = PyMongo(app)

@app.route("/postres", methods=["POST"])
def createPostre():
    id = mongo.db.postres.insert({
        "name": request.json["name"],
        "flavor": request.json["flavor"],
        "price": request.json["price"],
    })
    print(request.json)
    return jsonify(str(ObjectId(id)))


@app.route("/postres", methods=["GET"])
def getPostres():
    postres = []
    for document in mongo.db.postres.find():
        postres.append({
            '_id': str(ObjectId(document['_id'])),
            'name': document['name'],
            'price': document['price'],
            'flavor': document['flavor']
        })
    return jsonify(postres)


@app.route("/postres/<id>", methods=["DELETE"])
def deletePostre(id):
    mongo.db.postres.delete_one({
        '_id': ObjectId(id)
    })
    return 'deleted'


@app.route("/postre/<id>", methods=["GET"])
def getPostre(id):
    postre = mongo.db.postres.find_one({
        '_id': ObjectId(id)
    })
    return jsonify({
        '_id': str(ObjectId(postre['_id'])),
        'name': postre['name'],
        'price': postre['price'],
        'flavor': postre['flavor']
    })

@app.route("/postre/<id>", methods=["PUT"])
def updatePostre(id):
    print(id)
    mongo.db.postres.update_one({'_id': ObjectId(id)},{'$set':
    {
        'name': request.json['name'],
        'price': request.json['price'],
        'flavor': request.json['flavor']
    }})
    return 'updated'


if __name__ == '__main__':
    app.run(debug=True)