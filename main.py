from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import Query
from google import genai
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# create FastAPI app instance
app = FastAPI()

# Mount static files directory for serving HTML and other static content only for testing purposes
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/", response_class=HTMLResponse)
def serve_quiz_page():
    with open("static/quiz.html", "r") as f:
        return f.read()
    
# Initialize Google GenAI client
# Make sure to set your API key in the environment variable or replace it with your actual API
client = genai.Client(api_key="API_KEY")


# Define the Question model
class Question(BaseModel):
    id: int
    question: str
    choices: list[str]
    answer: int = None

# In-memory database to store questions
questions_db = []

@app.get("/questions/")
def create_question(topic: str = "General Knowledge"):
    prompt = (
        f"Generate 5 multiple choice questions about {topic}. "
        "For each question, provide a JSON object with the following format: "
        '{"question": "...", "choices": ["...", "...", "...", "..."], "answer": <correct_choice_index note:index should be 0-based>} '
        "Return a JSON array of these objects."
    )
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': list[Question],
        },
    )
    questions = response.parsed
    for idx, q in enumerate(questions):
        q.id = idx
    global questions_db
    questions_db = [q if isinstance(q, Question) else Question(**q) for q in questions]
    # # Remove the answer field before returning to client
    # questions_no_answer = [
    #     {**q.model_dump(), "answer": None} for q in questions_db
    # ]
    # return questions_no_answer
    return questions_db


@app.post('/check_answers/')
def check_answers(answers: list[dict]):
    results = []
    score = 0
    for item in answers:
        qid = item.get('id')
        user_answer = item.get('answer')
        if qid is not None and 0 <= qid < len(questions_db):
            correct_answer = questions_db[qid].answer
            is_correct = correct_answer == user_answer
            results.append({
                "id": qid,
                "correct": is_correct
            })
            if is_correct:
                score += 1
        else:
            results.append({
                "id": qid,
                "error": "Question not found"
            })
    return {"results": results, "score": score}