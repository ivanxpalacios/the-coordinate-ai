FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN pip install uv && uv sync --frozen

COPY src ./src

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0"]
