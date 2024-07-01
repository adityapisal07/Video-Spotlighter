import streamlit as st
from googleapiclient.discovery import build

# YouTube Data API setup
API_KEY = 'AIzaSyB3GphgEAi2Am39vSkzwAsGpGmvkRaRG3k'  # Replace with your own API key
youtube = build('youtube', 'v3', developerKey=API_KEY)

def fetch_youtube_videos(query):
    request = youtube.search().list(
        q=query,
        part='snippet',
        type='video',
        maxResults=3  # Limit to top 3 results
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

def fetch_related_videos(video_id):
    try:
        request = youtube.search().list(
            part='snippet',
            type='video',
            relatedToVideoId=video_id,
            maxResults=3  # Limit to top 3 related videos
        )
        response = request.execute()
        return response.get('items', [])
    except Exception as e:
        st.error(f"Error fetching related videos: {str(e)}")
        return []


# Streamlit UI
st.title('Video Spotlighter :)')

query = st.text_input('Enter your search query:',  placeholder='Search anything related to programming.....')
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
                    
                    # # Display related videos
                    # related_videos = fetch_related_videos(video_id)
                    # st.subheader('Related Videos:')
                    # for related_video in related_videos:
                    #     related_video_title = related_video['snippet']['title']
                    #     related_video_id = related_video['id']['videoId']
                    #     st.markdown(f"[{related_video_title}](https://www.youtube.com/watch?v={related_video_id})")
                    #     st.image(related_video['snippet']['thumbnails']['medium']['url'], width=320)
                else:
                    st.write('No details available.')
