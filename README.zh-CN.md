# NoteForge

[English](README.md) | [简体中文](README.zh-CN.md)

**从主题或文档生成证据边界清晰的研究报告。**

NoteForge 将研究主题或本地文档整理为结构化 Markdown 报告。它会明确区分检索元数据、源文档事实、模型推断、模拟记录与告警，让读者能够判断报告中的内容基于什么产生。

> NoteForge 用于辅助研究准备；它不提供全文核验，不保证引用准确性，不能替代权威政策审查，也不是经过加固的多租户研究平台。

## 主要能力

- 提供可安装的 Python 包、强类型 SDK 与统一 CLI。
- 通过 CLI、TUI、HTTP API 或 Docker 分析主题和文档。
- 无需 API Key 即可从 Crossref 获取真实学术元数据。
- 离线与模拟模式必须显式选择，且不会被冒充为检索证据。
- Job 中保存可检查的语义阶段状态、来源、告警和 Markdown 报告。
- 对已持久化的 v0.2 Job 提供事务式迁移。

所有入口都调用同一套 `AnalysisRequest` 与 `run_job` 管线：

```text
主题或文档
    -> 文档解析
    -> 关键词提取
    -> 文献检索
    -> 综合分析
    -> 技术案例与政策评估
    -> report.md
```

## 快速开始

NoteForge 支持 Python 3.10–3.13。核心 SDK 与 CLI 没有必需的第三方依赖。

```bash
python -m pip install .

# 可复现的离线演示
noteforge run --topic "evidence-aware research" --provider mock --job-id demo

# 获取真实 Crossref 元数据
noteforge run --topic "transformer model evaluation" --provider crossref

# 分析本地文档
noteforge run --file ./examples/sample_paper_abstract.md --provider crossref

noteforge report demo
```

按需安装 API 接口和文档解析器：

```bash
python -m pip install ".[api]"
python -m pip install ".[documents]"
```

## 选择使用入口

| 入口 | 用途 | 开始命令 |
| --- | --- | --- |
| CLI | 运行、恢复、检查和迁移 Job | `noteforge --help` |
| Python SDK | 在 Python 代码中集成强类型管线 | `from noteforge import AnalysisRequest, run_job` |
| TUI | 在终端中交互使用管线 | `noteforge tui` |
| HTTP API | 通过 API v1 提交并轮询 Job | `noteforge api` |
| Docker | 使用可复现镜像运行 API | `docker compose up -d --build` |

## Python SDK

```python
from pathlib import Path

from noteforge import AnalysisRequest, run_job

result = run_job(
    AnalysisRequest(
        topic="LLM deployment evaluation",
        provider="mock",
        job_id="sdk-demo",
    ),
    output_root=Path("outputs"),
)

print(result.status, result.report_path)
print(result.sources, result.warnings)
```

`AnalysisRequest`、`JobResult`、文献/来源/案例/政策记录、状态模型、枚举和结构化错误均采用标准库 dataclass。`LiteratureProvider.search(LiteratureQuery)` 是稳定的 Provider 扩展契约。

## 证据模式

| Provider | 数据来源 | 网络 | 证据用途 | 失败行为 |
| --- | --- | --- | --- | --- |
| `crossref` | Crossref REST 元数据 | 需要 | 应通过 DOI 或出版方继续核验的元数据 | 返回空结果并显示告警 |
| `mock` | 确定性的本地测试数据 | 不需要 | 仅用于演示和测试 | 始终标记为 `simulated` |
| `llm-simulated` | 模型生成的演示记录 | LLM 端点 | 仅用于演示 | 始终保持明确的模拟标记 |

Crossref 是默认 Provider。真实 Provider 故障不会自动回退到模拟数据。获取元数据不等于阅读或核验论文全文。

## Job 与迁移

规范 Job 产物保存在 `outputs/jobs/{job_id}/`：

```text
task_state.json
context_data.json
resume_log.txt
report.md
```

v0.3 删除了旧根目录脚本、`core/tasks/utils` 导入路径和 requirements 文件。已有 v0.2 Job 会在首次读取时进行备份与事务式迁移，也可以提前执行：

```bash
noteforge jobs migrate --all
```

兼容细节见 [v0.3 迁移指南](docs/migration_v0.3.md)。

## API 与 Docker

```bash
python -m pip install ".[api]"
noteforge api --host 0.0.0.0 --port 8000
```

```bash
curl -X POST http://localhost:8000/api/v1/jobs/submit \
  -F "topic=AI safety" -F "provider=crossref"
curl http://localhost:8000/api/v1/jobs/status/{job_id}
curl http://localhost:8000/api/v1/jobs/result/{job_id}
```

将 API 暴露到可信本地环境之外前，请设置 `API_TOKEN`。Docker 镜像默认安装 `.[api]`；构建时设置 `INSTALL_EXTRAS=true` 可加入文档解析器。

## 文档

- [CLI、TUI 与 API](docs/cli_tui_api.md)
- [Python SDK 与 Provider 集成](docs/developer_integration.md)
- [证据模式与文献 Provider](docs/mock_vs_real_provider.md)
- [从 v0.2 迁移](docs/migration_v0.3.md)
- [开发指南](DEVELOPMENT.md)
- [公开路线图](README_plan.md)
- [v0.3.0 发布说明](docs/releases/v0.3.0.md)
- [Crossref 示例报告](examples/sample_crossref_report.md)
- [文档分析示例报告](examples/sample_document_report.md)

## 项目状态

v0.3 建立可安装包、强类型语义契约、统一入口、迁移路径和发布质量门。v0.4 将聚焦引用完整性、证据等级、报告预设与 JSON/HTML 导出。详见[路线图](README_plan.md)。

## 贡献与安全

开发约定见 [CONTRIBUTING.md](CONTRIBUTING.md)，项目署名见 [CONTRIBUTORS.md](CONTRIBUTORS.md)，支持的安全模型与私密报告方式见 [SECURITY.md](SECURITY.md)。

## 许可证

MIT
