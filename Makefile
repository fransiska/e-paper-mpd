init:
	pip3 install -r requirements.txt

install:
	cp epaperShowSong.service /etc/systemd/system/
	chmod 664 /etc/systemd/system/epaperShowSong.service
	systemctl enable epaperShowSong
	systemctl restart epaperShowSong

run:
	python3 main.py

.PHONY: init install run
