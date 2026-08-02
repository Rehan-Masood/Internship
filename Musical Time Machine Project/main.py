import requests
from bs4 import BeautifulSoup

def main():
    print("=" * 50)
    print("      🎵 MUSICAL TIME MACHINE GENERATOR 🎵      ")
    print("=" * 50)

    # 1. Get user input
    date_input = input("\nWhich year do you want to travel to? Type the date in format YYYY-MM-DD: ").strip()

    # 2. Scrape Billboard Hot 100
    url = f"https://www.billboard.com/charts/hot-100/{date_input}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"\nFetching Billboard Hot 100 for {date_input}...")
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error: Unable to fetch Billboard data (Status Code: {response.status_code}). Check the date format.")
        return

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract song titles from Billboard chart
    song_tags = soup.select("li ul li h3#title-of-a-story")
    song_titles = [song.get_text().strip() for song in song_tags]

    if not song_titles:
        print("❌ Could not find any songs. Billboard page structure might have changed or date is invalid.")
        return

    print(f"✅ Successfully scraped {len(song_titles)} songs from Billboard Hot 100!")

    # 3. Save songs with Spotify Search Links to a text file
    filename = f"playlist_{date_input}.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"=========================================\n")
        file.write(f"   BILLBOARD HOT 100 - {date_input}\n")
        file.write(f"=========================================\n\n")

        for index, song in enumerate(song_titles, 1):
            # Encode spaces for URL formatting
            search_query = song.replace(" ", "%20")
            spotify_link = f"https://open.spotify.com/search/{search_query}"
            
            file.write(f"{index}. {song}\n")
            file.write(f"   Listen: {spotify_link}\n\n")

    print(f"\n🎉 Done! Created '{filename}' in your project directory.")
    print(f"📂 Open '{filename}' to view all 100 songs with clickable Spotify links!")

if __name__ == "__main__":
    main()