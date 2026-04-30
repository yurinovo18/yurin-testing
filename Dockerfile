FROM python:3.12-slim AS build
WORKDIR /app
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils patchelf scons gcc libc6-dev \
    && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir pyinstaller staticx \
    && pyinstaller --onefile --name calc --paths src src/calculator/cli.py \
    && staticx /app/dist/calc /app/dist/calc-static \
    && strip /app/dist/calc-static \
    && mkdir -p /empty-tmp

FROM scratch
COPY --from=build /empty-tmp /tmp
COPY --from=build /app/dist/calc-static /calc
ENTRYPOINT ["/calc"]
CMD ["--help"]
