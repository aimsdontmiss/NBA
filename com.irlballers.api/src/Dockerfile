FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

# RUN python manage.py makemigrations 
# RUN python manage.py migrate        


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]

