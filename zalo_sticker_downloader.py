from bs4 import BeautifulSoup
import regex as re
import imageio
from pathlib import Path
import requests
import os
import shutil
from PIL import Image


def download_image(url, path):
    response = requests.get(url, timeout=5)
    with open(path, 'wb') as f:
        f.write(response.content)

def split_image(path):
    name = path.split('/')[-1].replace('.png', '')
    img = Image.open(path)
    width, height = img.size
    for i in range(0, width, 130):
        new_img = img.crop((i, 0, i + 130, 130))
        new_img.save('images/' + str(name) + '_' + str(i//130) + '.png')


def make_gif(path, gif_name):
    Path('gifs').mkdir(parents=True, exist_ok=True)
    images = []
    for filename in Path(path).glob('%s_*.png' % gif_name):
        images.append(filename)
    images = sorted(images, key=lambda x: int(x.stem.split('_')[-1]))
    imageio.mimsave('gifs/' + gif_name + '.gif', [imageio.imread(str(filename)) for filename in images], duration=0.15)


urls = list()
with open('raw_html.txt', 'r') as f:
    raw_html = f.read()
    soup = BeautifulSoup(raw_html, 'html.parser')
    emoji_hrefs = soup.find_all('div', {'class': 'sticker sticker-message'})
    for emoji_href in emoji_hrefs:
        pattern = r"url\(\"(?P<url>.*)\"\);"
        match = re.search(pattern, str(emoji_href))
        urls.append(match.group('url').replace('amp;', ''))
print("Number of urls: %d" % len(urls))

for i, url in enumerate(urls):
    Path('images').mkdir(parents=True, exist_ok=True)
    path = 'images/' + str(i) + '.png'
    if not os.path.exists(path):
        download_image(url, path)
    else:
        print('Image already exists')

for i in range(len(urls)):
    path = 'images/' + str(i) + '.png'
    split_image(path)
    make_gif('images', str(i))
