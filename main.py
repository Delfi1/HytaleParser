import asyncio, hytale

async def download_all():
    # get all posts
    print("Proceeding to download all data", end='\n\n')
    print("Getting all posts data...")
    posts = await hytale.get_all_posts()

    print("Getting all media data...")
    media = await hytale.get_media()

    print("Downloading all posts data...")
    for post in posts:
        print(f"Downloading content from {post}...", end=' ')

        clips = post.get_clips()
        images = post.get_images()
        
        print(f"Found {len(clips)} clips and {len(images)} images:")
        print("Downloading clips...")
        for id in clips:
            await hytale.download_clip(id)
        print("Downloading images...")
        for url in images:
            await hytale.download_image(url)
        print()

    print("Downloading all media data...")
    clips = media['clips']
    images = media['screenshots'] + media['conceptArt']
    
    print("Downloading clips...")
    for clip in clips:
        await hytale.download_clip(clip['src'])
    
    print("Downloading images...")
    for img in images:
        await hytale.download_image(f"https://cdn.hytale.com/{img['src']}")


def main():
    asyncio.run(download_all())

if __name__ == "__main__":
    main()