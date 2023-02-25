from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import lxml

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'HX-Request': 'true',
    'HX-Trigger': '_gcaptcha_pt',
    'HX-Target': 'target',
    'HX-Current-URL': 'https://ssstik.io/en',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://ssstik.io',
    'Alt-Used': 'ssstik.io',
    'Connection': 'keep-alive',
    'Referer': 'https://ssstik.io/en',
    # Requests sorts cookies= alphabetically
    'Cookie': '_ga=GA1.2.1955429624.1677304202; _gid=GA1.2.2127585060.1677304202; _gat_UA-3524196-6=1; __gads=ID=3d666f7d4af6ac74-222962c523da00e3:T=1677304208:RT=1677304208:S=ALNI_MabiDzCv1NpAXT0wW6SwluLjXls4Q; __gpi=UID=00000bcba517ba12:T=1677304208:RT=1677304208:S=ALNI_MZ9cj0AIEiDoTBEZ6sWjwx0moxcvA',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

app = Flask(__name__)

@app.route('/tiktok', methods=['GET'])
def get_tiktok_data():
    url = request.args.get('url')
    data = f'id={url}&locale=en&tt=OGVMYXE1'
    respo = requests.post('https://ssstik.io/abc?url=dl',  headers=headers, data=data)
    soup = BeautifulSoup(respo.content, 'lxml')
    # Get the direct download link
    link = soup.find('a', id='direct_dl_link')
    download_link = link['href']
    
    # Get the image src
    img_tag = soup.find('img', class_='u-round result_author')
    img_src = img_tag['src']
    
    # Get the h2 text
    h2 = soup.find('h2')
    h2_text = h2.text.strip()
    
    # Get the p text
    p = soup.find('p', class_='maintext')
    p_text = p.text.strip()
    
    # Extract number of likes
    likes = soup.select_one('.trending-actions div:nth-child(1) div:nth-child(2)').text.strip()
    
    # Extract number of comments
    comments = soup.select_one('.trending-actions div:nth-child(2) div').text.strip()
    
    # Extract number of shares
    shares = soup.select_one('.trending-actions div:nth-child(3) div').text.strip()
    
    data = {
        "download_link": download_link,
        "image_src": img_src,
        "title": h2_text,
        "description": p_text,
        "likes": likes,
        "comments": comments,
        "shares": shares
    }
    
    return jsonify(data)

if __name__ == '__main__':
    app.run()
