
import newspaper
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_article(url):
    """
    Extracts the article from the given URL using newspaper3k as the primary method 
    and Selenium as a fallback for dynamic content.
    """
    response = {
        "status": "",
        "title": None,
        "authors": [],
        "publish_date": None,
        "text": None,
        "error": None
    }
    
    # First attempt: Use the standard newspaper3k method
    try:
        article = newspaper.article(url)
        article.download()
        article.parse()
        
        if article.text.strip():
            response["status"] = "Article extracted using the standard method."
            response["title"] = article.title
            response["authors"] = article.authors
            response["publish_date"] = article.publish_date.strftime("%Y-%m-%d") if article.publish_date else None
            response["text"] = article.text
            return response
        else:
            response["status"] = "Standard method failed. Falling back to Selenium..."
            raise ValueError("Empty article text.")
    
    except Exception as e:
        response["error"] = f"Standard method exception: {e}"
        response["status"] = "Falling back to Selenium..."

    # Second attempt: Use Selenium to load dynamic content
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)

        driver.get(url)
        html = driver.page_source
        driver.quit()

        # Use newspaper4k to parse the article from the rendered HTML
        article = newspaper.article(url)

        article.set_html(html)
        article.parse()

        if article.text.strip():
            response["status"] = "Article extracted using Selenium."
            response["title"] = article.title
            response["authors"] = article.authors
            response["publish_date"] = article.publish_date.strftime("%Y-%m-%d") if article.publish_date else None
            response["text"] = article.text
            return response
        else:
            raise ValueError("Empty article text even after using Selenium.")
    
    except Exception as e:
        response["error"] = f"Selenium method exception: {e}"
        response["status"] = "Failed to extract article content using both methods."
        return response

