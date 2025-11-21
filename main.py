import streamlit as st
import requests

#Streamlit docs
#https://docs.streamlit.io/

def fetch(session, url):
    try:
        result = session.get("http://localhost:8000/" + url)
        return result.json()
    except Exception:
        return {}

def video_player(vid: str):
    # Set the page configuration to be wide
    st.set_page_config(
        page_title=f"{vid} - Video",
        page_icon="📽️",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={}
    )
    session = requests.Session()

    #thing = fetch(session, "video")

    video_path = fetch(session, f"video/path/{vid}")
    #video_bytes = open(video_path, "rb").read()

    video_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

    #Split the page into 2
    col1, col2 = st.columns([1,1], )

    with col1:
        #Header, Home button, & Video player
        h1, h2 = st.columns([1,5])
        with h1:
            st.button("All videos", width="stretch", icon="🏠")
        with h2:
            st.header(f"{vid}", anchor="Center")
        video = st.video(video_path)
        #playback = fetch(session, f"video/playback/{vid}")
        #print(f"\nResult is:\n{playback}")
    with col2:
        #Grab text button & text output
        clicked = st.button("Get Text", width="stretch", on_click=session_write)
        with st.container(border=True, height="stretch"):
            st.write(video_text)


def session_write():
    session = requests.Session()
    st.write(session)

if __name__ == '__main__':
    video_player("demo")