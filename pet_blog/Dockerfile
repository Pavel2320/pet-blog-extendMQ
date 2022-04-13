FROM python:3.9.2-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN mkdir /pet_blog_django
WORKDIR /pet_blog_django
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .