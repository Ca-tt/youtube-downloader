.PHONY: run clean removetoken

clean:
	rm build dist -rf

removetoken:
	rm ~/tokens.json

build:
	pyinstaller --clean --noconsole --onefile --name "YouTube Downloader" --icon=assets/youtube-icon.ico src/main.py  

