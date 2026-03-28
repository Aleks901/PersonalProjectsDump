from bs4 import BeautifulSoup
import requests
from queue import Queue
from urllib.parse import urljoin
import logging
logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(filename="Crawler.log", level=logging.INFO)
    start_url = "https://www.matprat.no/"
    crawl_queue = Queue()
    crawl_queue.put(start_url)
    logger.info(f"Initializing crawler with starting url: {start_url}")
    crawling = True
    logger.info("Crawler starting..")

    while crawling:
        next_url = crawl_queue.get()
        try: 
            response = requests.get(next_url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Error fetching {next_url}: {e}")
            continue

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        if next_url == None:
            print("Queue empty")
            crawling = False
        
        logger.info(f"Crawling Url: {next_url}")

        crawl_queue.put(next_url)

        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            full_url = urljoin(next_url, href)
            crawl_queue.put(full_url)

        try:
            recipe_name = soup.find('h1', class_='RecipeHeader_recipe-header__title__12vm2').get_text()
        except AttributeError:
            recipe_name = "Unknown Recipe"
        
        print("Recipe Name: ", recipe_name)
        logger.info(f"Extracted recipe: {recipe_name}")
        for ingredients in soup.find_all('ul', class_='RecipeIngredients_ingredients__list__02Pml'):
            print(ingredients.get_text())
            open("recipes.txt", "a").write(f"Recipe Name: {recipe_name}\n")
            open("recipes.txt", "a").write(f"Ingredients: {ingredients.get_text()}\n\n")
            logger.info(f"Extracted ingredients for {recipe_name}")
    

if __name__ == '__main__':
    main()