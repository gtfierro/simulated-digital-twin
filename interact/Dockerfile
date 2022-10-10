FROM python:3.9

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD . .
RUN chmod +x read-all-properties.sh
ENTRYPOINT ["tail", "-f", "/dev/null"]
