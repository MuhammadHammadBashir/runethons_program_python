from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import urllib.parse

class WebExpert:
    def __init__(self):
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("--headless")  # Run Firefox in headless mode (no GUI)
        
        # Automatically install and manage GeckoDriver
        self.service = Service("/snap/bin/geckodriver")
        self.driver = webdriver.Firefox(service=self.service, options=self.options)

    def get_pdf_links(self, queries, max_results=5):
        base_url = "https://scholar.google.com/scholar?q="
        pdf_filter = " filetype:pdf"
        pdf_links = {}

        for query in queries:
            print(f"Searching for: {query}")
            encoded_query = urllib.parse.quote(query + pdf_filter)
            search_url = f"{base_url}{encoded_query}"
            self.driver.get(search_url)
            time.sleep(3)  # Allow page to load
            
            links = self.driver.find_elements(By.TAG_NAME, "a")
            pdf_urls = [link.get_attribute("href") for link in links if link.get_attribute("href") and link.get_attribute("href").endswith(".pdf")]
            pdf_links[query] = list(set(pdf_urls))[:max_results]  # Remove duplicates and limit results
        
        return pdf_links  # DO NOT quit the driver here!

    def get_page_html(self, url):
        print(f"Visiting the page: {url}")
        self.driver.get(url)
        time.sleep(2)  # Allow page to load

        # Get the full HTML content of the page
        return self.driver.page_source  # DO NOT quit the driver here!

    def close(self):
        """ Gracefully close the WebDriver instance. """
        if self.driver:
            self.driver.quit()
            print("Web driver closed.")

# # Example list of queries
# queries = [
#     "tennis biomechanics injury prevention", 
#     "tennis serve biomechanics pose estimation", 
#     "lower limb biomechanics tennis", 
#     "tennis agility training injury risk", 
#     "core stability tennis performance", 
#     "tennis video analysis motion capture", 
#     "biomechanical analysis tennis serve return", 
#     "injury risk assessment tennis pose estimation", 
#     "tennis performance analysis amateur level", 
#     "effects of prior injuries on tennis biomechanics"
# ]

# # Create instance
# web_expert = WebExpert()

# # Get PDF links
# pdf_links = web_expert.get_pdf_links(queries)

# html_results = []
# for query, links in pdf_links.items():
#     for link in links:
#         result = web_expert.get_page_html(link)
#         html_results.append(result)
#         print(f" - {link}")

# # Close the driver after all operations
# web_expert.close()
