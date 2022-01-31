from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

import solver

app = FastAPI()

class Guess(BaseModel):
    word: str    # example: WRECK
    colors: str  # example: W?.?.

@app.get("/")
def read_root():
    return {'see docs at': 'https://github.com/shoreofwonder/wordly'}

@app.post('/words')
def post_guesses(guesses: list[Guess]):
    return solver.solve(guesses)
