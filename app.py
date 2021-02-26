from flask import Flask,render_template,request, Blueprint
from flask.json import jsonify
from sqlalchemy import create_engine
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sqlite3
from flask_restx import Api, Resource, reqparse, fields

app = Flask(__name__)
# Database
engine = create_engine('sqlite:///resources/data.db')
#API Documentation
app = Flask(__name__)
api = Api(app, prefix='/api',version='1.0', title='Movie Recommendation - API Documenation',
    description='A simple API Documentation to retrieve machine learing info and data related to it',
    doc='/docs',
    base_url='/api'
) 
#Namespace
ns = api.namespace('Movies GET API', description='Find Content Based Recommended Movies')

@app.route('/home')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/model')
def model():
    return render_template('ml.html')





model = api.model('Movie Name', 
		  {'movie_name': fields.String(required = True, 
					 description="Name of the movie", 
					 help="Movie name cannot be blank.")})


@ns.route('/movie_titles')
class data(Resource):
    def get(self):
        connection = engine.connect()
        df = pd.read_sql("SELECT * FROM info",connection)
        records = df.title.to_list()
        return {"movie_titles":records}

@ns.route('/machinelearning/<string:movie_name>')
class Recommender(Resource):
    @api.doc(params={'movie_name': 'Enter the movie name'})
    def get(self, movie_name):
        connection = engine.connect()
        df = pd.read_sql("SELECT * FROM info",connection)
        features = ['keywords', 'cast', 'genres', 'director']

        for feature in features:
            df[feature] = df[feature].fillna('')
        def combined_features(row):
            return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
        df["combined_features"] = df.apply(combined_features, axis =1)
        cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"])
        # print("Count Matrix:", count_matrix.toarray())
        cosine_sim = cosine_similarity(count_matrix)
        records = df.to_json(orient='records')
        movie_user_likes = movie_name

        def get_index_from_title(title):
            value = df.index[df['title'] == title].tolist()
            return value[0]
        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index]))
    # similar_movies
        sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
    # sorted_similar_movies
        recommnedations = []
        def get_title_from_index(index):
            recommnedations.append(df[df.index == index]["title"].values[0])

        for movie in sorted_similar_movies:
            get_title_from_index(movie[0])
        # print(recommnedations[0:15])
        return {movie_name: recommnedations[1:15]}




@app.route('/data')
def data():
    connection = engine.connect()
    df = pd.read_sql("SELECT * FROM info",connection)
    records = df.to_json(orient='records')
    return records


@app.route('/ml_1',methods=["POST","GET"])
def ml_1():
    movie_name = request.form.get("text")
    connection = engine.connect()
    df = pd.read_sql("SELECT * FROM info",connection)
    features = ['keywords', 'cast', 'genres', 'director']

    for feature in features:
        df[feature] = df[feature].fillna('')
    def combined_features(row):
        return row['keywords']+" "+row['cast']+" "+row['genres']+" "+row['director']
    df["combined_features"] = df.apply(combined_features, axis =1)
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined_features"])
    # print("Count Matrix:", count_matrix.toarray())
    cosine_sim = cosine_similarity(count_matrix)
    records = df.to_json(orient='records')
    movie_user_likes = str(movie_name)

    def get_index_from_title(title):
        value = df.index[df['title'] == title].tolist()
        return value[0]
    movie_index = get_index_from_title(movie_user_likes)
    similar_movies = list(enumerate(cosine_sim[movie_index]))
# similar_movies
    sorted_similar_movies = sorted(similar_movies, key=lambda x:x[1], reverse=True)
# sorted_similar_movies
    recommnedations =[]
    def get_title_from_index(index):
        recommnedations.append(df[df.index == index]["title"].values[0])
    for movie in sorted_similar_movies:
        get_title_from_index(movie[0])
    # print(recommnedations[0:15])
    return jsonify(recommnedations[1:15])
# 
@app.route("/livesearch",methods=["POST","GET"])
def livesearch():
    searchbox = request.form.get("text")
    conn = sqlite3.connect('resources/data.db')
    cursor = conn.cursor()
    
    # con = sql.connect("DIMOP.db")
    # searchbox = "Batman"
    cursor.execute("""SELECT title FROM info WHERE title LIKE ?""", ('%'+searchbox+'%',))
    data = cursor.fetchall()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)