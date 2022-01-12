def app():
    
    import sqlalchemy
    import pandas as pd
    import streamlit as st
    import pickle
    
    engine = sqlalchemy.create_engine('sqlite:///movielens.db', echo=True)
    
    user_cluster = st.container()
    user_recommend = st.container()
    
    genre_cluster_data = pd.DataFrame(pickle.load(open("fav_genre_usergrps.pkl", 'rb')))
    user_data = pd.DataFrame(pickle.load(open("movies_favGenre_data.pkl", 'rb')))
    movies_data = pd.DataFrame(pickle.load(open("movies_data.pkl", 'rb')))
    ratings_data = pd.DataFrame(pickle.load(open("ratings.pkl", 'rb')))
    
    def get_users(selected_genre_list):
            try:
                i = genre_cluster_data[genre_cluster_data.fav_genre=='{}'.format(selected_genre_list)].index[0]
                return genre_cluster_data.genre_cluster[i]
            except:
                return "Sorry no users found who like these combination of Genres"
    
    with user_cluster:
        try:
            st.header("Find users with the same movie taste")
            sel_col1,disp_col1 = st.columns(2)
            selected_genre_list = sel_col1.multiselect("Please select genre(You can also select multiple genres)",
                                                       options=['Action','Adventure','Animation','Children','Comedy','Crime','Documentary',
                                                                'Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi',
                                                                'Thriller','War','Western'])
            
            selected_genre_list = " ".join(sorted(selected_genre_list)).replace(" ",",")
            same_taste_users = get_users(selected_genre_list)
            st.write("Total {} users loves this Genre. You can also add more genres in the above dropdown to get a particular set of users.".format(len(same_taste_users)))
              
            users_selected = sel_col1.multiselect("Pick Users from the below dropdown to see the common movies these users have watched and how they rated them",
                                                       options=same_taste_users)
            
            def find_common_movies(users):
                    movies = []
                    for i in users:
                        ind = user_data[user_data.userId==i].index[0]
                        movies.append(user_data.movies[ind])
                    common_movies = list(set.intersection(*map(set, movies)))
                    return common_movies
          
                
            def get_user_rating(title,userid):
                try:
                    z = movies_data[movies_data.title==title].index[0]
                    movie_id = movies_data.movieId[z]
                    rating = ratings_data.rating[ratings_data.rating[(ratings_data.userId==userid) & (ratings_data.movieId==movie_id)].index[0]]
                    return rating
                except:
                    return 0
             
            if st.button("Find the common movies watched by these users") == True:
                try:
                    com_movies=find_common_movies(users_selected)
                    common = pd.DataFrame(com_movies,columns=['common movies'])
                    for j in com_movies:    
                        for i in users_selected:
                            common["{}".format(i)] = get_user_rating(j,i)
                    st.write(common)
                           
                except:
                    st.write("No common movies were watched by these users")
                    
                    
            #st.text("The average rating given by these users on this list of common movies is as follows:")     
            #st.write(pd.DataFrame(users_selected,avg_ratings_common,columns=['userID','avg_rating']))
            if st.button("View Users who like the above combination of genres?") == True:
                st.write(pd.DataFrame(same_taste_users,columns=['UserID']))
        except:
            st.text("Please select Genre")
             
    with user_recommend:
        st.header("Let's Recommend some awesome movies to the given User!")
        sel_col1,disp_col1 = st.columns(2)
        reco_user = sel_col1.selectbox("Select the user whom you would like to recommend a movie",options=list(user_data.userId))
        reco_user_genre = user_data.fav_genre[user_data.fav_genre[user_data.userId==reco_user].index[0]]
        st.text("The favourite genre of user {} is {}".format(reco_user,reco_user_genre))
        movies_watched = user_data.movies[user_data.movies[user_data.userId==reco_user].index[0]]
        top_rated_df = pd.read_sql("SELECT title,genres FROM avg_ratings where genres like '%{}%' order by lap_avg desc limit 40".format(reco_user_genre.replace(",","|")),con=engine)
        top_rated_df_list = list(top_rated_df.title)
        list3 = set(movies_watched)&set(top_rated_df_list)
        recommended_movies = sorted(list3, key = lambda k : movies_watched.index(k))
        if st.button("Recommend") == True:
            st.write("These are the best rated movies of the user's favourite genre that isn't watched yet")
            st.write(pd.DataFrame(recommended_movies,columns=['Recommended Movies']))
