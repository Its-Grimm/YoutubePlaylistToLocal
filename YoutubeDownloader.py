import os
import subprocess
from pytube import Playlist


def downloadAudioFile(audioFile, outputPath, fileName):
    cmd = [
        'yt-dlp',
        '-x',
        '--audio-format', 'mp3',
        '-o', os.path.join(outputPath, fileName),
        '-q',
        '--no-warnings',
        audioFile
        
    ]
    subprocess.run(cmd, check=True)
    

def getPlaylistsFromFile():
    try:
        with open('Playlists.txt', 'r') as playlistFile:
            allPlaylists = [line.strip() for line in playlistFile if 'playlist?' in line]
            if len(allPlaylists) == 0:
                print('No valid YouTube playlists found in the file.')
            return allPlaylists
    except Exception as e:
        print(f'Error: {e}')
        return []


def main(): 
    allPlaylists = getPlaylistsFromFile()
        
    outputPath = 'DownloadedMusic'
    os.makedirs(outputPath, exist_ok=True)
    
    playlistCount = 1
    for eachPlaylist in allPlaylists:
        try:
            p = Playlist(eachPlaylist)
            # Verify if any of the playlist will cause problems before continuing. p.title will error if problem with playlist
            _ = p.title
        except:
            print('Playlist has a problem with it. Please verify and try again')
            continue
        
        playlistTitle = str(p.title).replace(' ', '').replace('\'', '').replace('/', '')
        
        print(f'Downloading Playlist {playlistCount}/{len(allPlaylists)}')
        print('\n', playlistTitle, '\n')
        playlistCount += 1
        
        songOutputFolder = os.path.join(outputPath, playlistTitle)
        os.makedirs(songOutputFolder, exist_ok=True)
        
        count = 1
        for video in p.videos:
            print(f'{count}/{len(p)}: Downloading {video.title}')
            
            try:
                songName = f'{video.title}.mp3'
                fullSongName = os.path.join(songOutputFolder, songName)
                # Will simply overwrite song file if already exists/downloaded
                if not os.path.isfile(fullSongName):
                    downloadAudioFile(video.watch_url, songOutputFolder, songName)
                else:
                    print('Song already exists. Skipping...\n')
                    
            except Exception as e:
                print(f'Skipping {video.title} due to error: "{e}"\n')
            
            count += 1
                    
        print('\nAll files successfully downloaded!\n')

if __name__ == '__main__': 
    main()