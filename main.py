import requests
from bs4 import BeautifulSoup


class HouseScraper:
    def __init__(self, url, filename):
        self.url = url
        self.filename = filename

    def fetch_houses(self):
        """Hämtar alla hus från hemsidan och returnerar en lista med titlar och URL:er."""
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        houses = soup.find_all('li', class_='sv-search-hit')

        house_list = []
        for house in houses:
            title_element = house.find('a', class_='h3rubrik')
            title = title_element.get_text(strip=True)
            title = ' '.join(title.split())
            house_url = "https://auktionstorget.kronofogden.se" + title_element['href']
            house_list.append(f"{title} | {house_url}")

        return house_list

    def save_houses_to_file(self, house_list):
        """Sparar alla hus till en textfil."""
        with open(self.filename, "w") as file:
            for house in house_list:
                file.write(house + "\n")

    def compare_and_update_houses(self):
        """Jämför nuvarande hus med de i textfilen och skriver ut nya hus, om det finns några."""
        current_houses = self.fetch_houses()

        try:
            with open(self.filename, "r") as file:
                saved_houses = file.read().splitlines()
        except FileNotFoundError:
            # Om filen inte finns, hämta och spara husen direkt
            print("Filen hittades inte, skapar ny fil och sparar nuvarande huslista.")
            self.save_houses_to_file(current_houses)
            return

        # Jämför och hitta nya hus
        new_houses = [house for house in current_houses if house not in saved_houses]

        if new_houses:
            print("Nya hus har kommit ut:")
            for house in new_houses:
                print(house)
            self.save_houses_to_file(current_houses)
        else:
            print("Auktionstorget: Inga nya hus har kommit ut.")

    def run(self):
        """Kör programmet med kontroll av filstatus."""
        try:
            with open(self.filename, "r") as file:
                # Fil finns, kör jämförelse
                self.compare_and_update_houses()
        except FileNotFoundError:
            # Filen hittas inte, hämta och spara aktuella hus
            print("Filen hittades inte, hämtar och sparar aktuella hus.")
            current_houses = self.fetch_houses()
            self.save_houses_to_file(current_houses)


# Exempelanvändning
url = "https://auktionstorget.kronofogden.se/Sokfastigheterbostadsratter.html?sv.url=12.6294450154af3d2b27d64&query=*&100.6294450154af3d2b27d91=12"
filename = "hus_list.txt"

scraper = HouseScraper(url, filename)
scraper.run()
