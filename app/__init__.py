from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'YOU NEVER GUESS'
from app import views

