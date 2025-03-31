install:
	cd backend && pip install -r requirements.txt
	cd desktop && npm install

start_desktop:
	cd desktop && npm run dev

start_backend:
	cd backend && python main.py
