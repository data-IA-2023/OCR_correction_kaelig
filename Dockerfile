FROM python:3.9.5-slim
ENV PYHTONUNBUFFERED=1
RUN apt-get update && apt-get -y install zbar-tools tesseract-ocr imagemagick
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["uvicorn", "controler:app", "--port", "3000", "--host", "0.0.0.0"]