import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

server = Flask(__name__)

# Configure MongoDB connection URI
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"
mongo = PyMongo(server)

# Gridfs for storing and retrieving large files in MongoDB forfiles above 16MB (BSON doc): https://www.mongodb.com/docs/manual/core/gridfs/
# Initialize GridFS object using the MongoDB database from PyMongo
fs = gridfs.GridFS(mongo.db)

# Configuring RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

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
    