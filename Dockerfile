FROM python:3.7.5-slim

COPY . /app
WORKDIR /app
RUN pip install \
      flask \
      boto3 \
      waitress

EXPOSE 5000
ENTRYPOINT ["waitress-serve"]
CMD ["--port=5000", "app:app"]
