FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable
ENV OPENAI_API_KEY=your_openai_api_key

CMD ["python", "fame.py"]