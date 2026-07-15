FROM python:3.12-slim

WORKDIR /workspace
COPY lab/app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY lab /workspace/lab

EXPOSE 8000
CMD ["uvicorn", "lab.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

