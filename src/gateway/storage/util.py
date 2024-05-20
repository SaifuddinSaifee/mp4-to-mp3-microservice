import pika, json

# this module is messed up, test again

def upload(file, grid_fs, rabbitmq_channel, access):
    """
    This function uploads a file to MongoDB using GridFS and then sends a message to RabbitMQ
    for asynchronous processing by a downstream service.
    """

    try:
        file_id = grid_fs.put(file)
    except Exception as err:
        return "Something went wrong, file not uploaded", 500
    
    # If the upload is successful
    message = {
        "video_file_id": str(file_id),
        "audio_file_id": None, # Set this space to mp3's file id
        "username": access["username"]

    }

    try:
        rabbitmq_channel.basic_publish(
            exchange="",
        )
    except:
        return None
