import os
import re
import logging
from crewai.tools import tool
from firecrawl import FirecrawlApp

@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for information using Firecrawl's v2 API.
    Args:
        query (str): The query to search the web for.
    Returns:
        A list of search results with cleaned website content in Markdown format.
    """
    try:
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

        # The library now calls the v2 endpoint automatically.
        # We just need to handle the new response format.
        response = app.search(
            query=query,
            limit=5,
            scrape_options={"formats": ["markdown"]}
        )

        cleaned_chunks = []

        # **KEY CHANGE**: The data is now in response['data']['web'] for v2
        if 'data' in response and 'web' in response['data']:
            for result in response['data']['web']:
                # Safely get data using .get() to avoid errors if a key is missing
                title = result.get("title", "No Title Available")
                url = result.get("url", "")
                markdown = result.get("markdown", "")

                if markdown:
                    # Clean the markdown content
                    cleaned = re.sub(r'\s+', ' ', markdown).strip()
                    cleaned = re.sub(r'\[[^\]]+\]\([^\)]+\)|https?://[^\s]+', '', cleaned)
                else:
                    cleaned = "No content available."

                cleaned_result = {
                    "title": title,
                    "url": url,
                    "markdown": cleaned,
                }
                cleaned_chunks.append(cleaned_result)
        
        return cleaned_chunks

    except Exception as e:
        logging.error(f"Error using Firecrawl search tool for query '{query}': {e}")
        return f"Error during web search: {e}"
