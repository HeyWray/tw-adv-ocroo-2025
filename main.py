import streamlit as st
import requests
import pyperclip as clip


#Streamlit docs
#https://docs.streamlit.io/

#streamlit sessions for showing the gallery or video player
if 'show_gallery' not in st.session_state:
    st.session_state["show_gallery"] = True

#copy to clipboard (customisation button)
if 'copy_text' not in st.session_state:
    st.session_state["copy_text"] = False

#Pages
def gallery():
    """
    Starting home page for the website
    return null
    """

    set_config("Home")
    session = requests.Session()

    st.header("Videos", anchor="Center")

    col1, col2, col3 = st.columns([1,1,1])
    cols = [col1, col2, col3]
    next_col = 0

    #get a list of videos
    videos = fetch(session, '/video')

    #counter = 1 #debugging variable for testing duplicate videos
    #create a series of buttons in columns for each video
    for vid in videos['videos']:
        with cols[next_col]:
            #create a button with the video title, description,
            #and then on clicking it will pass the video path
            #to video_player()
            st.button(f"{vid.get('id')}\n\n{vid.get('description')}",
                      width="stretch", on_click=set_video, args={vid.get('id')})
            #debug testing
            # st.button(f"{vid.get('id')} - {counter}\n\n{vid.get('description')}",
            #           width="stretch", on_click=set_video, args={vid.get('id')})

            #controls which video
            next_col += 1
            if next_col == 3: next_col = 0
            #counter += 1

def video_player(vid: str):
    """
    The primary video player page. Pass the video path that will be played with.
    return null
    """

    set_gallery(False)

    set_config(f"{vid} - Video")
    session = requests.Session()

    video_path = fetch(session, f"video/path/{vid}")

    if 'video_text' not in st.session_state:
        st.session_state["video_text"] = ""

    #Split the page into 2
    col1, col2 = st.columns([1,1], )

    with col1:
        #Header, Home button, & Video player
        h1, h2 = st.columns([1,5])
        with h1:
            st.button("All videos", width="stretch",
                      on_click=set_gallery, args={True})
        with h2:
            st.header(f"{vid}", anchor="Center")
        st.video(video_path)

    with col2:
        txtcol1, txtcol2 = st.columns([1,1])

        #Input time to get text
        with txtcol1:
            #Grab text button & text output
            time = st.text_input("Input time you want to get",placeholder="In seconds e.g. 128", width="stretch", max_chars=6, on_change=set_video_text, args={})

            #validate
            if time.isnumeric():
                #remove any float
                time = int(time)
                #remove negatives
                if time < 0 : time = 0
                #set text
                st.session_state["video_text"] = fetch(session, f"video/{vid}/frame/{time}/ocr")
                #copy to clipboard if set up
                if st.session_state["copy_text"]:
                    clip.copy(st.session_state["video_text"])

        #Customisation, automatically copy text to clipboard
        with txtcol2:
            if st.checkbox("Automatically copy text to clipboard", width="stretch"):
                st.session_state["copy_text"] = True
            else:
                st.session_state["copy_text"] = False

        with st.container(border=True, height="stretch"):
            if st.session_state["video_text"] == {}:
                st.session_state["video_text"] = "No text available"
            st.write(st.session_state["video_text"])

 
#session setting
def set_gallery(state: bool):
    """Sets the gallery state to switch back and forth between video player and gallery"""
    st.session_state["show_gallery"] = state
    #print("variable gallery")

def set_video(vid: str):
    st.session_state["video"] = vid
    set_gallery(False)
    #print("variable video")

def set_video_text():
    session = requests.Session()
    #print("variable text")

#functions
def fetch(session, url):
    """
    Gets the API methods (from simple_api)
    returns json"""
    try:
        result = session.get("http://localhost:8000/" + url)
        return result.json()
    except Exception:
        return {}

def _session_write():
    """
    Output the session for debug information
    """
    session = requests.Session()
    st.write(session)

def set_config(title: str):
    """
    Sets basic information for the page, pass what the tab title will be
    return null
    """
    # Sets the page configuration to be wide
    st.set_page_config(
        page_title=f"{title}",
        page_icon="📽",
        layout="wide",
        initial_sidebar_state="collapsed",
        menu_items={}
    )


if __name__ == '__main__':
    if st.session_state["show_gallery"]:
        gallery()
    else:
        video_player(st.session_state["video"])