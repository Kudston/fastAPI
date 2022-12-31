FROM python:3.9.7

WORKDIR /usr/src/myapp

COPY blogapp/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "blogapp.blogapi:app", "--host", "*", "--port", "8000"]
