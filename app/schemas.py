from pydantic import BaseModel

class FormRequest(BaseModel):
    form_key: str
    unique_id: str
    form_metadata: dict
    form_description: str
    session_id:str
