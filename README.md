# AI Scam Shield 🛡️

## What is this?
An AI system that detects scam messages and protects users — especially in India.

## Problem
Every day thousands of Indians lose money to scams via SMS, WhatsApp, and calls.
Most people cannot identify if a message is a scam or not.

## Solution
ScamShield uses AI to:
- Detect if a message is a scam
- Identify the type of scam
- Explain why it is a scam
- Give safety advice to the user

## Scam Types Covered
- Phishing
- Lottery fraud
- UPI fraud
- Job fraud
- Fake customs
- Impersonation (bank, CBI, TRAI)
- Vishing (voice/call scams)

## Difficulty Levels
- Easy: Obvious scams with clear red flags
- Medium: Realistic scams with local context
- Hard: Highly convincing personalized scams

## Scoring
- Detection: 0.4
- Scam Type: 0.2
- Explanation: 0.2
- Advice: 0.2
- Total: 1.0

## How to Run

### Install dependencies
pip install pydantic openai

### Set environment variables
$env:OPENAI_API_KEY="your_groq_key"
$env:API_BASE_URL="https://api.groq.com/openai/v1"
$env:MODEL_NAME="llama-3.3-70b-versatile"

### Run
python inference.py

## Real World Applications
- WhatsApp scam detection bot
- SMS filter for Android
- Browser extension for phishing links
- Bank alert system for customers
- Senior citizen protection tool

## Tech Stack
- Python
- Groq AI (llama-3.3-70b-versatile)
- Pydantic
- OpenEnv framework