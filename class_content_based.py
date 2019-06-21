import numpy as np
from ast import literal_eval
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class ContentBasedRec:
    def __init__(self):
        self.movie_title = "default"
        self.movies = pd.read_csv('./mydata/metadata_clean_small.csv')
        print(self.movies)
        movie_credits = pd.read_csv('./mydata/credits_small_again.csv')
        keywords = pd.read_csv('./mydata/keywords_small.csv')
        overviews_and_ids = pd.read_csv('./mydata/movies_metadata_small.csv')
        self.movies['overview'], self.movies['id'] = overviews_and_ids['overview'], overviews_and_ids['id']
        def clean_ids(x):#in our data files there are a few invalid ids
            try:
                return int(x)
            except:
                return np.nan #to handle possible errors
        self.movies['id'] = self.movies['id'].apply(clean_ids)
        #filter out all the rows i=with a null ID so that they do not interfere 
        self.movies= self.movies[self.movies['id'].notnull()]
        #print(self.movies)
        self.movies['id'] = self.movies['id'].astype('int')
        movie_credits['id'] = movie_credits['id'].astype('int')
        keywords['id'] = keywords['id'].astype('int')
        self.movies = self.movies.merge(movie_credits, on='id')
        self.movies = self.movies.merge(keywords, on='id')
        
        features = ['cast', 'crew', 'keywords', 'genres']
        #print("MOVIES WITH CREDITS {0}".format(self.movies))

        for feature in features :
            self.movies[feature] = self.movies[feature].apply(literal_eval)
       
        # extract director 
        def director_extract(x):
            for crew_member in x:
                if crew_member['job'] == 'Director':
                    return crew_member['name']
            return np.nan    
        # extract producer
        
        def producer_extract(x):
            producer_names = []
            for crew_member in x:
                if crew_member['job'] == 'Producer':
                    producer_names.append(crew_member['name'])
            return producer_names  
        # extract executive prodcer
        def exec_prod_extract(x):
            exec_producer_names = []
            for crew_member in x:
                if crew_member['job'] == 'Executive Producer':
                     exec_producer_names.append(crew_member['name'])
            return exec_producer_names

        self.movies['director'] = self.movies['crew'].apply(director_extract)
        #print("DIRECTOR" + self.movies['director'].head())
        self.movies['producer'] = self.movies['crew'].apply(producer_extract)
        #print(self.movies['producer'].head())
        self.movies['executive producer'] = self.movies['crew'].apply(exec_prod_extract)
        #print(self.movies['executive producer'].head())

        def generate_list(x):
            if isinstance(x, list):
                names = [ele['name'] for ele in x]
                if len(names) > 4:
                    names = names[4:]
                return names
            return []

        self.movies['cast'] = self.movies['cast'].apply(generate_list)
        self.movies['keywords'] = self.movies['keywords'].apply(generate_list)
        self.movies['genres'] = self.movies['genres'].apply(lambda x: x[:4])
        #print(self.movies)

        def sanitize(x):
            if isinstance(x, list):
                return [str.lower(i.replace(" ", "")) for i in x]
            else:
                if isinstance(x, str):
                    return str.lower(x.replace(" ", ""))
                else:
                    return ''
        self.movies[['title', 'cast', 'director', 'producer', 'executive producer', 'keywords', 'genres']]
        for feature in ['cast', 'director', 'producer', 'executive producer', 'keywords', 'genres']:
            self.movies[feature] = self.movies[feature].apply(sanitize)
        def create_soup(x):
            return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + ' '.join(x['executive producer']) + ' ' 
            + x['director'] + ' ' + ' '.join(x['genres']) + ' ' +' '.join(x['producer']) 

        self.movies['soup'] = self.movies.apply(create_soup, axis=1)
        from sklearn.feature_extraction.text import CountVectorizer
        count = CountVectorizer(stop_words = 'english')
        count_matrix = count.fit_transform(self.movies['soup'])
        self.cosine_sim = cosine_similarity(count_matrix, count_matrix)
        self.movies = self.movies.reset_index()
        self.indicies = pd.Series(self.movies.index, index=self.movies['title'])
    def content_recommender(self):
    #obtain the index of the movie that matches the title 
        idx = self.indicies[self.movie_title]
        
        #get the pair wise similarity sscores of all movies with that movie 
        #and convert it into a list of tuples 
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        #sort the movies based on the cosine similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse = True)
        
        #get the score of the ten most similar movies. ignore the first movie
        sim_scores = sim_scores[1:11]
        
        #get the movie indicies
        movie_indicies = [i[0] for i in sim_scores]
        self.recommendations = self.movies['title'].iloc[movie_indicies]
        
        #return the top 10 most similar movies
        return 

#Crb = ContentBasedRec()
#Crb.movie_title = 'Shadows in Paradise'
#Crb.content_recommender()
