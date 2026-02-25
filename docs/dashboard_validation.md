# OpenClaw 看板验证方法（第一阶段）

1. 打开 `agents/agents.json`，核对 9 个常驻主体均存在。
2. 打开 `skills/*/manifest.yaml`，核对每个主体技能已注册。
3. 执行 `python scripts/phase1_verify.py`，查看：
   - agents 列表
   - sandbox/workspace
   - 凭证检查
   - 时段判定
   - 最小连贯执行演示
4. 演示中需出现完整状态流转：
   `CREATED -> DISPATCHED -> ACKED -> RUNNING -> BLOCKED/SUCCEEDED -> VERIFIED -> SUMMARIZED`
