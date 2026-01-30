import os
from firecrawl import FirecrawlApp
from openai import OpenAI
from dotenv import load_dotenv
from pprint import pprint

# --- 설정 ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
FIRECRAWL_SERVER_URL = "http://3.26.233.253:3002"
TOPIC = "2025년 코쿤센터 직구 최신 정보"
# --- 설정 끝 ---

def main():
    """주제에 대해 검색, 스크랩, 요약을 수행하는 메인 함수"""

    if not OPENAI_API_KEY:
        print("오류: .env 파일에 OPENAI_API_KEY를 설정해주세요.")
        return

    try:
        firecrawl_app = FirecrawlApp(api_url=FIRECRAWL_SERVER_URL)
        openai_client = OpenAI(api_key=OPENAI_API_KEY)

        # 1. SEARCH: 여러 개의 후보 URL을 찾기 위해 limit을 늘림
        print(f"🔍 '{TOPIC}'에 대한 검색을 시작합니다 (후보 5개 탐색)...")
        search_results = firecrawl_app.search(query=TOPIC, limit=5)

        if not search_results or not search_results.data:
            print("검색 결과가 없습니다.")
            return

        # 2. SCRAPE: 성공할 때까지 순서대로 시도
        scraped_data = None
        for result in search_results.data:
            target_url = result['url']
            print(f"\n📄 '{target_url}' 페이지 스크랩 시도...")
            try:
                # 타임아웃, 프록시 등 고급 옵션 적용
                scraped_data_object = firecrawl_app.scrape_url(
                    url=target_url,
                    timeout=120000,
                    proxy='stealth'
                )
                
                if scraped_data_object and scraped_data_object.markdown:
                    print(f"✅ 스크랩 성공! (콘텐츠 길이: {len(scraped_data_object.markdown)}자)")
                    scraped_data = scraped_data_object # 성공한 데이터 저장
                    break # 성공했으므로 루프 탈출
                else:
                    print("🔸 콘텐츠가 없어 다음 URL로 넘어갑니다.")

            except Exception as e:
                print(f"❌ 스크랩 실패: {e}. 다음 URL로 넘어갑니다.")
                continue # 실패 시 다음 URL로 계속 진행

        # 3. SUMMARIZE: 스크랩에 최종 성공한 경우에만 요약 진행
        if scraped_data:
            print("\n🧠 AI가 스크랩된 내용을 요약합니다...")
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant who summarizes web content in clear, concise Korean."},
                    {"role": "user", "content": f"다음은 '{TOPIC}'에 대한 웹페이지 내용입니다. 이 내용을 바탕으로 사람들이 궁금해할 만한 핵심 정보를 정리해서 알려주세요:\n\n---\n{scraped_data.markdown}"}
                ]
            )
            summary = response.choices[0].message.content
            
            print("\n--- [ AI 최종 요약 결과 ] ---")
            print(summary)
            print("--------------------------")
        else:
            print("\n🚨 모든 후보 URL을 스크랩하는 데 실패했습니다.")

    except Exception as e:
        print(f"\n프로세스 중 심각한 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    main()