import asyncio, hytale

async def download_all():    
    posts = await hytale.get_all_posts()
    video_ids = list()
    for post in posts:
        print("Fetch video ids...")
        print(post.title)
        video_ids.extend(await hytale.get_all_videos(post))
    # get clips from /media
    video_ids.extend(await hytale.get_media_clips())

    for id in video_ids:
        await hytale.download_video(id)

def main():
    asyncio.run(download_all())

if __name__ == "__main__":
    main()