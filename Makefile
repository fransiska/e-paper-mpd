install:
	cp epaperShowSong.service /etc/systemd/system/
	chmod 664 /etc/systemd/system/epaperShowSong.service
	systemctl enable epaperShowSong
	systemctl restart epaperShowSong
