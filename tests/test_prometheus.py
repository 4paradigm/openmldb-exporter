import requests


# server is healthy itself
def test_prometheus_healthy(prom_url):
    response = requests.get(f"{prom_url}/-/healthy")
    assert response.status_code == 200


def test_prometheus_targets(prom_url):
    response = requests.get(f"{prom_url}/api/v1/targets")
    response_json = response.json()

    for target in response_json["data"]["activeTargets"]:
        assert target["health"] == "up", f"Target is {target}"
