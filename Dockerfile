FROM python:alpine3.7
RUN pip install pipenv gunicorn
RUN adduser -D glue
RUN mkdir /app
COPY Pipfile* /app/
WORKDIR /app
RUN chown -R glue /app
RUN pipenv lock --requirements > requirements.txt && \
      pip install -r requirements.txt
USER glue
CMD gunicorn --bind 0.0.0.0:5000 wsgi:app
COPY glue.py wsgi.py /app/
EXPOSE 5000
