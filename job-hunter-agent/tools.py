import os
import re
import logging
from crewai.tools import tool
from firecrawl import FirecrawlApp # Junhang님 버전에 맞는 FirecrawlApp 사용

@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for information using a self-hosted Firecrawl server.
    Args:
        query (str): The query to search the web for.
    Returns:
        A formatted string of search results with cleaned website content.
    """
    try:
        # API 키 대신, 직접 구축한 EC2 서버의 주소를 사용합니다.
        app = FirecrawlApp(api_url="http://3.26.233.253:3002")
        
        # CrewAI 에이전트가 이해할 수 있도록 문자열로 가공하여 반환합니다.
        # .search()가 반환하는 객체에서 .data 속성으로 결과 리스트에 접근합니다.
        search_results = app.search(query=query, limit=3) # limit은 필요에 따라 조절
        
        if not search_results or not search_results.data:
            return "No results found."

        content_parts = []
        for result in search_results.data:
            title = result.get("title", "No Title")
            markdown = result.get("markdown", "No content available.")
            
            # Markdown 내용 정리 (선택 사항)
            if markdown:
                cleaned = re.sub(r'\s+', ' ', markdown).strip()
            else:
                cleaned = "No content available."

            content_parts.append(f"Title: {title}\nContent:\n{cleaned}\n---")
        
        return "\n\n".join(content_parts)

    except Exception as e:
        logging.error(f"Error using Firecrawl search tool for query '{query}': {e}")
        return f"Error during web search: {e}"