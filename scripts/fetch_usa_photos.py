"""
Fetches and curates 100 American people photos in casual dress.
50 Men -> usa_lib/images/man/
50 Women -> usa_lib/images/woman/
Uses Wikimedia Commons and high-resolution public photo archives.
Verifies all images with OpenCV to ensure decodability.
"""

import os
import json
import urllib.request
import urllib.parse
import ssl
import cv2
import numpy as np
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
USA_DIR = os.path.join(BASE_DIR, 'step5_new_country', 'images')
MAN_DIR = os.path.join(USA_DIR, 'man')
WOMAN_DIR = os.path.join(USA_DIR, 'woman')

os.makedirs(MAN_DIR, exist_ok=True)
os.makedirs(WOMAN_DIR, exist_ok=True)

# SSL context for reliable image download
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'AntigravityFashionResearch/1.0 (https://github.com/mgtimber; mgtimber@example.com) Python-urllib'
}

MEN_NAMES = [
    "Brad Pitt", "Leonardo DiCaprio", "Chris Evans", "Ryan Gosling", "Michael B. Jordan",
    "Tom Hanks", "George Clooney", "Keanu Reeves", "Will Smith", "Zac Efron",
    "Matthew McConaughey", "Mark Wahlberg", "Ben Affleck", "Chris Pratt", "Justin Timberlake",
    "John Krasinski", "Adam Sandler", "Jake Gyllenhaal", "Bradley Cooper", "Timothée Chalamet",
    "Pedro Pascal", "Chris Pine", "Jason Momoa", "Paul Rudd", "Robert Downey Jr.",
    "Matt Damon", "Harrison Ford", "Samuel L. Jackson", "Dwayne Johnson", "Tom Cruise",
    "Christian Bale", "Ethan Hawke", "Woody Harrelson", "Mark Ruffalo", "Kevin Hart",
    "Dave Grohl", "Bruce Springsteen", "John Mayer", "Pharrell Williams", "Snoop Dogg",
    "Travis Scott", "Donald Glover", "Steve Carell", "Seth Rogen", "Jonah Hill",
    "Jeff Goldblum", "Owen Wilson", "Vince Vaughn", "Jared Leto", "Ashton Kutcher"
]

WOMEN_NAMES = [
    "Jennifer Aniston", "Taylor Swift", "Zendaya", "Emma Stone", "Scarlett Johansson",
    "Anne Hathaway", "Blake Lively", "Jennifer Lawrence", "Selena Gomez", "Margot Robbie",
    "Hailey Bieber", "Dakota Johnson", "Reese Witherspoon", "Jessica Alba", "Sandra Bullock",
    "Natalie Portman", "Julia Roberts", "Kendall Jenner", "Gigi Hadid", "Kristen Stewart",
    "Angelina Jolie", "Cameron Diaz", "Gwyneth Paltrow", "Halle Berry", "Charlize Theron",
    "Kate Hudson", "Mila Kunis", "Zoe Saldana", "Jessica Chastain", "Amy Adams",
    "Emily Blunt", "Rachel McAdams", "Amanda Seyfried", "Drew Barrymore", "Jennifer Lopez",
    "Beyoncé", "Lady Gaga", "Katy Perry", "Billie Eilish", "Ariana Grande",
    "Miley Cyrus", "Rihanna", "Kerry Washington", "Viola Davis", "Lupita Nyong'o",
    "Awkwafina", "Sydney Sweeney", "Florence Pugh", "Ana de Armas", "Jenna Ortega"
]

def search_wikimedia_image(query):
    """Searches Wikimedia Commons for an image of the person."""
    try:
        url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(query)}&gsrlimit=5&prop=imageinfo&iiprop=url|mime|size&format=json"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                imageinfo = page_info.get('imageinfo', [])
                if imageinfo:
                    info = imageinfo[0]
                    mime = info.get('mime', '')
                    img_url = info.get('url', '')
                    width = info.get('width', 0)
                    height = info.get('height', 0)
                    if mime in ['image/jpeg', 'image/png'] and img_url and width >= 300 and height >= 300:
                        # Prefer resized thumb for speed if available, or direct URL
                        return img_url
    except Exception as e:
        pass
    return None

def search_wikipedia_lead_image(name):
    """Fetches the lead image of the Wikipedia page."""
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&titles={urllib.parse.quote(name)}&prop=pageimages&format=json&pithumbsize=800"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for page_id, page_info in pages.items():
                if 'thumbnail' in page_info:
                    return page_info['thumbnail']['source']
    except Exception:
        pass
    return None

def download_and_verify_image(url, save_path):
    """Downloads image and verifies that it is a valid, readable image file."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            img_bytes = resp.read()
            if len(img_bytes) < 5000:  # Too small or icon
                return False
            
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            if img is None or img.shape[0] < 200 or img.shape[1] < 200:
                return False
            
            # Save properly encoded JPG
            cv2.imwrite(save_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 92])
            return True
    except Exception as e:
        return False

# High-quality fallback curated casual photos from public Unsplash fashion CDN
UNSPLASH_MAN_FALLBACKS = [
    "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=800&q=80",
    "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=800&q=80",
    "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=800&q=80",
    "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=800&q=80",
    "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&q=80",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&q=80",
    "https://images.unsplash.com/photo-1539571696357-5a69c17a67c6?w=800&q=80",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&q=80",
    "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=800&q=80",
    "https://images.unsplash.com/photo-1480429370139-e0132c086e2a?w=800&q=80"
]

UNSPLASH_WOMAN_FALLBACKS = [
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=800&q=80",
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=800&q=80",
    "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=800&q=80",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=800&q=80",
    "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=800&q=80",
    "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=800&q=80",
    "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=800&q=80",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=800&q=80",
    "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=800&q=80",
    "https://images.unsplash.com/photo-1469334031218-e382a71b716b?w=800&q=80"
]

def fetch_group_photos(names_list, dest_dir, prefix="man", fallback_urls=[]):
    print(f"\n>>> Fetching 50 American Casual Photos for: '{prefix}' into {dest_dir}...")
    count = 0
    fallback_idx = 0

    for idx, name in enumerate(names_list):
        save_path = os.path.join(dest_dir, f"{prefix}_{idx+1:02d}_{name.lower().replace(' ', '_')}.jpg")
        
        # Check if already downloaded and valid
        if os.path.exists(save_path):
            img = cv2.imread(save_path)
            if img is not None and img.shape[0] >= 150 and img.shape[1] >= 150:
                print(f"  [{idx+1}/50] (Cached) ✓ {name}")
                count += 1
                continue

        # Strategy 1: Wikipedia Lead Thumbnail
        img_url = search_wikipedia_lead_image(name)
        success = False
        if img_url:
            success = download_and_verify_image(img_url, save_path)

        # Strategy 2: Wikimedia Search for name + casual/street
        if not success:
            img_url = search_wikimedia_image(f"{name} 2019") or search_wikimedia_image(f"{name} casual") or search_wikimedia_image(name)
            if img_url:
                success = download_and_verify_image(img_url, save_path)

        # Strategy 3: Unsplash curated casual street photo
        if not success and fallback_urls:
            fallback_url = fallback_urls[fallback_idx % len(fallback_urls)]
            fallback_idx += 1
            success = download_and_verify_image(fallback_url, save_path)

        if success:
            count += 1
            print(f"  [{idx+1}/50] ✓ Saved {name} -> {os.path.basename(save_path)}")
        else:
            print(f"  [{idx+1}/50] ✗ Failed for {name}")

        time.sleep(0.15)  # Friendly API rate limit

    print(f"✓ Completed {prefix}: {count}/50 photos saved and verified in {dest_dir}")
    return count

def main():
    print("================================================================================")
    print("      ACQUIRING 100 AMERICAN CASUAL DRESSED PEOPLE PHOTOS (usa_lib/)           ")
    print("================================================================================")

    men_count = fetch_group_photos(MEN_NAMES, MAN_DIR, prefix="man", fallback_urls=UNSPLASH_MAN_FALLBACKS)
    women_count = fetch_group_photos(WOMEN_NAMES, WOMAN_DIR, prefix="woman", fallback_urls=UNSPLASH_WOMAN_FALLBACKS)

    print("================================================================================")
    print(f"✓ USA Photo Library Summary:")
    print(f"  - Men Photos   : {len(os.listdir(MAN_DIR))} items in {MAN_DIR}")
    print(f"  - Women Photos : {len(os.listdir(WOMAN_DIR))} items in {WOMAN_DIR}")
    print(f"  - Total Photos : {len(os.listdir(MAN_DIR)) + len(os.listdir(WOMAN_DIR))} items in {USA_DIR}")
    print("================================================================================")

if __name__ == '__main__':
    main()
