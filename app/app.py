from typing import Union
from services.llm_service import LLMService
from fastapi import FastAPI
from .schemas import FormRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

@app.post("/form")
def read_form(form: FormRequest):
    llm=LLMService(session_id=form.session_id)
    return llm.start_form_filling(form)
