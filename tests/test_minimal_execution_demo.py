from runtime.minimal_demo import run_minimal_demo


def test_minimal_execution_demo_has_evidence():
    result = run_minimal_demo(feishu_webhook=None)
    assert result["task_id"].startswith("task-")
    assert len(result["evidence"]) >= 3
