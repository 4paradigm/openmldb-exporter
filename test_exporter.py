from sqlalchemy import engine
import argparse
import requests
import pytest

from prometheus_client.parser import text_string_to_metric_families

def pytest_addoption(parser):
    parser.addoption("--zk_root",
                        type=str,
                        action="store",
                        default="openmldb-zk:2181",
                        help="endpoint to zookeeper")
    parser.addoption("--zk_path",
                        type=str,
                        action="store",
                        default="/openmldb",
                        help="root path in zookeeper for OpenMLDB")
    parser.addoption("--url",
                        type=str,
                        action="store",
                        default="http://openmldb-exporter:8000/metrics",
                        help="openmldb exporter pull url")


@pytest.fixture(scope="session")
def global_url(request):
    zk_root = request.config.getoption("--zk_root")
    zk_path = request.config.getoption("--zk_path")

    eng = engine.create_engine(f"openmldb:///?zk={zk_root}&zkPath={zk_path}")
    conn = eng.connect()
    # default online mode
    conn.execute("set session execute_mode = 'online'")
    # enable deploy response time
    conn.execute("set global deploy_stats = 'on'")
    return request.config.getoption("--url")


def test_components_online(global_url):
    # Make a request to your application to get the Prometheus metrics
    response = requests.get(global_url)

    # Parse the metrics from the response
    metrics = text_string_to_metric_families(response.text)

    ns_cnt = 0
    tb_cnt = 0
    # Assert that the metrics are as expected
    for metric in metrics:
        # all components online
        if metric.name == "openmldb_status":
            for sample in metric.samples:
                if sample.value == 1.0:
                    if sample.labels["role"] == "nameserver":
                        ns_cnt += 1
                    elif sample.labels["role"] == "tablet":
                        tb_cnt += 1

                    assert sample.labels["openmldb_status"] == "online"

    assert ns_cnt == 2
    assert tb_cnt == 3
