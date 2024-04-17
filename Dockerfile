FROM python:3.11-alpine

WORKDIR /app

#ENV DEBUG=False
ENV PROD=True

COPY requirements.txt .

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install gunicorn

COPY . .

EXPOSE 8000

ENTRYPOINT ["gunicorn", "-w", "3", "-b", ":8000", "config.wsgi:application"]
