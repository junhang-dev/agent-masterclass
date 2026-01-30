import pandas as pd
import asyncio
import aiohttp
import os
from tqdm.asyncio import tqdm

INPUT_FILENAME = "kb_video_titles_raw.csv"
OUTPUT_DIR = "output/thumbnails"

async def download_image(session, url, filepath):
    """지정된 URL에서 이미지를 비동기적으로 다운로드합니다."""
    try:
        async with session.get(url, timeout=30) as response:
            if response.status == 200:
                with open(filepath, 'wb') as f:
                    f.write(await response.read())
                return True
            else:
                return False
    except Exception:
        return False

async def main():
    """CSV 파일을 읽어 모든 썸네일을 다운로드하는 메인 함수."""
    if not os.path.exists(INPUT_FILENAME):
        print(f"❌ 오류: '{INPUT_FILENAME}' 파일이 없습니다. 먼저 `fetch_video_data.py`를 실행하세요.")
        return

    # 출력 폴더 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    df = pd.read_csv(INPUT_FILENAME)
    
    # 다운로드할 작업 목록 생성
    tasks = []
    async with aiohttp.ClientSession() as session:
        for index, row in df.iterrows():
            video_id = row['video_id']
            url = row['thumbnail_url']
            # 파일 확장자를 포함한 경로 생성 (기본 .jpg)
            filepath = os.path.join(OUTPUT_DIR, f"{video_id}.jpg")
            
            # 이미 파일이 존재하면 건너뛰기
            if not os.path.exists(filepath):
                tasks.append(download_image(session, url, filepath))
        
        if not tasks:
            print("✅ 모든 썸네일이 이미 다운로드되어 있습니다.")
            return

        print(f"🚀 총 {len(tasks)}개의 썸네일 다운로드를 시작합니다...")
        
        # tqdm을 사용하여 진행 상황 표시줄과 함께 비동기 작업 실행
        results = await tqdm.gather(*tasks)

        print(f"\n🎉 다운로드 완료! 성공: {results.count(True)}개, 실패: {results.count(False)}개")


if __name__ == "__main__":
    # Windows에서 asyncio 실행 시 필요한 이벤트 루프 정책 설정
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())