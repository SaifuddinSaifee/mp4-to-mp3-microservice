import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth_service import validate
from auth_service import access
from storage import util

server = Flask(__name__)

# Configure MongoDB connection URI
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"
mongo = PyMongo(server)

# Gridfs for storing and retrieving large files in MongoDB forfiles above 16MB (BSON doc): https://www.mongodb.com/docs/manual/core/gridfs/
# Initialize GridFS object using the MongoDB database from PyMongo
grid_fs = gridfs.GridFS(mongo.db)

# Configuring RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
rabbitmq_channel = connection.channel()

# Route to check access
@server.route("/login", method=["Post"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    
# Route to upload video
@server.route("/upload", method=["Post"])
def upload():
    access, err = validate.token(request)

    access = json.loads(access)

    # We need user to upload only one file
    if access["admin"] == True:
        if len(request.files) != 1:
            return "Please Upload one file only", 400

        # Upload to the gridfs mongodb
        for key, file in request.files.items():
            # Note: The upload function returns only on error; otherwise, it uploads data to MongoDB 
            err = util.upload(file, grid_fs, rabbitmq_channel, access)
            return "Something went wrong", 404 

        return "File uploaded Successfully", 200

    else:
        return "Unauthorized: You need admin access", 401
    
@server.route("/download", method=["GET"])
def download():
    pass


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)



