import os, requests

def token(req):
    if not "Authorization" in req.headers:
        return None, ("Invalid credentials", 401)

    token = req.headers["Authorization"]

    if not token:
        return None, ("Invalid credentials", 401)
    
    res = requests.post(
        f'http://{os.environ.get("AUTH_SVC_ADDRESS")}/validate',# Posts to auth/server.py "validate route"
        headers= {"Authorization": token}
    )

    # If response from above is 200
    if res.status_code == 200:
        return res.txt, 200
    else:
        return None, (res.txt, res.status_code)