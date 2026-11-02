# FindIt – Campus Lost & Found Management System

FindIt is a beginner-friendly web application for reporting lost and found items around a college campus.

## Features
- Report a lost item.
- Report a found item.
- View recent reports and summary counts.
- Search by item name, category or location.
- Filter reports by Lost or Found.
- Mark an item as returned.
- Health-check endpoint at `/health`.

## Technology
- Python and Flask
- HTML and CSS
- SQLite database
- Docker

## Run locally on Windows

1. Install Python 3.10 or newer.
2. Open PowerShell in this project folder.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the application:

   ```powershell
   python app.py
   ```

6. Open `http://127.0.0.1:5000` in your browser.

The SQLite database is created automatically in the `instance` folder.

## Run with Docker

Build the image:

```powershell
docker build -t findit:1.0 .
```

Run the container:

```powershell
docker run --name findit-app -p 5000:5000 findit:1.0
```

Open `http://localhost:5000`.

To stop the container:

```powershell
docker stop findit-app
```

To remove it:

```powershell
docker rm findit-app
```

> Note: This starter version stores data in a local SQLite database. In a Kubernetes deployment, container-local data can be lost when a Pod is replaced. For this introductory assignment, use one replica and treat the data as demonstration data. Persistent storage can be added later if required.

## Project structure

```text
FindIt_Campus_Lost_and_Found/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_app.py
```
