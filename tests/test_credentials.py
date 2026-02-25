from runtime.credentials import credential_presence_report


def test_credential_presence_report_has_required_keys():
    report = credential_presence_report()
    assert set(report.keys()) == {"bigquant", "ifind_qwen", "ifind_deepseek", "feishu_webhook"}
