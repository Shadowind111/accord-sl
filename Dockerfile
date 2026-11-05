FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements-full.txt requirements.txt ./
RUN pip install --no-cache-dir --index-url https://pypi.tuna.tsinghua.edu.cn/simple -r requirements-full.txt
COPY . .
EXPOSE 7860
CMD ["python", "app.py"]
