import random
from env.models import Observation, StepResult
from env.tasks import TASKS
from env.graders import grade

class ScamShieldEnv:

    def __init__(self):
        self.current_task = None
        self.done = False

    def reset(self):
        self.current_task = random.choice(TASKS)
        self.done = False
        return Observation(message=self.current_task["message"])

    def step(self, action):
        score, feedback = grade(self.current_task, action)
        self.done = True
        return StepResult(
            observation=Observation(message=self.current_task["message"]),
            reward=score,
            done=self.done,
            info={"feedback": feedback}
        )