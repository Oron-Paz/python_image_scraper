import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

Google_Image = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&'
u_agnt = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive',
}

def main():
    data = input('Enter your search keyword: ')
    num_images = int(input('Enter the number of images you want: '))
    folder_name = data + '_images'

    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    download_images(data, num_images, folder_name)

def download_images(data, num_images, folder_name):
    print('Searching Images....')
    
    search_url = Google_Image + 'q=' + data
    response = requests.get(search_url, headers=u_agnt)
    html = response.text
    
    b_soup = BeautifulSoup(html, 'html.parser')
    results = b_soup.findAll('img', {'class': 'rg_i Q4LuWd'})
    
    count = 0
    imagelinks = []
    for res in results:
        try:
            link = res['data-src']
            imagelinks.append(link)
            count += 1
            if count >= num_images:
                break
        except KeyError:
            continue
    
    print(f'Found {len(imagelinks)} images')
    print('Start downloading...')

    for i, imagelink in enumerate(imagelinks):
        response = requests.get(imagelink)

        try:
            # Use PIL to open the image and extract the format
            img = Image.open(BytesIO(response.content))
            file_extension = img.format.lower()
        except Exception as e:
            print(f"Error determining image format: {e}")
            file_extension = 'jpg'

        imagename = os.path.join(folder_name, f'{data}_{i+1}.{file_extension}')
        with open(imagename, 'wb') as file:
            file.write(response.content)

    print('Download Completed!')

if __name__ == '__main__':
    main()
