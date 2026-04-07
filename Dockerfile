FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV API_BASE_URL=https://api.groq.com/openai/v1
ENV MODEL_NAME=llama-3.3-70b-versatile

CMD ["python", "inference.py"]