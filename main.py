import pandas as pd
import numpy as np
import pickle as pk
from flask import Flask,render_template
import pickle

top_movies = pickle.load(open('top_movies.pkl','rb'))

app = Flask(__name__)
@app.route('/')


def index():
    return render_template('index.html', movie_name = list(top_movies['movie_title'].values) , poster = list(top_movies['poster_url'].values))

if __name__ == '__main__':
    app.run(debug = True)



print("Hello world")