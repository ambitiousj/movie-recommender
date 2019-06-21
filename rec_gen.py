
# coding: utf-8

# In[1]:


import pandas as pd
#import matplotlib.pyplot as plt
import sklearn.metrics as metrics
import numpy as np
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import correlation
from sklearn.metrics.pairwise import pairwise_distances
#from contextlib import contextmanager
#import warnings
#warnings.filterwarnings('ignore')
import numpy as np



class RecsEngine:

    def __init__(self):
        self.metric = 'cosine'
        self.k = 10
        self.currentuserid = 0
        self.recommended_titles = []
        self.watch_again_titles = []

        ###########  INITIALISATION OF DATA ##########################

        '''u_cols = ['user_id', 'age', 'sex', 'occupation', 'zip_code']
        self.users = pd.read_csv('./mydata/u.user', sep='|', names=u_cols,encoding='latin-1')

        #Reading ratings file:
        r_cols = ['user_id', 'movie_id', 'movie_rating', 'unix_timestamp']
        self.ratings = pd.read_csv('./mydata/u.data', sep='\t', names=r_cols,encoding='latin-1')

        #Reading items file:
        m_cols = ['movie_id', 'movie_title' ,'release_date','video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
        'Animation', 'Children\'s', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy',
        'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        self.movies = pd.read_csv('./mydata/u.item', sep='|', names=m_cols, encoding='latin-1')

        self.movies['release_date'] = pd.to_datetime(self.movies['release_date'], errors = 'coerce')
        # extract the year from the datetime 
        self.movies['year'] = self.movies['release_date'].apply(lambda x: str(x).split('-')[0] if x != np.nan else np.nan)
        self.movies = self.movies.drop('release_date', axis = 1)
        self.movies = self.movies.drop('video release date', axis = 1)
        self.movies = self.movies.drop('IMDb URL', axis = 1)
        
        self.movies.shape

        def clean_int(x):
            try:
                return int(x)
            except:
                return np.nan

        self.ratings = self.ratings.drop(["unix_timestamp"], axis = 1)
        self.users = self.users.drop(["zip_code"], axis = 1)

        self.movies['year'] = self.movies['year'].apply(clean_int)

        self.movies = self.movies[self.movies['year'].notnull()]

        self.movies['year'] = self.movies['year'].astype(int)'''
    
        usersfile = open('./mydata/u.user2.csv', 'r')
        self.users = pd.read_csv(usersfile)
        usersfile.close()
        #self.users = pd.read_csv('./mydata/u.user2.csv')
        ratingsfile = open('./mydata/u.data2.csv', 'r')
        self.ratings = pd.read_csv(ratingsfile)
        ratingsfile.close()
        #self.ratings = pd.read_csv('./mydata/u.data2.csv')
        
        print(self.ratings.columns)
        self.movies = pd.read_csv('./mydata/u.item2.csv')

        n_users = self.users.shape[0]
        n_movies = self.movies.shape[0]
       

        #check if all ratings have valid movie ids
        ratingsnew = self.ratings[self.ratings.movie_id.isin(self.movies.movie_id)]

        #ratings.shape

        #sparsity=1.0-len(ratings)/float(n_users*n_movies)

        #ratings.movie_rating.unique()

        ratings_explicit = self.ratings[self.ratings.movie_rating != 0]
        ratings_implicit = self.ratings[np.isnan(self.ratings.movie_rating)]

        # create a rataings matrix from the data we have now

        self.ratings_matrix = ratings_explicit.pivot(index='user_id', columns='movie_id', values='movie_rating')
        movie_id = self.ratings_matrix.columns

        n_users = self.ratings_matrix.shape[0]
        n_movies = self.ratings_matrix.shape[1]
        #print(n_users, n_movies)

        #NaNs cannont be used within the algorithm so must change to zeros 
        self.ratings_matrix.fillna(0, inplace = True)
        self.ratings_matrix = self.ratings_matrix.astype(np.int32)
        #setting the data type to an integer

        expl_u_ratings = self.users[self.users.user_id.isin(ratings_explicit.user_id)]
        impl_u_ratings = self.users[self.users.user_id.isin(ratings_implicit.user_id)]

        #return ratings_matrix,movies,users,ratings

    ################USER ID CHECK################################
    def check_if_user_exists(self,userid):
        useridlist = self.ratings_matrix.index
        if userid in useridlist:
            self.currentuserid = userid
            return True
        else:
            return False
   
        
        
        
    #############SAVE TO FILE#############

    def sign_out(self):

        #usersfile = open('./mydata/u.user2.csv', 'w')
        self.users.to_csv('./mydata/u.user2.csv', index=False)
        #self.users.to_csv(usersfile, index=False)
        #usersfile.close()
        self.ratings.to_csv('./mydata/u.data2.csv', index=False)
        
        return True

    ####### FIND K NEAREST NEIGHBOUR (USER) ##########
        

    # User based Recommendation engine 
    # this function will find 'k' similar users given the user id and the ratings martrix provided 
    def findkuser(self, user_id):
        similarities=[]
        indicies=[]
        model_KNn = NearestNeighbors(metric = self.metric, algorithm = 'brute')  # kNearestNeighbour, using the metric previously set
        # and brute force search
        model_KNn.fit(self.ratings_matrix)
        loc = self.ratings_matrix.index.get_loc(user_id)
        distances, indices = model_KNn.kneighbors(self.ratings_matrix.iloc[loc, :].values.reshape(1, -1), n_neighbors = self.k+1)
        similarities = 1-distances.flatten()
        print('{0} most similar users for User {1}:\n'.format(self.k,user_id))
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i]+1 == user_id:
                continue;

            else:
                print('{0}: User {1}, with similarity of {2}'.format(i, indices.flatten()[i]+1, similarities.flatten()[i]))
                
        return similarities,indices
        

    #similarities,indices = findkuser(24,ratings_matrix, metric='cosine')

    ############## PREDICT USER-BASED FUNCTION #################


    #This function predicts rating for specified user-item combination based on user-based approach
    def predict_userbased(self, user_id, item_id):
        prediction=0
        user_loc = self.ratings_matrix.index.get_loc(user_id)
        item_loc = self.ratings_matrix.columns.get_loc(item_id)##change names of variables etc
        similarities, indices=self.findkuser(user_id) #similar users based on cosine similarity
        mean_rating = self.ratings_matrix.iloc[user_loc,:].mean() #to adjust for zero based indexing
        sum_wt = np.sum(similarities)-1
        product=1
        wtd_sum = 0 
        
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i] == user_loc:
                continue;
            else: 
                ratings_diff = self.ratings_matrix.iloc[indices.flatten()[i],item_loc]-np.mean(self.ratings_matrix.iloc[indices.flatten()[i],:])
                product = ratings_diff * (similarities[i])
                wtd_sum = wtd_sum + product
        
        #in case of very sparse datasets, using correlation metric for collaborative based approach may give negative ratings
        #which are handled here as below
        if prediction <= 0:
            prediction = 1   
        elif prediction >5:
            prediction = 5
        
        prediction = int(round(mean_rating + (wtd_sum/sum_wt)))
        print ('\nPredicted rating for user {0} of movie {1} is {2}'.format(user_id,item_id,prediction))

        return prediction

    
    
        
     

    ######### FIND K NEAREST NEIGHBOR (ITEM) ##########
    def FindKnnItems(self, item_id):
        similarities = []
        indicies = []
        ratings_matrix_t = self.ratings_matrix.T
        item_loc = ratings_matrix_t.index.get_loc(item_id)
        model_knn = NearestNeighbors(metric = self.metric, algorithm = 'brute')
        model_knn.fit(ratings_matrix_t)
        distances, indices = model_knn.kneighbors(ratings_matrix_t.iloc[item_loc, :].values.reshape(1, -1), n_neighbors = self.k+1)
        similarities = 1-distances.flatten()
        print ('{0} most similar items for item {1}:\n'.format(self.k,item_id))
        for i in range(0, len(indices.flatten())):
            if indices.flatten()[i]+1 == item_id:
                continue;

            else:
                print ('{0}: Item {1} :, with similarity of {2}'.format(i,indices.flatten()[i]+1, similarities.flatten()[i]))

        return similarities,indices

    ########## ITEM - BASED PREDICTIONN FUNCTION ###########
    def predict_itembased(self, user_id, item_id):
        prediction = wtd_sum = 0
        user_loc = self.ratings_matrix.index.get_loc(user_id)
        item_loc = self.ratings_matrix.T.index.get_loc(item_id)
        similarites, indices = self.FindKnnItems(item_id)
        sum_wt = np.sum(similarites)-1
        product = 1
        for i in range (0, len(indices.flatten())):
            if indices.flatten()[i] == item_loc:
                continue;
            else:
                product = self.ratings_matrix.iloc[user_loc,indices.flatten()[i]] * (similarites[i])
                wtd_sum = wtd_sum + product
        prediction = int(round(wtd_sum/sum_wt))
        
        #in the case of a highly sparse data set:
        if prediction <= 0:
            prediction = 1
        if prediction >5:
            prediction = 5
        print ('\nPredicted rating for user {0} for movie {1}: {2}'.format(user_id,item_id,prediction))
        return prediction
 
    

    ###### ADD A NEW USER TO THE  DATAFRAME ##########

    def add_new_user(self,userage, userocc, gender, movietitle, rating):
        users_t = self.users.T
        print("your user id is now: {0}".format(self.users.shape[0] +1))
        userid = self.users.shape[0] +1
        rownum = userid - 1
        users_t[rownum]= [userid,userage, gender, userocc]
        self.users = users_t.T
        self.currentuserid = userid
        self.ratings, self.ratings_matrix = self.update_ratings(movietitle, rating)#put self infront of a class function when calling it  
        
    def add_new_rating(self,movietitle,rating):
        self.ratings, self.ratings_matrix = self.update_ratings(movietitle, rating)#put self infront of a class function when calling it  
    
                
    ########## ADD A NEW RATING TO THE DAWTA FRAME #############

    def update_ratings(self, movietitle, rating):
        updatedratings = False
        updatedmatrix = False
         
        DictOfMovies = { i+1 : self.movies.movie_title[i] for i in range(0, len(self.movies.index) ) }
        listofmovies = pd.Series(DictOfMovies)
        movie_name = []
        movie_num = []
        for (key, value) in DictOfMovies.items():
            movie_name.append(value)
            movie_num.append(key)
        movie_idx = movie_name.index(movietitle)
        movie_id = movie_num[movie_idx]
        int(movie_id)
        ratings_t = self.ratings.T
            
        ratings_t[self.ratings.shape[0]] = [self.currentuserid, movie_id, rating]
        ratingsnew = ratings_t.T
        
        if ratingsnew.shape[0] == self.ratings.shape[0] + 1:
            ratingsnew =ratingsnew.drop_duplicates(subset=['user_id','movie_id'], keep='last', inplace=False)
            new_matrix = ratingsnew.pivot(index='user_id', columns='movie_id', values='movie_rating')
            new_matrix.fillna(0, inplace = True)
            new_matrix = new_matrix.astype(np.int32)
        
        return ratingsnew, new_matrix


   ######### RECOMMENDATION FUNCTION WHICH HOLDS ALL THE RECOMMENDATION FUNCTIONS #####

    def recommend(self,user_id,algorithm):
            
        predict = []
        movie = []
        prediction_cos = {}
        prediction_cor = {}
        watch_again = []
        tempMatrix = self.ratings_matrix
        print("algorithm :" + algorithm)
        some_values = user_id
        
        if (algorithm == 'similar_users'):
            print("these are what some similar users to you picked ")
            correlation = False
            cosine = False
            tempMatrix = tempMatrix.loc[tempMatrix.index == (some_values)]
            ratingsDict = {i+1: tempMatrix.values[0, i] for i in range(0, len(tempMatrix.columns))}
            #print (ratingsDict)
            for (key, value) in ratingsDict.items():
                predict.append(value)
                movie.append(key)
            while(correlation == False):
                self.metric = 'correlation'
                j = 0
                while(j<len(predict) ):
    #remeber to change back to  j<len(predict) aftr testing. i reduced the size to speed up calculation
                    if (predict[j] < 5):                            
                        prediction_cor[movie[j]]=(self.predict_userbased(user_id, movie[j]))
                                                  
                        j = j + 1
                    else:                    
                        prediction_cor = {movie[j]:(-1)} #for already rated items
                        watch_again.append(movie[j])
                        j = j + 1
                print(prediction_cor)
                correlation = True

            while(cosine == False):
                self.metric = 'cosine'
                j = 0
                while(j<len(predict)):
                    if (predict[j] < 5):                            
                        prediction_cos[movie[j]]=(self.predict_userbased(user_id, movie[j]))
                        j = j+1
                    else:                    
                        prediction_cos = {movie[j]:(-1)} #for already rated items
                        
                        j = j + 1
                print(prediction_cor)
                cosine = True                    
        
        elif (algorithm == 'similar_items'):
            print("these are some similar movies to which you like")
            correlation = False
            cosine = False
            tempMatrix = tempMatrix.loc[tempMatrix.index == (some_values)]
            print(tempMatrix)
            ratingsDict = {i+1: tempMatrix.values[0, i] for i in range(0, len(tempMatrix.columns))}
            #print (ratingsDict)
            for (key, value) in ratingsDict.items():
                predict.append(value)
                movie.append(key)
            while(correlation == False):
                self.metric = 'correlation'
                j = 0
                while(j<len(predict)):
                    if (predict[j] < 5):                            
                        prediction_cor[movie[j]]=(self.predict_itembased(user_id, movie[j]))
                                                  
                        j = j + 1
                    else:                    
                        prediction_cor = {movie[j]:(-1)} #for already rated items
                        watch_again.append(movie[j])
                        j = j + 1
                print(prediction_cor)
                correlation = True                
            while(cosine == False):
                self.metric = 'cosine'
                j = 0
                while(j<len(predict)):
                    if (predict[j] < 5):                            
                        prediction_cos[movie[j]]=(self.predict_itembased(user_id, movie[j]))
                        j = j+1
                    else:                    
                        prediction_cos = {movie[j]:(-1)} #for already rated items
                        
                        j = j + 1
                print(prediction_cos)
                cosine = True     
  
                           
            
         
        
        
        prediction_cos = pd.Series(prediction_cos)
        print(prediction_cos)
        print(len(prediction_cos))
        prediction_cor = pd.Series(prediction_cor)
        print(prediction_cor)
        print(len(prediction_cor))

        prediction = prediction_cos.combine(prediction_cor, max)
        prediction = prediction.sort_values(ascending=False)
        recommended = prediction[:10]
        watch_again = watch_again[:5]
        
        print("Size of recommended list is {0}".format(len(recommended)))
        print("Size of watch again list is {0}".format(len(watch_again)))
        if len(recommended)> 0:
            for i in range(len(recommended)):
                print("RECOMMENDED => " + self.movies.movie_title[recommended.index[i]])
                self.recommended_titles.append(self.movies.movie_title[recommended.index[i]])
        if len(watch_again) > 0:   
            for x in range(len(watch_again)):
                print("WATCH AGAIN => " + self.movies.movie_title[watch_again[x]])
                self.watch_again_titles.append(self.movies.movie_title[watch_again[x]])

            
        print("Recommendations generation completed.")
        return()        



#tratings.to_csv('../mydata/testing123.csv', index=False)
#tusers.to_csv('../mydata/testingusers.csv', index=False)

