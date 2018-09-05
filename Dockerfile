FROM python:3-onbuild
COPY . /web
WORKDIR /web
RUN pip install -r ./requirements.txt
CMD ["python","app.py"]
