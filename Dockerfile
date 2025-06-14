# Dockerfile

# 1) Use official slim Python runtime
FROM python:3.12-slim

# 2) Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3) Set working directory
WORKDIR /app

# 4) (Optional) Install system dependencies if you need to compile extensions
# RUN apt-get update && apt-get install -y --no-install-recommends \
#      build-essential \
# && rm -rf /var/lib/apt/lists/*

# 5) Copy & install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6) Copy project code
COPY . .

# 7) Expose port 8000
EXPOSE 8000

# 8) Copy & prepare entrypoint script
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# 9) Use the script as the container's entrypoint
ENTRYPOINT ["./entrypoint.sh"]
