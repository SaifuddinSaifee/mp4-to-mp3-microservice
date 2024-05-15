import jwt, datetime, os, json
from flask import Flask, request
from flask_mysqldb import MySQL
from dotenv import load_dotenv

server = Flask(__name__)
mysql = MySQL(server)

# config
# Load the .env file
load_dotenv()
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_Password"] = os.environ.get("MYSQL_Password")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# Authentication
@server.route("/login", methods=["POST"])
def login():
    """
    A function that handles the login route. It checks the user's credentials and returns a JWT token if valid.
    """
    auth = request.authorization
    if not auth or not auth.email or not auth.password:
        return "missing credentials", 401
    
    # check if user exists with email and password in the auth db (users table)
    cur = mysql.connection.cursor()

    # check if user exists with email and password in the auth db (users table)
    result = cur.execute("SELECT * FROM users WHERE email = %s", (auth.email,))

    if result > 0:
        user_data = cur.fetchone()
        if user_data[2] == auth.password: # check if supplied password matches the one in the auth db
            return createJWT(user_data[1], os.environ.get("JWT_SECRET"), True) # Create JWT Token
        return "invalid credentials", 401

# Create JWT Token
def createJWT(username, secret, authz):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.now() + datetime.timedelta(days=1), # Expire the token after 1 day
            "iat": datetime.datetime.now(), # Issued at time
            'admin': authz
        },
        secret,
        algorithm="HS256"
    )


@server.route("/validate", methods=["POST"])
def validate():
    encoded_jwt = request.headers["Authorization"]

    # Check for JWT token in the header
    if not encoded_jwt:
        return "Missing Credentials", 401
    
    type, encoded_jwt = encoded_jwt.split(" ")

# only for Bearer Token has access to token's associated resources
    if type == "Bearer":
        try:
            # Decode and verify the JWT
            decoded = jwt.decode(
                encoded_jwt, os.environ.get("JWT_SECRET"), algorithms=["HS256"]
            )
        except: return "Unauthorized", 403

        return decoded, 200






if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5000, debug=True)



