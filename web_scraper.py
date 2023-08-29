import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from google.colab import drive
drive.mount('/content/drive')


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

all_data = []

for i in range(1, 501):
    if i == 1:
        url = 'https://www.century21albania.com/properties'
    else:
        url = f"https://www.century21albania.com/properties?page={i}"

    response = requests.get(url, headers=headers)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')
    listings_container = soup.find('div', class_='osahan_top_filter cardShowProperties row')

    if listings_container:
        listings = listings_container.find_all('div', class_='col-lg-3 col-md-4 property')
        data = []

        for listing in listings:
            status_element = listing.find('span', class_ = 'badge-primary')
            status_element2 = listing.find('span', class_ = 'badge-danger')
            price_element = listing.find('h2', class_='text-primary mb-2')
            description_element = listing.find('h5', class_='card-title')
            location_element = listing.find('h6', class_='card-subtitle mt-1 mb-0 text-muted')
            surface_element = listing.find('div', class_='col-xs-3 col-sm-3 col-md-3 col-lg-3 FutureInfo col-3')
            no_rooms_elements = listing.find_all('div', class_='col-xs-3 col-sm-3 col-md-3 col-lg-3 FutureInfo col-3')
            no_bathrooms_elements = listing.find_all('div', class_='col-xs-3 col-sm-3 col-md-3 col-lg-3 FutureInfo col-3')

            # Extracting elements
            if status_element:
                status = status_element.text.strip()
            else:
                status = status_element2.text.strip()


            if price_element:
                price = price_element.text.strip()
            else:
                price = "N/A"

            if description_element:
                description = description_element.text.strip()
            else:
                description = "N/A"

            if location_element:
                location = location_element.text.strip()
            else:
                location = "N/A"

            if surface_element:
                area = surface_element.text.strip()
            else:
                area = "N/A"

            if len(no_rooms_elements) >= 2:
                no_rooms = no_rooms_elements[1].get_text(strip=True)
            else:
                no_rooms = "N/A"

            if len(no_rooms_elements) >= 3:
                no_bathrooms = no_rooms_elements[2].get_text(strip=True)
            else:
                no_bathrooms = "N/A"



                # Create a dictionary for the current listing
            listing_data = {
                'Status': status[3:],
                'Price': price[0:-2],
                'Description': description,
                'Location': location,
                'Area': area[0:-3],
                'No_rooms': no_rooms,
                'No_bathrooms': no_bathrooms
                }



            data.append(listing_data)

        all_data.extend(data)

    # Introduce a time delay between requests
    time.sleep(3)  # Delay for a no. of seconds

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(all_data)

# Save the DataFrame to a CSV file
csv_filename = '/content/drive/My Drive/real_estate_data.csv'
df.to_csv(csv_filename, index=False)


