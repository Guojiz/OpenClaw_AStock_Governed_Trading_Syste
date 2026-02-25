# OpenClaw 能力对照（第一阶段）

## 1) OpenClaw 原生可直接使用
- 多智能体路由：以 `central` 统一调度常驻子代理。
- 多智能体沙箱：每个主体在 `agents/agents.json` 声明独立 sandbox。
- Skills 机制：各主体在 `skills/*/manifest.yaml` 注册技能。
- 子代理能力：后续通过 sessions_spawn 增补临时研究代理。
- 通道路由：Central -> TechOps/Executor/Comms 的业务链路已固定。

## 2) 需要在 Skill/业务层实现
- A 股交易时段状态机（已在 `runtime/session.py` 实现）。
- 凭证存在性检查与连通性自检（已在 `runtime/credentials.py` 与 `runtime/minimal_demo.py` 实现）。
- 任务状态机与证据链（已在 `runtime/models.py` 与 `runtime/minimal_demo.py` 实现）。
- 飞书按时段模板渲染（已在 `runtime/feishu.py` 实现）。
- BigQuant/iFinD 真实 SDK 登录适配（当前为凭证驱动的自检占位）。

## 3) 本项目映射方式
- 制度层主体：`Central / Qwen党 / DeepSeek党` 仅做展示与治理。
- 工程层主体：`central + 8 个常驻子代理` 完整落地于 `agents/agents.json`。
- 执行闭环：`Central创建任务 -> 派发TechOps -> 自检回执 -> 汇总 -> 飞书播报`。
- 审计可追溯：每个任务保留状态流转与证据数组，支持后续落盘到 `state/`。
