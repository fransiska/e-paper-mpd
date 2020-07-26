# e-Paper MPD

Display MPD information on Waveshare e-ink display.

Currently using python 3.7.3.

Files in `waveshare_epd` are from [waveshare](https://github.com/waveshare/e-Paper)

## Running

To use with different host:

```bash
sudo MPDHOST="raspberrypi.local" python3 main.py

# without sudo
export MPDHOST="raspberrypi.local"
python3 main.py
```

or just 

```bash
make run
```

## Install Service

Assuming this repository is located at `/home/pi/Git/e-paper-mpd`

```bash
sudo make install
```

## MPD Cheatsheet

### Reset MPD

1. Set MPD's root folder `/etc/mpd.conf` change `music_directory`
2. Remove database `sudo rm /var/lib/mpd/tag_cache` and playlist `sudo rm /var/lib/mpd/playlists/*`
3. Reboot
4. Upon starting MPD will start rescanning the folder `music_directory`. It doesn't seem to take much CPU even on raspberry zero. But it will take a long long time if the directory is large.

### Playlist vs Files

- To queue `m3u8` playlist, the playlist `m3u8` file itself have to be inside the `music_directory` but the path of the files inside the playlist can be absolute path and does not have to be inside `music_directory`. Play playlist using `mpc load playlist.m3u8`
- To queue files in a folder, use `mpc add folder_name`. The files have to be inside `music_directory`, ie. listable by `mpc ls`.
