import os
import dotenv
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# .env 파일에서 환경 변수 로드
dotenv.load_dotenv()

# 환경 변수에서 API 키 가져오기
API_KEY = os.getenv("YOUTUBE_API_KEY")
# KB국민은행 부동산 채널 ID
CHANNEL_ID = "UCHmXGmj6JA-4iQ1UFMC7LYw"
# 저장할 파일 이름
OUTPUT_FILENAME = "kb_video_titles_raw.csv"

def get_all_video_data(api_key, channel_id):
    """지정된 YouTube 채널의 모든 영상 ID, 제목, 썸네일 URL을 가져옵니다."""
    if not api_key:
        print("❌ 오류: YouTube API 키가 .env 파일에 설정되지 않았습니다.")
        return None

    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        request = youtube.channels().list(part="contentDetails", id=channel_id)
        response = request.execute()
        
        if not response.get("items"):
            print(f"❌ 오류: 채널 ID '{channel_id}'를 찾을 수 없습니다.")
            return None
            
        playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        
        videos = []
        next_page_token = None
        
        print(f"📡 '{channel_id}' 채널의 영상 정보 수집을 시작합니다...")
        while True:
            request = youtube.playlistItems().list(
                part="snippet",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()
            
            for item in response["items"]:
                snippet = item["snippet"]
                video_id = snippet["resourceId"]["videoId"]
                title = snippet["title"]
                # 고화질 썸네일이 없을 경우 기본 썸네일을 사용
                thumbnail_url = snippet["thumbnails"].get("high", snippet["thumbnails"].get("default", {})).get("url")

                if thumbnail_url:
                    videos.append({
                        "video_id": video_id,
                        "title": title,
                        "thumbnail_url": thumbnail_url
                    })

            next_page_token = response.get("nextPageToken")
            if not next_page_token:
                break
        
        return videos

    except HttpError as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return None
    except Exception as e:
        print(f"알 수 없는 오류가 발생했습니다: {e}")
        return None

if __name__ == "__main__":
    if os.path.exists(OUTPUT_FILENAME):
        print(f"✅ 파일 '{OUTPUT_FILENAME}'이 이미 존재합니다. API 호출을 건너뜁니다.")
    else:
        video_data = get_all_video_data(API_KEY, CHANNEL_ID)
        if video_data:
            df = pd.DataFrame(video_data)
            df.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')
            print(f"\n🎉 총 {len(video_data)}개의 영상 정보를 '{OUTPUT_FILENAME}' 파일로 저장했습니다.")
        else:
            print("\n❌ 영상 정보를 가져오는 데 실패했습니다.")
