import asyncio, hytale

async def download_all():    
    posts = await hytale.get_all_posts()
    video_ids = list()
    for post in posts:
        print("Fetch video ids...")
        print(post.title)
        content = await hytale.get_all_videos(post)
        print(f"Post clips: {content}")
        video_ids.extend(id for id in content if id not in video_ids)
    # get clips from /media
    video_ids.extend(id for id in await hytale.get_media_clips() if id not in video_ids)

    print(video_ids)
    for id in video_ids:
        await hytale.download_video(id)

def main():
    asyncio.run(download_all())

if __name__ == "__main__":
    main()