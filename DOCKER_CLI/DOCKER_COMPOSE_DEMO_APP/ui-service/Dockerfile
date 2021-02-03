FROM python:3.8
WORKDIR /app
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app ./
ENV PORT 5000
ENV REVERT_SERVICE_PORT 5001
ENV REVERT_SERVICE_NAME text-revert-service
CMD ["python", "app.py"]