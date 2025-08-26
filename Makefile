.PHONY: build dev clean api client

build: 
	./setup.sh

clean:
	rm -rf .venv

api:
	cd ./api &&	fastapi dev main.py --port 8000

client:
	cd ./client && streamlit run 🏠_Home.py

dev:
	osascript -e 'tell app "Terminal" to do script "cd $(shell pwd) && source .venv/bin/activate && make api"'
	osascript -e 'tell app "Terminal" to do script "cd $(shell pwd) && source .venv/bin/activate && make client"'