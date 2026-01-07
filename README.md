# Playwright Enterprise Demo

这是一个企业级 UI 自动化测试框架示例，基于 Playwright（Sync API）+ Pytest + Allure。
强调严格 POM、类型标注、稳定性与可追踪的失败证据策略，适用于面试与工程化展示。

## 技术栈

- Python 3.10+
- Playwright（Sync API）
- Pytest
- Allure
- Poetry

## 目录结构

```
.
├── .github/workflows/playwright.yml
├── config/
├── pages/
├── tests/
├── utils/
├── conftest.py
├── pyproject.toml
├── requirements.txt
├── pytest.ini
└── README.md
```

## 关键工程实践

- 严格 POM：测试代码不出现原生选择器
- BasePage 统一封装等待、异常处理、高亮展示
- 失败证据策略（默认开启）：
  - screenshot: only-on-failure
  - trace: retain-on-failure
  - video: retain-on-failure（可选）
- CI 上传 `allure-results` 与 `artifacts`，可追踪失败原因

## 配置体系（多环境）

支持 `config/{dev,staging,prod}.yaml`，运行时通过 `ENV=staging` 选择。
YAML 使用与环境变量一致的 `APP_*` 键名（如 `APP_BASE_URL`）。
`dev` 默认使用公开的 SwagLabs 账号，可直接运行；如需覆盖，使用环境变量或 `.env`。
敏感信息通过环境变量或 GitHub Secrets 注入：

```
APP_BASE_URL=https://www.saucedemo.com/
APP_TIMEOUT=10000
APP_HEADLESS=true
APP_BROWSER=chromium
APP_USERNAME=CHANGEME
APP_PASSWORD=CHANGEME
APP_TRACE_MODE=retain-on-failure
APP_VIDEO_MODE=off
APP_ENV=dev
```

本地运行时：复制 `.env.example` 为 `.env`（不会提交到仓库）。

## 本地运行

### Poetry 安装依赖

```
poetry install --no-interaction --no-root
poetry run playwright install --with-deps
```

### 执行用例

```
poetry run pytest
```

### 生成 Allure 报告

```
allure generate allure-results -o allure-report --clean
```

## CI / DevOps（GitHub Actions）

工作流：`.github/workflows/playwright.yml`

- 触发：`main` 分支 Push / PR
- Poetry 缓存 + Playwright 浏览器缓存
- 并行执行：pytest-xdist（`-n auto`）
- 上传 `allure-results` 与 `artifacts`
- 生成 Allure HTML 并发布到 GitHub Pages
