import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_data = {}

    try:
        product_data['url'] = url

        title = soup.find('span', id='productTitle')
        if title:
            product_data['title'] = title.get_text().strip()
        else:
            product_data['title'] = 'N/A'

        price = soup.find('span', id='priceblock_ourprice')
        if price:
            product_data['price'] = price.get_text().strip()
        else:
            product_data['price'] = 'N/A'

        rating = soup.find('span', class_='a-icon-alt')
        if rating:
            product_data['rating'] = rating.get_text().strip().split()[0]
        else:
            product_data['rating'] = 'N/A'

        reviews = soup.find('span', id='acrCustomerReviewText')
        if reviews:
            product_data['reviews'] = reviews.get_text().strip()
        else:
            product_data['reviews'] = 'N/A'

        description = soup.find('meta', {'name': 'description'})['content']
        product_data['description'] = description
        
        asin = soup.find('th', text='ASIN').find_next_sibling('td').get_text().strip()
        product_data['asin'] = asin
        
        product_desc = soup.find('div', id='productDescription')
        if product_desc:
            product_data['product_description'] = product_desc.get_text().strip()
        else:
            product_data['product_description'] = 'N/A'
        
        manufacturer = soup.find('a', id='bylineInfo')
        if manufacturer:
            product_data['manufacturer'] = manufacturer.get_text().strip()
        else:
            product_data['manufacturer'] = 'N/A'
        
    except:
        pass

    return product_data

def scrape_product_list_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product_urls = []

    try:
        results = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for result in results:
            product_link = result.find('a', class_='a-link-normal.s-no-outline')['href']
            if product_link and product_link.startswith('/'):
                product_url = f"https://www.amazon.in{product_link}"
                product_urls.append(product_url)
                
    except:
        pass

    return product_urls

def main():
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}"
    
    all_product_urls = []

    for page_number in range(1, 21):
        page_url = base_url.format(page_number)
        page_product_urls = scrape_product_list_page(page_url)
        all_product_urls.extend(page_product_urls)

    all_product_data = []

    for product_url in all_product_urls:
        product_data = scrape_product_page(product_url)
        all_product_data.append(product_data)

    csv_filename = "amazon_products.csv"
    csv_header = [
        'url', 'title', 'price', 'rating', 'reviews', 'description', 'asin',
        'product_description', 'manufacturer' 
    ]

    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_header)
        writer.writeheader()
        
        for product in all_product_data:
            writer.writerow(product)

    print(f"Scraped data has been saved to {csv_filename}")

if __name__ == "__main__":
    main()
