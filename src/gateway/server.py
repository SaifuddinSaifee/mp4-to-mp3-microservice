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

# Initialize GridFS object using the MongoDB database from PyMongo
grid_fs = gridfs.GridFS(mongo.db)

# Configuring RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
rabbitmq_channel = connection.channel()

# Route to check access
@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err, 401

# Route to upload video
@server.route("/upload", methods=["POST"])
def upload():
    access, err = validate.token(request)

    if err:
        return err, 401

    access = json.loads(access)

    # We need user to upload only one file
    if access.get("admin"):
        if len(request.files) != 1:
            return "Please upload one file only", 400

        # Upload to GridFS MongoDB
        for key, file in request.files.items():
            err = util.upload(file, grid_fs, rabbitmq_channel, access)
            if err:
                return "Something went wrong", 500

        return "File uploaded successfully", 200
    else:
        return "Unauthorized: You need admin access", 401

@server.route("/download", methods=["GET"])
def download():
    # Implement your download logic here
    pass

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)


