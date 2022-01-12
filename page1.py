def app():
    
    import streamlit as st
    
    project_info = st.container()
    dataset = st.container()
    dataset_info = st.container()
    
    
    
    with project_info:
        st.title("AMDB - Awesome Movie Database\nA Project by Hrithik Rai Saxena\nTo be submitted at the University of South Bohemia,Czech Republic")
        st.image("word_cloud.png")
        st.text("This is a word cloud generated from the user tags of this Database")
        st.header("Through this Project we attempt to create a Movie Database and Recommendation System.\n The user can:")
        st.text("* Search for a movie by its title or part and get similar recommendations")
        st.text("* View Top rated movies, Genre Wise")
        st.text("* Find users in the database with similar taste of movies")
        st.text("* Recommend movies to a given user from the database")
        st.text("* Get recommendations based on your choice of movies")
    
    
    
    with dataset:
        st.header("The Dataset used for this project:")
        st.text("MovieLens 25M movie ratings.\nHere we have 25 million ratings and one million tag applications applied to 62,000 movies by 162,000 users.")
        st.text("You can find the dataset at - https://grouplens.org/datasets/movielens/25m/")
        st.header("List of Genres:")
        st.text("Action,Adventure,Animation,Children's,Comedy,Crime,Documentary,Drama,Fantasy,\nFilm-Noir,Horror,Musical,Mystery,Romance,Sci-Fi,Thriller,War,Western")
       
    
    with dataset_info:
        st.header("Some interesting Facts about this Database")
        st.image("dataset_info.png")
        st.text("# There lives a guy on this planet, who has watched 32202 movies and rated them on the Movielens platform.")
        st.text("# The movie rated most has over 80k ratings and its Forrest Gump")
        st.text("The ratings are distributed as follows")
        st.image("ratings_dist.png")
        