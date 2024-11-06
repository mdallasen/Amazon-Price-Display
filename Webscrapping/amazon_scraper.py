from bs4 import BeautifulSoup 
import requests
import pandas as pd

def amazon_category_top_10(base_url): 

    headers = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                            'Accept-Language': 'en-US, en;q=0.5'})

    # Send HTTP request
    response = requests.get(base_url, headers=headers)

    # Check if the request was sucessful and extract first 10 products 
    if response.status_code == 200: 
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        results = soup.find_all('div', {'data-component-type': 's-search-result'}, limit=10)

        for item in results:
            product = {}
            title_element = item.h2.a

            # Extract product name
            product['name'] = title_element.text.strip() if title_element else 'N/A'
            
            # Extract product link
            product['link'] = f"https://www.amazon.com{title_element['href']}" if title_element else 'N/A' 

            # Extract product price
            price = item.find('span', 'a-price-whole')
            product['price'] = f"${price.text}" if price else f"N/A"
 
            # Extract product rating
            rating = item.find('span', {'class': 'a-icon-alt'})
            product['rating'] = f"${rating.text}" if rating else f"N/A"

            # Extract review count
            reviews = item.find('span', {'class': 'a-size-base'})
            product['reviews'] = f"${reviews.text}" if reviews else f"N/A"

            products.append(product)

    return pd.DataFrame(products)