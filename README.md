# Installation

### Create a virtual environment
` python -m venv venv `

- Linux:
` source venv/bin/activate`

- Windows: `.\venv\Scripts\activate.bat`

### Install FastAPI
`pip install fastapi uvicorn`
`pip install -q -U google-genai`

### Start Server
`uvicorn main:app --reload --port 8000`

-website will be available at `http://localhost:8000`

