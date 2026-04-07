from pydantic import BaseModel

class Observation(BaseModel):
    message: str

class Action(BaseModel):
    is_scam: bool
    scam_type: str
    explanation: str
    advice: str

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict