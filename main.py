import pandas as pd
import numpy as np
import pickle as pk
from flask import Flask,render_template
import pickle

top_movies = pickle.load(open('top_movies.pkl','rb'))

app = Flask(__name__)
@app.route('/')


def index():
    movie_names = list(top_movies['movie_title'].values)
    posters = list(top_movies['poster_url'].values)
    movies = list(zip(movie_names, posters))  
    return render_template('index.html', movies=movies)

if __name__ == '__main__':
    app.run(debug = True)




print("Hello world")