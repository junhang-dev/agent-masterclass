import os
from firecrawl import FirecrawlApp
from pprint import pprint

# Junhang님의 EC2 서버 주소
FIRECRAWL_SERVER_URL = "http://3.26.233.253:3002"

def test_firecrawl_server():
    """Firecrawl 서버의 주요 기능들을 테스트합니다."""
    
    print(f"Firecrawl 서버({FIRECRAWL_SERVER_URL})에 연결을 시도합니다...")
    app = FirecrawlApp(api_url=FIRECRAWL_SERVER_URL)
    
    # 1. Scrape 기능 테스트
    print("\n--- 1. Scrape 기능 테스트 시작 ---")
    try:
        # [수정 1] 메소드 이름을 scrape_url 로 변경
        scraped_data = app.scrape_url(url='https://blog.google/technology/ai/')
        print("Scrape 성공! 일부 내용:")
        # 결과 객체에서 markdown 속성을 직접 접근
        if scraped_data and hasattr(scraped_data, 'markdown'):
            pprint(scraped_data.markdown[:200] + "...")
        else:
            pprint(scraped_data)
    except Exception as e:
        print(f"Scrape 실패: {e}")

    # 2. Search 기능 테스트
    print("\n--- 2. Search 기능 테스트 시작 ---")
    try:
        search_results = app.search(query="Google Gemini latest updates")
        # [수정 2] search_results 객체 내부의 .data 리스트의 길이를 확인
        print("Search 성공! 결과 개수:", len(search_results.data))
        if search_results.data:
            # 결과 객체에서 .data 리스트에 접근하여 첫 번째 항목의 제목을 출력
            pprint(search_results.data[0]['title'])
    except Exception as e:
        print(f"Search 실패: {e}")


if __name__ == "__main__":
    test_firecrawl_server()