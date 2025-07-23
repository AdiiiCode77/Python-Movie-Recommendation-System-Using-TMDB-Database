from flask import Flask, render_template, request
from recommender import recommend_movies_with_posters
import pandas as pd

app = Flask(__name__)
movies = pd.read_csv('movies.csv')
print("Columns in CSV:", pd.read_csv('movies.csv').columns.tolist())

@app.route('/', methods=['GET', 'POST'])
def index():
    recommendations = []
    selected_movie = ''
    if request.method == 'POST':
        selected_movie = request.form['movie']
        recommendations = recommend_movies_with_posters(selected_movie)
    return render_template('index.html', movies=movies['title'].tolist(), recommendations=recommendations, selected_movie=selected_movie)

if __name__ == '__main__':
    app.run(debug=True)
