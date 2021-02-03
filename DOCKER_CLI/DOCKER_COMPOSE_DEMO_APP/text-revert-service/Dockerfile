FROM python:3.8
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app ./
ENV PORT 5001
CMD ["python", "api.py"]