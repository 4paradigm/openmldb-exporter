FROM debian:bullseye

RUN apt-get update && apt-get install -y python3-pip && \
    pip3 install --no-cache-dir openmldb-exporter==0.6.0 && \
    apt-get clean

ENV OPENMLDB_EXPORTER_VERSION=0.6.0
EXPOSE 8000

# --config.zk_root and --config.zk_path must provided by user
ENTRYPOINT [ "/usr/local/bin/openmldb-exporter", "--log.level=INFO" ]
