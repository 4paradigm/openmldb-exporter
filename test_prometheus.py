import argparse
import requests
import pytest


prom_url = 'http://127.0.0.1:9090'

# server is healthy itself
def test_prometheus_healthy():
    response = requests.get(f"{prom_url}/-/healthy")
    assert response.status_code == 200


def test_prometheus_targets():
    response = requests.get(f"{prom_url}/api/v1/targets")
    response_json = response.json()

    for target in response_json["data"]["activeTargets"]:
        assert target["health"] == "up"
