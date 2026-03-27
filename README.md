# test-jenkins

## 项目简介
一个极简 `pytest` 示例项目，主要用于验证 Jenkins CI 流程是否打通。

## 功能简介
- 运行 1 个简单测试用例
- 生成 `junit.xml` 与 `html` 测试报告
- Jenkins Pipeline 自动执行测试并归档报告
- 测试结束后通过飞书机器人发送通知

## 主要用途
仅用于测试流程，不追求业务复杂度。

## 本地运行
```bash
pip install -r requirements.txt
pytest
python scripts/notify_feishu.py
```

## Jenkins 使用说明
1. 在 Jenkins 中配置环境变量 `FEISHU_WEBHOOK`（飞书机器人 webhook）。
2. 使用仓库中的 `Jenkinsfile` 直接跑流水线。
3. 构建产物会归档到 `reports/`。

