import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Function to crawl a given URL and index its content
def crawl(start_url):
    base_domain = urlparse(start_url).netloc
    visited_urls = set()
    index = {}

    def crawl_page(url):
        if url in visited_urls:
            return

        try:
            response = requests.get(url)
            
            # Check for HTTP errors
            if response.status_code != 200:
                print(f"Skipping {url}: HTTP {response.status_code}")
                return
        
            # Process only HTML responses
            if "text/html" not in response.headers.get("Content-Type", ""):
                print(f"Skipping {url}: Non-HTML content")
                return
            
            soup = BeautifulSoup(response.text, "html.parser")
            visited_urls.add(url)

            # Extract and index text content
            index_page(url, soup.get_text())

            # Follow links on the same domain
            for link in soup.find_all("a", href=True):
                next_url = urljoin(url, link['href'])

                # Ensure the link is on the same domain
                if urlparse(next_url).netloc == base_domain:
                    crawl_page(next_url)

        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")

    # Function to index the words from a page
    def index_page(url, text):
        words = text.split()
        for word in words:
            word = word.lower()
            if word not in index:
                index[word] = []
            if url not in index[word]:
                index[word].append(url)

    # Function to search for a query in the indexed data
    def search(query):
        query = [word.lower() for word in query]
        result_urls = None

        for word in query:
            if word in index:
                if result_urls is None:
                    result_urls = set(index[word])
                else:
                    result_urls &= set(index[word])
            else:
                # If any word is not in the index, return no results
                return []

        return list(result_urls) if result_urls else []

    # Start crawling from the start_url
    crawl_page(start_url)

    # Print the generated index (for debugging purposes)
    print("Index:")
    for word, urls in index.items():
        print(f"{word}: {urls}")

    # Test the search function
    while True:
        query = input("Enter search terms (comma-separated, or 'quit' to exit): ").strip()
        if query.lower() == 'quit':
            break
        words = query.split(",")
        results = search(words)
        print("Results:")
        for result in results:
            print(result)

# Start URL for testing
start_url = "https://vm009.rz.uos.de/crawl/index.html"

# Start crawling
crawl(start_url)
