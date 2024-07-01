import streamlit as st
import pyrebase
from googleapiclient.discovery import build
import webbrowser
# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyAwTzHS3ae7wINBULOJG4DXII0raLqykQ0",
    'authDomain': "video-spotlighter.firebaseapp.com",
    'projectId': "video-spotlighter",
    'storageBucket': "video-spotlighter.appspot.com",
    'messagingSenderId': "955927624427",
    'appId': "1:955927624427:web:ae603bce4eedaefae41cae",
    'measurementId': "G-KRCWDXQ4PR",
    'databaseURL': ""
}

# link
link = "t.ly/uo1We"

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# YouTube Data API setup
API_KEY = 'AIzaSyBk1MWV7Rw83SjNsfe72XeotvOWOeJEc9w'  # Replace with your own API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_youtube_videos(query):
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=3
    )
    response = request.execute()
    return response.get('items', [])

def fetch_video_details(video_id):
    request = youtube.videos().list(
        part='snippet,statistics',
        id=video_id
    )
    response = request.execute()
    return response['items'][0] if response['items'] else None

def main_page():
    st.title('Video Spotlighter :)')

    query = st.text_input('Enter your search query:', placeholder='Search anything related to programming.....')
    if st.button('Search'):
        if query:
            videos = fetch_youtube_videos(query)
            st.subheader(f'Top 3 Videos for "{query}":')
            for index, video in enumerate(videos):
                video_title = video['snippet']['title']
                video_id = video['id']['videoId']
                video_details = fetch_video_details(video_id)

                # Display video thumbnail and title
                st.image(video['snippet']['thumbnails']['medium']['url'], width=320)
                st.write(f"**Title:** {video_title}")
                st.write(f"**Views:** {video_details['statistics']['viewCount'] if video_details else 'N/A'}")

                # Create expander to show more details on click
                with st.expander(f"View {video_title}"):
                    if video_details:
                        channel_name = video_details['snippet']['channelTitle']
                        publish_date = video_details['snippet']['publishedAt']
                        description = video_details['snippet']['description']

                        st.write(f"**Channel:** {channel_name}")
                        st.write(f"**Published at:** {publish_date}")
                        st.write(f"**Description:** {description}")

                        # Embed video player
                        st.video(f"https://www.youtube.com/watch?v={video_id}")
                    else:
                        st.write('No details available.')
        else:
            st.error("Please enter your search query.")

def login_page():
    st.title("Welcome to Video Spotlighter :)")

    # Choice for Login or Sign Up
    choice = st.selectbox("Login/Signup", ["Login", "Signup"])

    email = st.text_input('Enter your email:')
    password = st.text_input('Enter your password:', type='password')

    if choice == "Signup":
        if st.button("Create Account"):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("Account created successfully!")
                st.experimental_set_query_params(loggedIn="true")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Failed to create account: {e}")

    elif choice == "Login":
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.success("Logged in successfully!")
                st.experimental_set_query_params(loggedIn="true")
                webbrowser.open(link)
                
            except Exception as e:
                error_json = e.args[1]
                error = eval(error_json)['error']['message']
                if error == "EMAIL_NOT_FOUND" or error == "INVALID_PASSWORD":
                    st.error("Invalid login details. Please check your email and password and try again.")
                else:
                    st.error(f"Failed to login: {error}")

# Main logic
query_params = st.experimental_get_query_params()
if query_params.get("loggedIn") == ["true"]:
    main_page()
else:
    login_page()
