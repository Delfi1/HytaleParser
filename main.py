import asyncio, hytale

async def download_all():
    # get all posts
    posts = await hytale.get_all_posts()

    # get clips from all posts
    print("Downloading clips...")
    clips_ids = list()
    for post in posts:
        print(f"Fetch clips ids in {post.title}...")
        content = await hytale.get_all_clips(post)
        print(f"Post clips: {content}")
        clips_ids.extend(id for id in content if id not in clips_ids)
    # get clips from /media
    clips_ids.extend(id for id in await hytale.get_media_clips() if id not in clips_ids)

    for id in clips_ids:
        await hytale.download_clip(id)

    # get images from all posts
    print("Dowloading images...")
    images_url = list()
    for post in posts:
        print(f"Fetch images in {post.title}...")
        content = await hytale.get_all_images(post)
        print(f"Post images: {content}")
        images_url.extend(url for url in content if url not in images_url)
    # get images from /media
    images_url.extend(url for url in await hytale.get_media_images() if url not in images_url)
    
    for url in images_url:
        await hytale.download_image(url)

def main():
    asyncio.run(download_all())

if __name__ == "__main__":
    main()