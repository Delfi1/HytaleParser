import ast, click, asyncio, hytale

async def run(main: bool, fanarts: bool, media: bool, posts: list):
    slugs = await hytale.get_all_posts()

    # Posts id's
    fp = set([12, 22, 33])
    mp = set(range(len(slugs))).difference(fp)
    all = list(mp) + list(fp)

    total = list()
    if main: total += mp
    if fanarts: total += fp
    if len(posts) != 0: total = posts
    total = sorted(total)

    for t in total:
        # If post is not exists - skip
        if not t in all:
            continue

        slug = slugs[t]
        
        # If post can't be loaded
        try:
            post = await hytale.get_post_by_slug(slug)
            print(f"Downloading content from {post}...", end=' ')
        except:
            continue

        clips = post.get_clips()
        videos = post.get_youtube_vids()
        images = post.get_images()
        
        print(f"Found {len(clips)} clips, {len(videos)} youtube videos and {len(images)} images:")
        if len(clips) != 0: print("Downloading clips...")
        for id in clips:
            await hytale.download_clip(id)
        if len(videos) != 0: print("Downloading youtube videos...")
        for url in videos:
            await hytale.download_video(url)
        if len(images) != 0: print("Downloading images...")
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
@click.option("--media", default=True, help="Download /media data")
@click.option("--posts", default=str(), help="Overrides \"main\" and \"fanarts\". Example: \"[0, 1, 51]\"")
def main(main: bool, fanarts: bool, media: bool, posts: str):
    try: posts = ast.literal_eval(posts)
    except: posts = list()
    
    asyncio.run(run(main, fanarts, media, posts))

if __name__ == "__main__":
    main()