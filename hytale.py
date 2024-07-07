import os
from typing import Any, List
import requests
import json
import glob
import aiohttp
import urllib.request
import yt_dlp
from bs4 import BeautifulSoup

# response headers
headers = {
    'User-Agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}

class Post:
    def url(self) -> str:
        yy = int(self.publishedAt[:4])
        mm = int(self.publishedAt[5:7])
        return f"https://hytale.com/news/{yy}/{mm}/{self.slug}"

    def __init__(self, data: dict):
        self.title = data['title']
        self.publishedAt = data['publishedAt']
        self.slug = data['slug']

async def get_all_posts() -> List[Post]:
    url = 'https://hytale.com/api/blog/post/published'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            result = await response.json()

    return [Post(data) for data in result]

async def download_clip(id: str):
    print(f"Downloading {id}...", end=' ')
    yt_opts = {'verbose': True,'outtmpl': 'clips/%(title)s.%(ext)s'}

    files = glob.glob(f"{id}.*", root_dir="./clips")
    if files:
        print("Already installed, skip")
        return files[0]
    print()

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([f'https://iframe.videodelivery.net/{id}'])
    
    file = glob.glob(f"{id}.*", root_dir="./clips")
    return file[0]
    
async def download_image(url: str):
    img = url[url.rfind('/')+1:]
    print(f"Downloading {img}...", end=' ')
    
    file = glob.glob(img, root_dir="./images")
    if file:
        print("Already installed, skip")
        return
    
    path = f"./images/{img}"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as handle:
        data = requests.get(url, stream=True)
        handle.write(data.content)

    print("Success")

async def get_all_clips(post: Post) -> list:
    url = post.url()

    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find("div", {"class": "post__body"})
    
    result = list()

    for element in body:
        try:
            if element['class'][0] == "video-container":
                stream = element.find("stream")

                if stream:
                    result.append(stream["src"])
        except Exception as e: ...
    
    return result

async def get_all_images(post: Post) -> list:
    url = post.url()

    request = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find("div", {"class": "post__body"})
    imgs = body.find_all("img")

    result = list()
    for img in imgs:
        try:
            result.append(img['data-src'])
        except Exception as e: ...

    return result

async def get_media() -> list:
    request = urllib.request.Request("https://hytale.com/media", headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, "html.parser")
    
    raw_media = soup.select_one("script:-soup-contains('clips')").string
    return json.loads(raw_media[raw_media.index("["):raw_media.rindex("]")+1])[0]['media']

# Returns list of clips uuids
async def get_media_clips() -> list:
    media = await get_media()

    clips = media['clips']

    result = list()
    for clip in clips:
        result.append(clip['src'])
    return result

# Rerurns list of links
async def get_media_images() -> list:
    media = await get_media()
    images = media['screenshots'] + media['conceptArt']

    result = list()
    for image in images:
        result.append(f"https://cdn.hytale.com/{image['src']}")

    return result