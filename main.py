import asyncio, hytale

async def download_all():    
    posts = await hytale.get_all_posts()
    clips_ids = list()
    for post in posts:
        print("Fetch video ids...")
        print(post.title)
        content = await hytale.get_all_videos(post)
        print(f"Post clips: {content}")
        clips_ids.extend(id for id in content if id not in clips_ids)
    # get clips from /media
    clips_ids.extend(id for id in await hytale.get_media_clips() if id not in clips_ids)

    print(f"Clipss uuids: {clips_ids}")
    for id in clips_ids:
        await hytale.download_video(id)

def main():
    asyncio.run(download_all())

if __name__ == "__main__":
    main()