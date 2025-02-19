FROM python:3.12.4
WORKDIR /internal
COPY internal/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r /internal/requirements.txt
COPY internal/ /internal/
RUN mkdir -p ./test/
COPY ./test /test
EXPOSE 8080
#CMD ["unicorn", "app", "--host", "0.0.0.0", "--port", "8080"]

