# Playwright Enterprise Demo

这是一个自动化测试框架示例，基于 Playwright（Sync API）+ Pytest + Allure，
采用严格 POM、类型标注和稳健的基础封装，面向面试展示和工程化实践。

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
└── README.md
```

## 关键设计

- 严格 POM：测试代码不出现原生选择器
- BasePage 统一封装等待、异常处理和高亮展示
- 失败自动截图 + trace（Allure 附件）
- CI 运行后上传 `allure-results` 与 `artifacts`

## 本地运行

### Poetry 安装依赖

```
poetry install --no-interaction --no-root
poetry run playwright install --with-deps
```

### 执行用例

```
poetry run pytest -q --alluredir=allure-results
```

### 生成 Allure 报告

```
allure generate allure-results -o allure-report --clean
```

## CI / DevOps（GitHub Actions）

工作流：`.github/workflows/playwright.yml`

- 触发：`main` 分支 Push / PR
- 安装 Poetry 与依赖
- 安装 Playwright 浏览器
- 运行 Pytest
- 上传 `allure-results` 与 `artifacts`

如需在 CI 中生成 Allure HTML 报告，可在工作流中增加：

```
allure generate allure-results -o allure-report --clean
```

并将 `allure-report` 作为 Artifact 上传。
