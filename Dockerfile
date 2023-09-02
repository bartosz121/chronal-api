FROM python:3.11.5-slim-bookworm as builder

ARG CHRONAL_ENVIRONMENT

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    # poetry
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR='/tmp/pypoetry' \
    POETRY_HOME='/opt/poetry' \
    # chronal-api
    CHRONAL_ENVIRONMENT=${CHRONAL_ENVIRONMENT}


RUN apt update \
    && apt install --no-install-recommends -y \
    build-essential gcc libsqlite3-dev \
    # Clean up
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U pip \
    && pip install "poetry==1.6.1"

COPY pyproject.toml poetry.lock ./

RUN echo "CHRONAL_ENVIRONMENT: ${CHRONAL_ENVIRONMENT}" \
    && poetry version \
    && poetry run pip install -U pip \
    && poetry install \
    $(if [ "$CHRONAL_ENVIRONMENT" = "production" ] ; then echo "--only main" ; fi) \
    --no-interaction --no-ansi --no-root \
    && rm -rf "$POETRY_CACHE_DIR"

COPY . ./

RUN poetry install --only-root --no-interaction --no-ansi \
    && rm -rf "$POETRY_CACHE_DIR"


FROM python:3.11.5-slim-bookworm as runtime

RUN apt update \
    && apt install --no-install-recommends -y \
    curl \
    # Clean up
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

ENV VIRUTAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRUTAL_ENV} ${VIRUTAL_ENV}

COPY --from=builder /app /app

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 CMD [ "poe", "healthcheck" ]

CMD ["poe", "serve"]