FROM python:3.9

# Path: /app
WORKDIR /app

# Path: /app/requirements.txt
COPY requirements.txt .

# Path: /app
RUN pip install -r requirements.txt

# Path: /app
COPY /dataportal .

#EXpose port 8000
EXPOSE 8000

# Path: /app
WORKDIR /app

#Start the django server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
