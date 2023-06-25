FROM python:3.10
WORKDIR /app
ADD . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["python", "seek.py", "-q", "Which dependencies does my application have?"]