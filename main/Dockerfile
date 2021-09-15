FROM pypy:3.7
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY run.sh .
COPY wsgi.py .
COPY api api

CMD [ "bash", "run.sh" ]
