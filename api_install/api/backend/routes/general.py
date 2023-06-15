from flask import Blueprint, request
from main import g, users, app 

@app.before_request
def before_request():
    g.user = users.authenticate(request.headers.get('Authorization'))
