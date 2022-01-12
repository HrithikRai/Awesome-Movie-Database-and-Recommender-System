def amdb():
    import page1
    import page2
    import page3
    import page4
    import streamlit as st

    PAGES = {
        "Introduction to the Database": page1,
        "Explore the Dataset": page2,
        "Users Section": page3,
        "Get Recommendations": page4
    }

    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()


if __name__ == "__main__":
    amdb()
