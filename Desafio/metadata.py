import eyed3
audiofile = eyed3.load("Manowar  Warriors of the Worlds.mp3")
print(audiofile.tag.artist)
print(audiofile.tag.album)
print(audiofile.tag.album_artist)
print(audiofile.tag.title)
print(audiofile.tag.track_num)
# pytaglib