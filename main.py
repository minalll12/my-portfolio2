from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import cohere
import os

class chatRequest(BaseModel):
    prompt: str

class chatResponse(BaseModel):
    response: str

app = FastAPI()

load_dotenv()
API_KEY = os.getenv("API_KEY")

co = cohere.ClientV2(api_key=os.getenv("API_KEY"))

@app.get("/")
def health():
    return {"status": "Ok! This is working woohoo!"}

@app.post("/chat", response_model=chatResponse)
def chat(request: chatRequest):
    
    user_prompt = request.prompt
    
    response = co.chat(
        model="command-a-03-2025",
        messages=[{"role": "user", "content": user_prompt}],
    )

    final_response = response.message.content[0].text

    return chatResponse(response=f"Cohere said this: {final_response}")