from bs4 import BeautifulSoup
import requests
from queue import Queue
from urllib.parse import urljoin
import logging
from rich.console import Console
from rich.table import Table
logger = logging.getLogger(__name__)

console = Console();
table = Table(title="Crawler Status")

found_recipes = Table(title="Scraped Recipes")
found_recipes.add_column("Scraped", style="cyan")
found_recipes.add_column("Status", style="green")

def main():
    logging.basicConfig(filename="Crawler.log", level=logging.INFO)
    start_url = "https://www.matprat.no/"
    crawl_queue = Queue()
    crawl_queue.put(start_url)
    logger.info(f"Initializing crawler with starting url: {start_url}")
    crawling = True
    table.add_column("Task", style="cyan")
    table.add_column("Status", style="green")
    table.add_row("Crawler Initialized", "✅ Done")
    table.add_row("Crawler", "⏳ Running")
    console.print(table)



    while crawling:
        extracted_recipes = 0
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
            logger.info(f"Extracted recipe: {recipe_name}")
            print("Recipe found: ", recipe_name)
            found_recipes.add_row(f"{recipe_name}", "✅ Extracted")
        except AttributeError:
            recipe_name = "Unknown Recipe"
            logger.error("Invalid url, moving on..")
        
        for ingredients in soup.find_all('ul', class_='RecipeIngredients_ingredients__list__02Pml'):
            open("recipes.txt", "a").write(f"Recipe Name: {recipe_name}\n")
            open("recipes.txt", "a").write(f"Ingredients: {ingredients.get_text()}\n\n")
            logger.info(f"Extracted ingredients for {recipe_name}")
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Crawler stopped!")
        console.print(found_recipes)
        print("Extracted recipes saved to recipes.txt")
