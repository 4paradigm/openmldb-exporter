from sqlalchemy import engine
import argparse
import requests
import pytest

from prometheus_client.parser import text_string_to_metric_families


@pytest.fixture(scope="session")
def global_url():
    parser = argparse.ArgumentParser(
        description="OpenMLDB exporter integration test")
    parser.add_argument("--zk_root",
                        type=str,
                        default="openmldb-zk:2181",
                        help="endpoint to zookeeper")
    parser.add_argument("--zk_path",
                        type=str,
                        default="/openmldb",
                        help="root path in zookeeper for OpenMLDB")
    parser.add_argument("--url",
                        type=str,
                        default="http://openmldb-exporter:8000/metrics",
                        help="openmldb exporter pull url")
    args = parser.parse_args()
    zk_root = args.zk_root
    zk_path = args.zk_path

    eng = engine.create_engine(f"openmldb:///?zk={zk_root}&zkPath={zk_path}")
    conn = eng.connect()
    # default online mode
    conn.execute("set session execute_mode = 'online'")
    # enable deploy response time
    conn.execute("set global deploy_stats = 'on'")
    return args.url


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
