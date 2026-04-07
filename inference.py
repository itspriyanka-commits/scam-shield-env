import os
import json
from openai import OpenAI
from env.environment import ScamShieldEnv
from env.models import Action

API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

def get_model_output(message):
    prompt = f"""
    Analyze this message and return ONLY a JSON object with these fields:
    - is_scam: true or false
    - scam_type: one of [lottery, phishing, impersonation, vishing, upi_fraud, fake_customs, normal]
    - explanation: why this is or is not a scam (mention words like urgent, link, reward, verify, bank if applicable)
    - advice: what the user should do (mention do not click, official, contact, do not share, ignore if applicable)

    Message: "{message}"

    Return ONLY valid JSON. No extra text.
    """

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content


def parse_output(raw_text):
    try:
        clean = raw_text.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean)
        return Action(
            is_scam=data["is_scam"],
            scam_type=data["scam_type"],
            explanation=data["explanation"],
            advice=data["advice"]
        )
    except Exception as e:
        print(f"Parsing error: {e}")
        return Action(
            is_scam=True,
            scam_type="unknown",
            explanation="suspicious message contains urgent request",
            advice="do not click any link and contact official support"
        )


def main():
    env = ScamShieldEnv()
    total_reward = 0
    episodes = 5

    print("=" * 50)
    print("   SCAM SHIELD AI - RUNNING")
    print("=" * 50)

    for i in range(episodes):
        obs = env.reset()
        message = obs.message

        print(f"\nEpisode {i+1}")
        print(f"Message : {message}")

        raw = get_model_output(message)
        action = parse_output(raw)

        print(f"Is Scam : {action.is_scam}")
        print(f"Type    : {action.scam_type}")
        print(f"Reason  : {action.explanation}")
        print(f"Advice  : {action.advice}")

        result = env.step(action)
        total_reward += result.reward

        print(f"Score   : {result.reward:.2f}")
        if result.info["feedback"]:
            print(f"Feedback: {result.info['feedback']}")
        print("-" * 50)

    print(f"\nFinal Average Score: {total_reward/episodes:.2f} / 1.00")
    print("=" * 50)


if __name__ == "__main__":
    main()