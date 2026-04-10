FROM python:3.11-slim

# Create a user with UID 1000 for Hugging Face compatibility
RUN useradd -m -u 1000 user

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Grant permissions mapping to the new user before switching context
RUN chown -R user:user /app
USER user

EXPOSE 7860

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
