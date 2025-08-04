# Mount static files directory for serving HTML and other static content only for testing purposes
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
def serve_quiz_page():
    with open("static/quiz.html", "r") as f:
        return f.read()