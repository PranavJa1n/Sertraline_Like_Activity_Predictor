FROM python:3.13
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir \
    --timeout 120 \
    --retries 10 \
    --resume-retries 10 \
    -r requirements.txt
    
COPY . .

EXPOSE 8000

RUN useradd app
USER app

CMD ["python", "app.py"]