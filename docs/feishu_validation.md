# 飞书验证方法

1. 在 `.env` 或 `secrets.yaml` 填入 `FEISHU_WEBHOOK`。
2. 运行：`python scripts/phase1_verify.py`。
3. 查看输出 `minimal_demo.feishu.sent`：
   - `true`：已推送。
   - `false`：输出真实原因（如凭证缺失）。
4. 飞书消息应包含：时段、三平台状态、task_id、timestamp。
