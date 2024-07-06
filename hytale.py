from typing import Any, List
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
        slug = self.slug
        return f"https://hytale.com/news/{yy}/{mm}/{slug}"
    
    def cover_url(self) -> str:
        return f"https://cdn.hytale.com/variants/blog_cover_{self.coverImage['s3Key']}"

    def __init__(self, data: dict):
        self.title = data['title']
        self.publishedAt = data['publishedAt']
        self.slug = data['slug']
        self.author = data['author']
        self.featured = data['featured']
        self.bodyExcerpt = data['bodyExcerpt']
        self.tags = data['tags']
        self._id = data['_id'] 
        self.coverImage = data['coverImage']

async def get_post_info(post: Post):
    title = f"Title: \"***{post.title}***\" \n"
    bodyExcerpt = f"BodyExcerpt: \"***{post.bodyExcerpt}***\" \n"
    author = f"Author: \"***{post.author}***\" \n"
    publishedAt = f"CreatedAt: \"***{post.publishedAt}***\" \n"
    featured = f"Featured: \"***{post.featured}***\" \n"
    tags = f"Tags: **{post.tags}** \n"
    id = f"Id: \"***{post._id}***\" \n"
    link = f"Link: {post.url()} \n"

    context = title + bodyExcerpt + author + publishedAt + featured + tags + id + link

    return context

async def get_all_posts() -> List[Post]:
    url = 'https://hytale.com/api/blog/post/published'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            result = await response.json()

    return [Post(data) for data in result]

async def get_latest_post() -> Post:
    posts = await get_all_posts()
    return posts[0]

async def get_post_by_id(post_id: int) -> Post:
    posts = await get_all_posts()
    return posts[len(posts) - post_id]

async def download_video(id: str):
    yt_opts = {'verbose': True,'outtmpl': 'clips/%(title)s.%(ext)s'}

    files = glob.glob(f"{id}.*", root_dir="./clips")
    if files:
        return files[0]

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download([f'https://iframe.videodelivery.net/{id}'])
    
    file = glob.glob(f"{id}.*", root_dir="./clips")
    return file[0]
    
async def get_all_videos(post: Post) -> list:
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
        except Exception as e:
            ...
    
    return result

async def get_media_clips() -> list:
    request = urllib.request.Request("https://hytale.com/media", headers=headers)
    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html, "html.parser")
    
    raw_media = soup.select_one("script:-soup-contains('clips')").string
    media = json.loads(raw_media[raw_media.index("["):raw_media.rindex("]")+1])[0]['media']

    clips = media['clips']

    result = list()
    for clip in clips:
        result.append(clip['src'])
    return result