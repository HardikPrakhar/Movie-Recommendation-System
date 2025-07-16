import pandas as pd
import numpy as np
import pickle as pk
from flask import Flask,render_template,request
import requests
import pickle

top_movies = pickle.load(open('top_movies.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
clone = pickle.load(open('clone.pkl','rb'))
similarities = pickle.load(open('similarities.pkl','rb'))
gen_similarities = pickle.load(open('gen_similarities.pkl','rb'))
gen_mov = pickle.load(open('gen_mov.pkl','rb'))



app = Flask(__name__)
@app.route('/')
def index():
    movie_names = list(top_movies['movie_title'].values)
    posters = list(top_movies['poster_url'].values)
    movies = list(zip(movie_names, posters))  
    return render_template('index.html', movies=movies)

def get_omdb_poster(title):
        api_key = '59a27e3d'
        url = f"http://www.omdbapi.com/?t={title}&apikey={api_key}"
        response = requests.get(url).json()
        return response.get("Poster", None)


@app.route('/')
def recommend_ui():
    return render_template('recommend_page.html')



@app.route('/recommend', methods=['POST'])



def recommend():
    name = request.form.get('name').strip().lower()
    #Content-based recommendation
    matched = gen_mov[gen_mov['movie_title'].str.lower().str.strip() == name]

    if matched.empty:
        return "Movie not found. Please check spelling and try again."

    movie_index = matched.index[0]
    distances = gen_similarities[movie_index]
    content_based = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:6]

    recommended_titles = set()
    recommendations = []

    print("Recommendations for you:")
    for i in content_based:
        title = gen_mov.iloc[i[0]].movie_title
        if title not in recommended_titles:
            recommended_titles.add(title)
            recommendations.append(title)

    print("\nYou may also like:")
    #Collaborative filtering
    normalized_index = pt.index.str.lower().str.strip()


    if name not in normalized_index.values:
        return "Movie not found in pivot table."


    real_name = pt.index[normalized_index == name][0]
    index = np.where(pt.index == real_name)[0][0]
    collab_based = sorted(list(enumerate(similarities[index])), key=lambda x: x[1], reverse=True)[1:]

    count = 0
    for i in collab_based:
        title = pt.index[i[0]]
        if title not in recommended_titles:
            recommended_titles.add(title)
            recommendations.append(title)
            count += 1
            if count == 5:
                break
    movdf = []
    for i in recommendations:
        movie_title = i
        overview = clone[clone['movie_title'] == i]['movie_info'].iloc[0]
        director = clone[clone['movie_title'] == i]['directors'].iloc[0]
        actors = clone[clone['movie_title'] == i]['actors'].iloc[0]
        poster = get_omdb_poster(movie_title)
        if poster is None:
            poster = "/static/no-poster-available.jpg"
        movdf.append({'movie_title':movie_title , 'overview' : overview , 'director' : director , 'actors' : actors , 'poster': poster})
    return render_template('recommend_page.html' , data = movdf)


if __name__ == '__main__':
    app.run(debug = True)




print("Hello world")