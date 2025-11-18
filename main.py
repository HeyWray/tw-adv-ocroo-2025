import streamlit as st
import requests


#Set the page configuration to be wide
st.set_page_config(
    page_title="Video",
    page_icon="📽️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

def fetch(session, url):
    try:
        result = session.get("http://localhost:8000/" + url)
        return result.json()
    except Exception:
        return {}

def video_player():
    session = requests.Session()

    thing = fetch(session, "video")
    #Split the page into 2
    col1, col2 = st.columns([2,1])

    with col1:
        #Header, Home button, & Video player
        h1, h2 = st.columns([1,6])
        with h1:
            st.button("More videos", width="stretch")
        with h2:
            st.header(f"Welcome to Video Player - Home Page {thing}", anchor="Center", width="stretch")
        st.video("./resources/oop.mp4")
    with col2:
        #Grab text button & text output
        st.button("Get Text", width="stretch")
        st.text_area(
            "video area", value="", height="stretch", max_chars=None, key=None, help=None, on_change=None, args=None, kwargs=None,
            placeholder="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            disabled=False, label_visibility="hidden", width="stretch")

if __name__ == '__main__':
    video_player()