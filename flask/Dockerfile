FROM python:3.9

WORKDIR /app

COPY ./flask/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#COPY ./flask/app /app

CMD ["python","-u","main.py"]