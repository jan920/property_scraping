
# website: https://www.rightmove.co.uk/property-for-sale/Glasgow


import requests
import csv
from bs4 import BeautifulSoup


class PropertyWebsiteScraper:
    def __init__(self, url_start, url_continuing, url_min_bed, url_ending, listing_scraper, price_scraper, bedrooms_scraper, address_scraper, link_scraper):
        self.url_start = url_start
        self.url_continuing = url_continuing
        self.url_min_bed = url_min_bed
        self.url_ending = url_ending
        self.listing_scraper = listing_scraper
        self.price_scraper = price_scraper
        self.bedrooms_scraper = bedrooms_scraper
        self.address_scraper = address_scraper
        self.link_scraper = link_scraper

    def return_url(self, min_bedrooms, page_number):
        url = self.url_start + self.url_continuing + self.url_min_bed + str(min_bedrooms)\
              + self.url_ending + str(page_number)
        return url

    def return_soup(self, url):
        res = requests.get(url)
        res.raise_for_status()
        content = res.text
        soup = BeautifulSoup(content, "html.parser")
        return soup

    def find_suitable_listings(self, min_bedrooms, price_per_bedroom, num_to_check):
        count = 0
        page = 0
        listings = []
        while count < num_to_check:
            url = self.return_url(min_bedrooms, page)
            soup = self.return_soup(url)
            for listing in soup.find_all(self.listing_scraper[0], class_=self.listing_scraper[1]):
                price = self.return_price(listing)
                print(price)
                bedrooms = self.return_bedrooms(listing)
                print(bedrooms)
                address = self.return_address(listing)
                print(address)
                link = self.return_link(listing)
                print(link)
                if bedrooms and price:
                    condition2 = price/bedrooms < price_per_bedroom
                    condition3 = bedrooms >= min_bedrooms
                    if condition2 and condition3:
                        listings.append([price, bedrooms, address, link])
                count += 1
            page += 1
        return listings

    def find_price(self, listing):
        price = listing.find(self.price_scraper[0], class_=self.price_scraper[1])
        return price.text

    def return_price(self, listing):
        price_string = self.find_price(listing)
        price_string = price_string.split()[0]
        price_string = price_string.strip('£ ')
        price_string = price_string.replace(',', '')
        if price_string.isdigit():
            return int(price_string)
        else:
            return False

    def find_bedrooms(self, listing):
        bedrooms = listing.find(self.bedrooms_scraper[0], class_=self.bedrooms_scraper[1])
        return bedrooms.text

    def return_bedrooms(self, listing):
        bedrooms_string = self.find_bedrooms(listing)
        return_bed = bedrooms_string.split()[0]
        if return_bed.isdigit():
            return int(return_bed)
        else:
            return False

    def find_address(self, listing):
        address = listing.find(self.address_scraper[0], class_=self.address_scraper[1])
        return address.text

    def return_address(self, listing):
        address_string = self.find_address(listing)
        return " ".join(address_string.split())

    def find_link(self, listing):
        link = listing.find(self.link_scraper[0], class_=self.link_scraper[1])
        return link

    def return_link(self, listing):
        link_html = self.find_link(listing)
        return self.url_start + link_html['href']


class RightMoveScraper(PropertyWebsiteScraper):
    def __init__(self,
                 url_start="https://www.rightmove.co.uk",
                 url_continuing="/property-for-sale/find.html?locationIdentifier=REGION%5E550",
                 url_min_bed="&minBedrooms=",
                 url_ending="&sortType=6",
                 listing_scraper=("div", "propertyCard-wrapper"),
                 price_scraper=("div", "propertyCard-priceValue"),
                 bedrooms_scraper=("h2", "propertyCard-title"),
                 address_scraper=("address", "propertyCard-address"),
                 link_scraper=("a", "propertyCard-link")):

        super().__init__(url_start, url_continuing, url_min_bed, url_ending, listing_scraper, price_scraper, bedrooms_scraper, address_scraper, link_scraper)

    def next_page(self, page_number):
        return "&index=" + str(page_number*24)

    def return_url(self, min_bedrooms, page_number):
        next_page = self.next_page(page_number)
        url = self.url_start + self.url_continuing + self.url_min_bed + str(min_bedrooms)\
              + self.url_ending + next_page
        return url


class ZooplaScraper(PropertyWebsiteScraper):
    def __init__(self,
                 url_start="https://www.zoopla.co.uk",
                 url_continuing="/for-sale/property/glasgow/?",
                 url_min_bed="beds_min=",
                 url_ending="&identifier=glasgow&q=Glasgow&search_source=refine&radius=0&pn=",
                 listing_scraper=("li", "srp"),
                 price_scraper=("a", "listing-results-price"),
                 bedrooms_scraper=("h2", "listing-results-attr"),
                 address_scraper=("a", "listing-results-address"),
                 link_scraper=("a", "listing-results-address")):

        super().__init__(url_start, url_continuing, url_min_bed, url_ending, listing_scraper, price_scraper, bedrooms_scraper, address_scraper, link_scraper)


class S1homesScraper(PropertyWebsiteScraper):
    def __init__(self,
                 url_start="https://www.s1homes.com",
                 url_continuing="/property-for-sale/forsale_search_results.cgi?refine=0&veryLocal=7",
                 url_min_bed="&bedrooms=",
                 url_ending="&&location=7&newhomes=yes&locationText=Glasgow%2C%20Scotland&sort=pr&page=",
                 listing_scraper=("div", "listing"),
                 price_scraper=("h5", "hidden-xs"),
                 bedrooms_scraper=("h5", "hidden-xs"),
                 address_scraper=("a", "prop-link"),
                 link_scraper=("a", "prop-link")):

        super().__init__(url_start, url_continuing, url_min_bed, url_ending, listing_scraper, price_scraper, bedrooms_scraper, address_scraper, link_scraper)

    def return_price(self, listing):
        price_string = self.find_price(listing)
        price_string = price_string.split()[2]
        price_string = price_string.strip('£ ')
        price_string = price_string.replace(',', '')
        if price_string.isdigit():
            return int(price_string)
        else:
            return False

    def find_bedrooms(self, listing):
        bedrooms = listing.find_all(self.bedrooms_scraper[0], class_=self.bedrooms_scraper[1])
        return bedrooms[1].text

    def return_bedrooms(self, listing):
        bedrooms_string = self.find_bedrooms(listing)
        bedrooms_string = bedrooms_string.split()[0]
        if bedrooms_string.isdigit():
            return int(bedrooms_string)
        else:
            return False


if __name__=="__main__":
    min_bedrooms = 3
    price_per_bedroom = 1000000
    num_to_check = 1

    listings = []
    RightMove = RightMoveScraper()
    listings += RightMove.find_suitable_listings(min_bedrooms=min_bedrooms, price_per_bedroom=price_per_bedroom, num_to_check=num_to_check)
    ZooplaScraper = ZooplaScraper()
    listings += ZooplaScraper.find_suitable_listings(min_bedrooms=min_bedrooms, price_per_bedroom=price_per_bedroom, num_to_check=num_to_check)
    S1homes = S1homesScraper()
    listings += S1homes.find_suitable_listings(min_bedrooms=min_bedrooms, price_per_bedroom=price_per_bedroom, num_to_check=num_to_check)

    with open('properties_scrape.csv', 'a+') as csv_file:
        csv_file.seek(0)
        csv_reader = csv.reader(csv_file)
        links = [line[3] for line in csv_reader]
        csv_writer = csv.writer(csv_file)
        for listing in listings:
            if listing[3] not in links:
                csv_writer.writerow([listing[0], listing[1], listing[2], listing[3]])
