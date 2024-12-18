
from duckduckgo_search import DDGS
from datetime import datetime

ddgs = DDGS()

def search_web(topic, url_count=3):
    """
    Perform a web search for the given query using DuckDuckGo.
    Return the top results with title, link, and source.
    """
    print(f"Searching the web for: {topic}...")
    current_date = datetime.now().strftime("%Y-%m")
    results = ddgs.news(f"{topic} {current_date}", max_results=10)
    
    formatted_results = []
    for result in results:
        url = result.get("url", "No URL")
        # Skip msn.com results
        if "msn.com" in url.lower():
            continue

        formatted_results.append({
            "title": result.get("title", "No Title"),
            "href": url,
            "source": result.get("source", "Unknown Source"),
        })

        # Stop once we have the desired number of non-msn results
        if len(formatted_results) == url_count:
            break

    if not formatted_results:
        return f"Could not find news results for '{topic}' from allowed sources."

    return formatted_results
