# OpenClaw_AStock_Governed_Trading_System

第一阶段目标：完成 OpenClaw 多智能体“验活”，确保不是口头流程。

## 快速开始

```bash
python -m pip install -e '.[dev]'
python scripts/phase1_verify.py
pytest -q
```

## 已落地能力
- 9 个常驻子代理注册
- 全量技能清单注册
- A 股交易时段状态机
- 凭证存在性检查（`.env`/`secrets.yaml`）
- 最小连贯执行闭环（含 task_id、状态流转、证据链、飞书发送链路）

## 凭证说明
- 请复制 `secrets.example.yaml` 为 `secrets.yaml`。
- 禁止提交真实凭证，仓库已通过 `.gitignore` 屏蔽。
