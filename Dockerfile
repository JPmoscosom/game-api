FROM python:3.12
WORKDIR /Gravity
COPY . /Gravity
COPY requeriments.txt .
COPY .env .
COPY . /models
COPY . /routes
RUN pip install gunicorn blinker build click colorama Flask itsdangerous Jinja2 MarkupSafe packaging psycopg2-binary pyproject_hooks python-decouple python-dotenv Werkzeug
EXPOSE 443
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app