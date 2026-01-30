import os
import dotenv
import pandas as pd
from tqdm import tqdm
from google.cloud import vision
from google.api_core.client_options import ClientOptions

# --- 설정 (Configuration) ---
dotenv.load_dotenv()
GOOGLE_VISION_API_KEY = os.getenv("GOOGLE_VISION_API_KEY")

# 분석할 데이터와 썸네일 이미지가 있는 경로
INPUT_FILENAME = "kb_video_titles_raw.csv"
THUMBNAIL_DIR = "output/thumbnails"
OUTPUT_FILENAME = "ocr_analysis_results.csv"


def analyze_thumbnail_text(client, image_path: str) -> str:
    """Google Cloud Vision API를 사용하여 이미지에서 텍스트를 추출합니다."""
    try:
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        
        # 텍스트 감지 수행
        response = client.text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)

        if response.text_annotations:
            # 첫 번째 결과가 전체 인식 텍스트임
            full_text = response.text_annotations[0].description.replace('\n', ' ').strip()
            return full_text
        else:
            return None # 텍스트가 없는 경우 None 반환

    except FileNotFoundError:
        return "Error: Image file not found"
    except Exception as e:
        return f"Error: {e}"


def main():
    """메인 OCR 분석 파이프라인을 실행합니다."""
    # --- 사전 조건 확인 ---
    if not GOOGLE_VISION_API_KEY:
        print("❌ 오류: GOOGLE_VISION_API_KEY가 .env 파일에 설정되지 않았습니다.")
        return
    if not os.path.exists(INPUT_FILENAME):
        print(f"❌ 오류: '{INPUT_FILENAME}' 파일이 없습니다. 먼저 `fetch_video_data.py`를 실행하세요.")
        return
    if not os.path.exists(THUMBNAIL_DIR):
        print(f"❌ 오류: '{THUMBNAIL_DIR}' 폴더가 없습니다. 먼저 `download_thumbnails.py`를 실행하세요.")
        return

    # --- OCR 분석 시작 ---
    print("📝 썸네일 OCR 분석을 시작합니다...")

    # API 키를 사용하여 Vision API 클라이언트 초기화 (한 번만)
    client_options = ClientOptions(api_key=GOOGLE_VISION_API_KEY)
    client = vision.ImageAnnotatorClient(client_options=client_options)
    
    df = pd.read_csv(INPUT_FILENAME)
    ocr_results = []

    # tqdm을 사용하여 진행 상황 표시
    for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="OCR Processing"):
        video_id = row['video_id']
        image_path = os.path.join(THUMBNAIL_DIR, f"{video_id}.jpg")
        
        ocr_text = analyze_thumbnail_text(client, image_path)
        ocr_results.append({
            "video_id": video_id,
            "ocr_text": ocr_text
        })

    # 결과 데이터프레임 생성 및 저장
    df_results = pd.DataFrame(ocr_results)
    df_results.to_csv(OUTPUT_FILENAME, index=False, encoding='utf-8-sig')

    print(f"\n🎉 OCR 분석 완료! 결과가 '{OUTPUT_FILENAME}' 파일에 저장되었습니다.")
    print("\n--- 분석 결과 샘플 ---")
    print(df_results.head())
    print("--------------------")

if __name__ == "__main__":
    main()