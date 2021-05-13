FROM python:3.5

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ocr.py ./
COPY test.py ./
COPY data/img_1.jpg ./data/
COPY piro2 ./piro2

CMD ./test.py
