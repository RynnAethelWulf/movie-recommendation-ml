<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.imgur.com/6wj0hh6.jpg" alt="Project logo"></a>
</p>

<h3 align="center">Building a Movie Recommendation Engine in Python using Scikit-Learn </h3>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![GitHub Issues](https://img.shields.io/github/issues/kylelobo/The-Documentation-Compendium.svg)](https://github.com/bimalkprabha/movie-recommendation-ml/issues)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)


</div>

---

<p align="center">  Wondered how Google comes up with movies that are similar to the ones you like? This project is based on Machine Learning and Content based recommendation based on user input movies with asssitance of sickit learn.
  
</p>

## 📝 Table of Contents

- [About](#about)
- [Getting Started](#getting_started)
- [Acknowledgments](#acknowledgement)


## 🧐 About <a name = "about"></a>

Content based recommendation <br>
This type of recommendation systems, takes in a movie that a user currently likes as input. Then it analyzes the contents (storyline, genre, cast, director etc.) of the movie to find out other movies which have similar content. Then it ranks similar movies according to their similarity scores and recommends the most relevant movies to the user.



## 🏁 Getting Started <a name = "getting_started"></a>
- Import the required packages

```
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```
- Choose the features to be used for the model. We do not need to use all the features. Some of them are not appropriate for this model. I choose these four features:
```
features = ['keywords','cast','genres','director']
```

-Fit and transform the data into the ‘count vectorizer’ function that prepares the data for the vector representation. When you pass the text data through the ‘count vectorizer’ function, it returns a matrix of the number count of each word.Use ‘cosine_similarity’ to find the similarity. This is a dynamic way of finding the similarity that measures the cosine angle between two vectors in a multi-dimensional space.
```
cv = CountVectorizer()
        count_matrix = cv.fit_transform(df["combined_features"])
        # print("Count Matrix:", count_matrix.toarray())
        cosine_sim = cosine_similarity(count_matrix)
```
- Sort the list ‘similar_movies’ by the coefficients 

```
        for movie in sorted_similar_movies:
            get_title_from_index(movie[0])
        # print(recommnedations[0:15])
        return {movie_name: recommnedations[1:15]}
```

## Webiste Link - https://movie-recommendation-v-2.herokuapp.com/  
P.S Loading of the site might take some time due to low computing power of free tier heroku.


## 🎉 Acknowledgements <a name = "acknowledgement"></a>
- UWA Data Science
</div>
