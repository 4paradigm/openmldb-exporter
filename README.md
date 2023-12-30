# OpenMLDB Exporter

[![PyPI](https://img.shields.io/pypi/v/openmldb-exporter?label=openmldb-exporter)](https://pypi.org/project/openmldb-exporter/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openmldb-exporter)

## Features

- [OpenMLDB](https://github.com/4paradigm/OpenMLDB) Prometheus Exporter exposing metrics
- [OpenMLDB](https://github.com/4paradigm/OpenMLDB) mixin provides well-configured examples for [Prometheus](https://prometheus.io/) server and [Grafana](https://grafana.com/) dashboard

## Requirements

- A runnable OpenMLDB instance that is accessible from your network
- OpenMLDB version >= 0.5.0
- Python >= 3.8


## Quick Start

**You can run openmdlb-exporter from docker, or install and run directly from PyPI.**

<details open=true><summary>Use docker</summary>

```sh
docker run ghcr.io/4paradigm/openmldb-exporter \
    --config.zk_root=<openmldb_zk_addr> \
    --config.zk_path=<openmldb_zk_path>
```

</details>

<details open=true><summary>Install and Run from PyPI</summary>

```sh
pip install openmldb-exporter

# start
openmldb-exporter \
    --config.zk_root=<openmldb_zk_addr> \
    --config.zk_path=<openmldb_zk_path>
```
</details></br>

And replace `<openmdlb_zk_addr>` and `<openmldb_zk_path>` to correct value. Afterwards, you can check metrics with curl:

```sh
curl http://<IP>:8000/metrics
```
`<IP>` is docker container IP, or `127.0.0.1` if installing from PyPI.

<details><summary>Example output</summary>

```sh
# HELP openmldb_connected_seconds_total duration for a component conncted time in seconds                              
# TYPE openmldb_connected_seconds_total counter                                                                        
openmldb_connected_seconds_total{endpoint="172.17.0.15:9520",role="tablet"} 208834.70900011063                         
openmldb_connected_seconds_total{endpoint="172.17.0.15:9521",role="tablet"} 208834.70700001717                         
openmldb_connected_seconds_total{endpoint="172.17.0.15:9522",role="tablet"} 208834.71399998665                         
openmldb_connected_seconds_total{endpoint="172.17.0.15:9622",role="nameserver"} 208833.70000004768                     
openmldb_connected_seconds_total{endpoint="172.17.0.15:9623",role="nameserver"} 208831.70900011063                     
openmldb_connected_seconds_total{endpoint="172.17.0.15:9624",role="nameserver"} 208829.7230000496                      
# HELP openmldb_connected_seconds_created duration for a component conncted time in seconds                            
# TYPE openmldb_connected_seconds_created gauge                                                                        
openmldb_connected_seconds_created{endpoint="172.17.0.15:9520",role="tablet"} 1.6501813860467942e+09                   
openmldb_connected_seconds_created{endpoint="172.17.0.15:9521",role="tablet"} 1.6501813860495396e+09                   
openmldb_connected_seconds_created{endpoint="172.17.0.15:9522",role="tablet"} 1.650181386050323e+09                    
openmldb_connected_seconds_created{endpoint="172.17.0.15:9622",role="nameserver"} 1.6501813860512116e+09               
openmldb_connected_seconds_created{endpoint="172.17.0.15:9623",role="nameserver"} 1.650181386051238e+09                
openmldb_connected_seconds_created{endpoint="172.17.0.15:9624",role="nameserver"} 1.6501813860512598e+09               
```

</details>

## Configuration

You can view the help from:
```sh
openmldb-exporter -h
```
`--config.zk_root` and `--config.zk_path` are mandatory.

<details><summary>Available options</summary>

```
usage: openmldb-exporter [-h] [--log.level LOG.LEVEL] [--web.listen-address WEB.LISTEN_ADDRESS]
                        [--web.telemetry-path WEB.TELEMETRY_PATH] [--config.zk_root CONFIG.ZK_ROOT]
                        [--config.zk_path CONFIG.ZK_PATH] [--config.interval CONFIG.INTERVAL]

OpenMLDB exporter

optional arguments:
 -h, --help            show this help message and exit
 --log.level LOG.LEVEL
                       config log level, default WARN
 --web.listen-address WEB.LISTEN_ADDRESS
                       process listen port, default 8000
 --web.telemetry-path WEB.TELEMETRY_PATH
                       Path under which to expose metrics, default metrics
 --config.zk_root CONFIG.ZK_ROOT
                       endpoint to zookeeper, default 127.0.0.1:6181
 --config.zk_path CONFIG.ZK_PATH
                       root path in zookeeper for OpenMLDB, default /
 --config.interval CONFIG.INTERVAL
                       interval in seconds to pull metrics periodically, default 30.0
```

</details>

## Development

### Extra Requirements

- Same in [Requirements](#requirements)
- [poetry](https://github.com/python-poetry/poetry) as build tool

### Run

1. Setup python dependencies:

   ```sh
   poetry install
   ```

2. Start openmldb exporter

   ```sh
   poetry run openmldb-exporter
   ```

   Pass in necessary flags after `openmldb-exporter`. Run `poetry run openmldb-exporter --help` to get the help info.


## Compatibility

| [OpenMLDB Exporter version](https://grafana.com/grafana/dashboards/17843-openmldb-dashboard/?tab=revisions) | [OpenMLDB supported version](https://github.com/4paradigm/OpenMLDB/releases) | [Grafana Dashboard revision](https://grafana.com/grafana/dashboards/17843-openmldb-dashboard/?tab=revisions) | Explaination |
| ---- | ---- | ---- | ------- |
| >= 0.9.0 | >= 0.8.4 | >=4 | OpenMLDB removed deploy response time in database since 0.8.4 |
| < 0.9.0  | >= 0.5.0, < 0.8.4 | 3 | |


## Release History

- 0.9.0
    * Features
      - **BREAKING** support OpenMLDB 0.8.4. OpenMLDB 0.8.4 removed deploy response time, please use openmldb-exporter >= 0.9.0. Ref [Compatibility](#compatibility) info above
      - **BREAKING** update grafana dashboard config, use the latest revision (4 or later) if you upgrade OpenMLDB cluster >=0.8.4. For legacy OpenMLDB <= 0.8.3, select [revison 3](https://grafana.com/api/dashboards/17843/revisions/3/download). You can also download corresponding Grafana dashboard from Github Release asserts
    * Tests
      - Remove deploy response time related tests
    * Chores
      - update deps
      - add CI jobs

- 0.8.2
    * Chores
      - deps: restrict OpenMLDB version < 0.8.4

- 0.8.1
    * Features
      - update openmldb-exporter docker image
    * Chores
      - doc and workflow updates

- 0.8.0
    * Features
        - Upgrade OpenMLDB SDK to v0.8
        - improve test code

- 0.7.1
    * Features
        - Upgrade OpenMLDB SDK to v0.7
        - Upgrade prometheus client to 0.16
- 0.6.0
    * Features
        - Depends on OpenMLDB SDK v0.6
