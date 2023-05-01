FROM golang:1.20-bullseye AS building

WORKDIR /opt/test/

COPY test/ ./

RUN go mod download && go mod verify && \
    go build -v -o ./prometheus_cfg_hook prometheus_config_hook.go

FROM debian:bullseye-slim

WORKDIR /usr/local/bin

COPY --from=building /opt/test/prometheus_cfg_hook .

ENTRYPOINT [ "/usr/local/bin/prometheus_cfg_hook" ]
