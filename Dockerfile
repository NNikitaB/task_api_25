FROM python:3.12.4-alpine
WORKDIR /internal
COPY .internal/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r /internal/requirements.txt
COPY .internal /internal/
COPY .test /test/
EXPOSE 8080
EXPOSE 5432
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
