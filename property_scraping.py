import csv
import requests
from bs4 import BeautifulSoup


class PropertyWebsiteScraper:
    """Website scrapper class containing methods which are used for
    scrapping property websites for information about the properties

    Args:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link


    Attributes:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link
    """

    def __init__(self, url_host_name, url_continuing, url_min_bed, url_ending, listing_scraper,
                 price_scraper, bedrooms_scraper, address_scraper, link_scraper):
        self.url_host_name = url_host_name
        self.url_continuing = url_continuing
        self.url_min_bed = url_min_bed
        self.url_ending = url_ending
        self.listing_scraper = listing_scraper
        self.price_scraper = price_scraper
        self.bedrooms_scraper = bedrooms_scraper
        self.address_scraper = address_scraper
        self.link_scraper = link_scraper

    def return_url(self, min_bedrooms, page_number):
        """Return url address which is gonna be used for scraping"""
        url = self.url_host_name + self.url_continuing + self.url_min_bed + str(min_bedrooms) +\
              self.url_ending + str(page_number)
        return url

    def find_suitable_listings(self, min_bedrooms, price_per_bedroom, num_to_check):
        """Return all listing fitting the criteria from website"""
        count = 0
        page = 0
        listings = []
        while count < num_to_check:
            url = self.return_url(min_bedrooms, page)
            soup = return_soup(url)
            for listing in soup.find_all(self.listing_scraper[0], class_=self.listing_scraper[1]):
                price = self.return_price(listing)
                bedrooms = self.return_bedrooms(listing)
                address = self.return_address(listing)
                link = self.return_link(listing)
                if check_valid_listing(bedrooms, price, price_per_bedroom, min_bedrooms):
                    listings.append([price, bedrooms, address, link])
                count += 1
            page += 1
        return listings

    def find_price(self, listing):
        """Finds place on the website which stores information about number of bedrooms"""
        price = listing.find(self.price_scraper[0], class_=self.price_scraper[1])
        return price.text

    def return_price(self, listing):
        """returns price from the listing"""
        price_string = self.find_price(listing)
        price_string = price_string.split()[0]
        price_string = price_string.strip('£ ')
        price_string = price_string.replace(',', '')
        if price_string.isdigit():
            return int(price_string)
        return False

    def find_bedrooms(self, listing):
        """Finds place on the website which stores information about number of bedrooms"""
        bedrooms = listing.find(self.bedrooms_scraper[0], class_=self.bedrooms_scraper[1])
        return bedrooms.text

    def return_bedrooms(self, listing):
        """returns number of bedrooms from the listing"""
        bedrooms_string = self.find_bedrooms(listing)
        return_bed = bedrooms_string.split()[0]
        if return_bed.isdigit():
            return int(return_bed)
        return False

    def find_address(self, listing):
        """Finds place on the website which stores information about address"""
        address = listing.find(self.address_scraper[0], class_=self.address_scraper[1])
        return address.text

    def return_address(self, listing):
        """returns address from the listing"""
        address_string = self.find_address(listing)
        return " ".join(address_string.split())

    def find_link(self, listing):
        """Finds place on the website which stores link to the listing"""
        link = listing.find(self.link_scraper[0], class_=self.link_scraper[1])
        return link

    def return_link(self, listing):
        """returns link from the listing"""
        link_html = self.find_link(listing)
        return self.url_host_name + link_html['href']


class RightMoveScraper(PropertyWebsiteScraper):
    """Website scrapper class containing methods which are used for
    scrapping RightMove Website for information about the properties

    Inherits from PropertyWebsiteScraper class

    Args:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link


    Attributes:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link
    """

    def __init__(self,
                 url_host_name="https://www.rightmove.co.uk",
                 url_continuing="/property-for-sale/find.html?locationIdentifier=REGION%5E550",
                 url_min_bed="&minBedrooms=",
                 url_ending="&sortType=6",
                 listing_scraper=("div", "propertyCard-wrapper"),
                 price_scraper=("div", "propertyCard-priceValue"),
                 bedrooms_scraper=("h2", "propertyCard-title"),
                 address_scraper=("address", "propertyCard-address"),
                 link_scraper=("a", "propertyCard-link")):
        super().__init__(url_host_name, url_continuing, url_min_bed, url_ending, listing_scraper,
                         price_scraper, bedrooms_scraper, address_scraper, link_scraper)

    def next_page(self, page_number):
        """Return next page url parameter"""
        return "&index=" + str(page_number * 24)

    def return_url(self, min_bedrooms, page_number):
        """Return url address which is gonna be used for scraping"""
        next_page = self.next_page(page_number)
        url = self.url_host_name + self.url_continuing + self.url_min_bed + str(min_bedrooms) \
              + self.url_ending + next_page
        return url


class ZooplaScraper(PropertyWebsiteScraper):
    """Website scrapper class containing methods which are used for
    scrapping Zoopla Website for information about the properties

    Inherits from PropertyWebsiteScraper class

    Args:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link


    Attributes:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link
    """

    def __init__(self,
                 url_host_name="https://www.zoopla.co.uk",
                 url_continuing="/for-sale/property/glasgow/?",
                 url_min_bed="beds_min=",
                 url_ending="&identifier=glasgow&q=Glasgow&search_source=refine&radius=0&pn=",
                 listing_scraper=("li", "srp"),
                 price_scraper=("a", "listing-results-price"),
                 bedrooms_scraper=("h2", "listing-results-attr"),
                 address_scraper=("a", "listing-results-address"),
                 link_scraper=("a", "listing-results-address")):
        super().__init__(url_host_name, url_continuing, url_min_bed, url_ending, listing_scraper,
                         price_scraper, bedrooms_scraper, address_scraper, link_scraper)


class S1homesScraper(PropertyWebsiteScraper):
    """Website scrapper class containing methods which are used for
    scrapping S1homes Website for information about the properties

    Inherits from PropertyWebsiteScraper class

    Args:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link


    Attributes:
        url_host_name (str): url
        url_continuing (str): path and arguments after
        url_min_bed (str): url min bedroom query string
        url_ending (str): query string finishing the url
        listing_scraper (tuple, str): tuple containing string find parameter for listing
        price_scraper (tuple, str): tuple containing string find parameter for price
        address_scraper (tuple, str): tuple containing string find parameter for address
        bedrooms_scraper (tuple, str): tuple containing string find parameter for bedrooms
        link_scraper (tuple, str): tuple containing string find parameter for link
    """

    def __init__(self,
                 url_host_name="https://www.s1homes.com",
                 url_continuing="/property-for-sale/forsale_search_results.cgi?refine=0&veryLocal=7",
                 url_min_bed="&bedrooms=",
                 url_ending="&&location=7&newhomes=yes&locationText=Glasgow%2C%20Scotland&sort=pr&page=",
                 listing_scraper=("div", "listing"),
                 price_scraper=("h5", "hidden-xs"),
                 bedrooms_scraper=("h5", "hidden-xs"),
                 address_scraper=("a", "prop-link"),
                 link_scraper=("a", "prop-link")):

        super().__init__(url_host_name, url_continuing, url_min_bed, url_ending, listing_scraper,
                         price_scraper, bedrooms_scraper, address_scraper, link_scraper)

    def return_price(self, listing):
        """returns price from the listing"""
        price_string = self.find_price(listing)
        price_string = price_string.split()[2]
        price_string = price_string.strip('£ ')
        price_string = price_string.replace(',', '')
        if price_string.isdigit():
            return int(price_string)
        return False

    def find_bedrooms(self, listing):
        """Finds place on the website which stores information about number of bedrooms"""
        bedrooms = listing.find_all(self.bedrooms_scraper[0], class_=self.bedrooms_scraper[1])
        return bedrooms[1].text

    def return_bedrooms(self, listing):
        """returns number of bedrooms from the listing"""
        bedrooms_string = self.find_bedrooms(listing)
        bedrooms_string = bedrooms_string.split()[0]
        if bedrooms_string.isdigit():
            return int(bedrooms_string)
        return False


def return_soup(url):
    """Return BeautifulSoup entity created from url received"""
    res = requests.get(url)
    res.raise_for_status()
    content = res.text
    soup = BeautifulSoup(content, "html.parser")
    return soup


def check_valid_listing(bedrooms, price, price_per_bedroom, min_bedrooms):
    """Check if listing is valid"""
    if bedrooms and price:
        condition2 = price / bedrooms < price_per_bedroom
        condition3 = bedrooms >= min_bedrooms
        if condition2 and condition3:
            return True
    return False


if __name__ == "__main__":
    MIN_BEDROOMS = 5
    PRICE_PER_BEDROOM = 50000
    NUM_TO_CHECK = 1

    LISTINGS = []
    RIGHT_MOVE_SCRAPER = RightMoveScraper()
    LISTINGS += RIGHT_MOVE_SCRAPER.find_suitable_listings(min_bedrooms=MIN_BEDROOMS,
                                                          price_per_bedroom=PRICE_PER_BEDROOM,
                                                          num_to_check=NUM_TO_CHECK)
    ZOOPLA_SCRAPER = ZooplaScraper()
    LISTINGS += ZOOPLA_SCRAPER.find_suitable_listings(min_bedrooms=MIN_BEDROOMS,
                                                      price_per_bedroom=PRICE_PER_BEDROOM,
                                                      num_to_check=NUM_TO_CHECK)
    S1HOMES_SCRAPPER = S1homesScraper()
    LISTINGS += S1HOMES_SCRAPPER.find_suitable_listings(min_bedrooms=MIN_BEDROOMS,
                                                        price_per_bedroom=PRICE_PER_BEDROOM,
                                                        num_to_check=NUM_TO_CHECK)

    with open('properties_scrape.csv', 'a+') as csv_file:
        csv_file.seek(0)
        CSV_READER = csv.reader(csv_file)
        LINKS = [line[3] for line in CSV_READER]
        CSV_WRITER = csv.writer(csv_file)
        for property_listing in LISTINGS:
            if property_listing[3] not in LINKS:
                CSV_WRITER.writerow([property_listing[0], property_listing[1],
                                     property_listing[2], property_listing[3]])
