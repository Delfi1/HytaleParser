import click, asyncio, hytale

async def run(main: bool, fanarts: bool, media: bool):
    posts = await hytale.get_all_posts()
    
    for i in range(len(posts)):
        slug = posts[i].slug
        print(f"p({i}) = {slug}")

    # Posts id's
    fp = set([12, 22, 33])
    mp = set(range(len(posts))).difference(fp)
    
    total = list()
    if main: total += mp
    if fanarts: total += fp
    total = sorted(total)

    print("Downloading posts")
    for n in total:
        post = posts[n]
        print(f"Downloading content from {post}...", end=' ')

        clips = post.get_clips()
        videos = post.get_youtube_vids()
        images = post.get_images()
        
        print(f"Found {len(clips)} clips, {len(videos)} youtube videos and {len(images)} images:")
        print("Downloading clips...")
        for id in clips:
            await hytale.download_clip(id)
        print("Downloading youtube videos...")
        for url in videos:
            await hytale.download_video(url)
        print("Downloading images...")
        for url in images:
            await hytale.download_image(url)
        print()

    if media:
        data = await hytale.get_media()
        print("Downloading all media data...")
        clips = data['clips']
        images = data['screenshots'] + data['conceptArt']
        
        print("Downloading clips...")
        for clip in clips:
            await hytale.download_clip(clip['src'])
        
        print("Downloading images...")
        for img in images:
            await hytale.download_image(f"https://cdn.hytale.com/{img['src']}")
    

@click.command()
@click.option("--main", default=True, help="Download main posts data")
@click.option("--fanarts", default=False, help="Download fanarts posts data")
@click.option("--media", default=True, help="Download ./media data")
def main(main: bool, fanarts: bool, media: bool):
    asyncio.run(run(main, fanarts, media))

if __name__ == "__main__":
    main()