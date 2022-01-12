def app()   :
    
    import sqlalchemy
    import pandas as pd
    import streamlit as st
    from st_aggrid import AgGrid
    from st_aggrid.grid_options_builder import GridOptionsBuilder
    
    engine = sqlalchemy.create_engine('sqlite:///movielens.db', echo=True)
    
    movies_list = st.container()
    movies_search = st.container()
    movie_recommendation = st.container()
        
    with movies_list:
    
        st.title("List Of Available movies in the Database")
        sel_col,disp_col = st.columns(2)
        movies_list = pd.read_sql("SELECT title,genres FROM movies_data",con=engine)
        
        # add this
        gb = GridOptionsBuilder.from_dataframe(movies_list)
        gb.configure_pagination()
        gridOptions = gb.build()
        
        AgGrid(movies_list, gridOptions=gridOptions)
          
        
    with movies_search:
        st.header("Search a Movie in the Database")
        sel_col1,disp_col1 = st.columns(2)
        search = sel_col1.text_input("Please enter the movie name or a part of it")
        st.write(pd.read_sql("SELECT title,genres,avg_rating,num_ratings FROM avg_ratings where title like '%{}%'".format(search),con=engine))
    
    with movie_recommendation:
        st.header("Let me help you with some best rated movies")
        sel_col2,disp_col2 = st.columns(2)
        select_genre = sel_col2.selectbox("What kind of genre amuses you?",options=['Action','Adventure','Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical','Mystery','Romance','Sci-Fi','Thriller','War','Western'])
        st.text("Below is the list of top 10 best rated movies in the {} genre".format(select_genre))
        
        # Legacy Caching
        @st.experimental_memo
        def return_top10(genre):
            result = pd.read_sql("SELECT title,genres,avg_rating FROM avg_ratings where genres like '%{}%' order by lap_avg desc limit 10".format(genre),con=engine)
            return result
        res = return_top10(select_genre)
        st.write(res)