FROM golang:1.20-bullseye

WORKDIR /opt/test/

COPY test/ ./

RUN go mod download && go mod verify

RUN go build -v -o ./prometheus_cfg_hook cmd/prometheus_config_hook.go

ENTRYPOINT [ "/opt/test/prometheus_cfg_hook" ]
