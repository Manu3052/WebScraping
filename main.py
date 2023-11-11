from dataclasses import dataclass

import pandas as pd
import requests
from bs4 import BeautifulSoup


@dataclass
class WebPage:
    """
    This class is responsible for reading and retrieving all the products found in an e-commerce page.
    """

    base_url = "https://www.amazon.com.br/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
    }
    products_link = []
    products = []

    def get_request(self, url: str):
        """
        This method is responsible for making requests for the url given

        Attributes:
            url (str): Receives a string that represents a url from a page
        """
        request = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(request.content, "lxml")
        return soup

    def get_request_from_all_pages(self):
        """
        This method is responsible for making requests and using beautifulsoup to transform these requests in html.
        """
        url = f"https://www.amazon.com.br/s?k=lola+cosmetics&crid=3388UCEFGMOSB&sprefix=%2Caps%2C690&ref=nb_sb_ss_sx-trend-t-ps-d-purchases-ten-ca_5_0"
        request = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(request.content, "lxml")
        amount_pages = int(
            soup.find("span", class_="s-pagination-item s-pagination-disabled").string
        )
        for item in range(0, amount_pages):
            url = f"https://www.amazon.com.br/s?k=lola+cosmetics&page={item}&crid=3388UCEFGMOSB&sprefix=%2Caps%2C690&ref=nb_sb_ss_sx-trend-t-ps-d-purchases-ten-ca_5_0"
            request = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(request.content, "lxml")
            self.get_products_individual_links(soup)

    def get_products_individual_links(self, soup):
        """
        Method responsible for getting all the products individual links and saving in an attribute which is a list products_link
        """
        products = soup.find_all(
            "a",
            class_="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal",
        )
        for item in products:
            product_link = item.get("href")
            self.products_link.append(product_link)

    def get_products_info(self):
        """
        Method responsible for retrieving the information of individual products the camps used are: name, price, rate, amount of reviews

        """
        for individual_link in self.products_link:
            product_url = self.base_url + individual_link
            soup = self.get_request(url=product_url)
            product_name = soup.find(
                "h1",
                id="title",
            )
            if product_name is not None:
                product_name = product_name.text.strip()
                product_price = soup.find("span", class_="a-offscreen").string.strip()
                try:
                    product_rate = soup.find("span", class_="a-icon-alt").string.strip()
                except:
                    product_rate = "No rating"
                try:
                    reviews_amount = soup.find(
                        "span", id="acrCustomerReviewText"
                    ).string.strip()
                except:
                    reviews_amount = "no one review it"
                product = {
                    "Nome do Produto": product_name,
                    "Preço": product_price,
                    "Rate": product_rate,
                    "Quantidade de reviews": reviews_amount,
                }
                self.products.append(product)
                print(f"Saving {product_name}")

    def transform_excel(self):
        """
        This method is responsible for creating or overwriting an already existing xlsx
        """
        df = pd.DataFrame(self.products)
        df.to_excel("utils\products.xlsx", sheet_name="Produtos")


def main():
    web_page = WebPage()
    web_page.get_request_from_all_pages()
    web_page.get_products_info()
    web_page.transform_excel()


# Calling the def main() method
main()
