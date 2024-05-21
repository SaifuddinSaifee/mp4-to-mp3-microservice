import pika, json

import pika.spec

# this module is messed up, test again

def upload(file, grid_fs, rabbitmq_channel, access):
    """
    This function uploads a file to MongoDB using GridFS and then sends a message to RabbitMQ
    for asynchronous processing by a downstream service.
    """

    try:
        file_id = grid_fs.put(file)
    except Exception as err:
        return f"Something went wrong, file not uploaded: \nE: {err}", 500
    
    # If the file upload is successful
    message = {
        "video_file_id": str(file_id),
        "audio_file_id": None, # Set this space to mp3's file id
        "username": access["username"]

    }

    try:
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key = "video", # Later create a queue called "video" in the rabbitmq management panel http://rabbitmq-manager.com/#/queues
            body = json.dumps(message), # Convert pythhon to json
            properties = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE # To make sure the msgs are persisted in the queue in case pod crashes
            ),
        )
    except:
        # If the queuing fails then remove the file from the db
        grid_fs.delete(file_id)
        return "Internal server Error", 500
