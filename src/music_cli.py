import json

def load_data(filename):
    """Load song and playlist data from a JSON file."""
    with open(filename, 'r') as file:
        return json.load(file)

def print_songs_in_playlist(playlist, songs):
    """Print songs in the selected playlist."""
    print(f"\nPlaylist: {playlist['name']}\nDescription: {playlist['description']}\n")
    print("Songs:")
    for song_id in playlist['song_ids']:
        song = next((s for s in songs if s['id'] == song_id), None)
        if song:
            print(f"- {song['title']} by {song['artist']} ({song['category']})")

def main():
    """Main CLI application function."""
    data = load_data('../data/MusicCollection.json')
    songs = data['songs']
    playlists = data['playlists']

    print("Welcome to the Music CLI App!")
    print("Available Playlists:")
    
    # List available playlists
    for playlist in playlists:
        print(f"{playlist['id']}: {playlist['name']}")

    while True:
        try:
            selected_playlist_id = int(input("\nSelect a playlist by ID (or type 0 to exit): "))
            if selected_playlist_id == 0:
                print("Exiting the Music CLI App. Goodbye!")
                break
            playlist = next((p for p in playlists if p['id'] == selected_playlist_id), None)
            if playlist:
                print_songs_in_playlist(playlist, songs)
            else:
                print("Playlist not found.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()