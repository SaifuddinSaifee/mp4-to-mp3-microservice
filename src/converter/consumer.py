import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import convert_to_mp3

def main():
    # Connect to MongoDB instance running on Minikube internal host
    client = MongoClient("host.minikube.internal", 27017)
    db_Videos = client.videos  # Database for storing video files
    db_mp3 = client.mp3s       # Database for storing MP3 files

    # Create GridFS instances for video and MP3 databases
    fs_Videos = gridfs.GridFS(db_Videos)
    fs_mp3s = gridfs.GridFS(db_mp3)

    # Establish a connection to RabbitMQ server
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")  # RabbitMQ service name
    )
    rabbitmq_channel = connection.channel()  # Create a channel on the connection

    # Define callback function to process messages from RabbitMQ
    def callback(rabbitmq_channel, method, properties, body):
        # Convert video to MP3 and store the result in MongoDB GridFS
        err = convert_to_mp3.start(body, fs_Videos, fs_mp3s, rabbitmq_channel)

        # Acknowledge or reject the message based on conversion result
        if err:
            rabbitmq_channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            rabbitmq_channel.basic_ack(delivery_tag=method.delivery_tag)

    # Set up consumption of messages from the queue defined by VIDEO_QUEUE environment variable
    rabbitmq_channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback
    )

    # Print status message and start consuming messages from RabbitMQ
    print("Waiting for messages. To exit press CTRL + C")
    rabbitmq_channel.start_consuming()

# Entry point of the script
if __name__ == "__main__":
    try:
        main()  # Run the main function
    except KeyboardInterrupt:
        print("Interrupted")  # Handle keyboard interrupt gracefully
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
