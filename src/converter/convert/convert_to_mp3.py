import os, json, tempfile, pika
from bson.objectid import ObjectId
import moviepy.editor


def start(message, fs_Videos, fs_mp3s, rabbitmq_channel):
    # Parse the incoming message from JSON format
    message = json.loads(message)

    # Create a temporary file to store the video data
    temp_file = tempfile.NamedTemporaryFile()

    # Retrieve the video file from MongoDB GridFS using the provided file ID
    out = fs_Videos.get(ObjectId(message["video_file_id"]))

    # Write the video file data to the temporary file
    temp_file.write(out.read())

    # Extract audio from the video file using moviepy
    audio = moviepy.editor.VideoFileClip(temp_file.name).audio
    temp_file.close()

    # Define the path for the temporary MP3 file
    temp_file_path = tempfile.gettempdir() + f"/{message['video_file_id']}.mp3"
    audio.write_audiofile(temp_file_path)

    # Read the MP3 file data and store it in MongoDB GridFS
    with open(temp_file_path, "rb") as file:
        data = file.read()
        file_id = fs_mp3s.put(data)

    # Remove the temporary MP3 file
    os.remove(temp_file_path)

    # Add the audio file ID to the message
    message["audio_file_id"] = str(file_id)

    try:
        # Publish the updated message to the MP3_QUEUE in RabbitMQ
        rabbitmq_channel.basic_publish(
            exchange="",
            routing_key=os.environ.get("MP3_QUEUE"),
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE  # Ensure messages are persisted in the queue
            ),
        )
    except Exception as err:
        # If publishing fails, delete the MP3 file from MongoDB GridFS
        fs_mp3s.delete(file_id)
        return "Failed to publish message"
