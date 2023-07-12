FROM python:3.11-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . .
EXPOSE 8000
CMD ["gunicorn", "can_do.wsgi:application", "--bind", "0:8000"]
