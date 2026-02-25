from runtime.minimal_demo import run_minimal_demo


def test_minimal_demo_contains_required_states():
    result = run_minimal_demo(feishu_webhook=None)
    flow = [item["status"] for item in result["status_flow"]]
    assert flow[:4] == ["CREATED", "DISPATCHED", "ACKED", "RUNNING"]
    assert flow[-2:] == ["VERIFIED", "SUMMARIZED"]
