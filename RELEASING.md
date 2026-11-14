# 发布 naiwasay

源码仓库：https://github.com/ZeshenTian/naiwasay

发布使用 GitHub Actions 和 PyPI Trusted Publishing（OIDC），无需长期 API Token。

## 首次关联

在 PyPI 的账户 Publishing 页面添加 GitHub pending publisher：

| 字段 | 值 |
| --- | --- |
| PyPI Project Name | `naiwasay` |
| Owner | `ZeshenTian` |
| Repository name | `naiwasay` |
| Workflow name | `publish.yml` |
| Environment name | `pypi` |

GitHub 仓库的发布环境名称必须是 `pypi`。首次上传成功后，PyPI 会自动创建项目，
并将 pending publisher 转为项目的正式发布者。

## 发布新版本

1. 修改 `pyproject.toml` 和 `src/naiwasay/main.py` 中的版本号。
2. 合并到 `main`，等待 CI 测试和打包检查通过。
3. 创建对应版本的 GitHub Release，例如 tag `v0.1.0`。
4. 发布 Release；`publish.yml` 会运行测试、构建 wheel 和 sdist、检查元数据，
   随后通过 OIDC 上传到 PyPI。
5. 查看 https://pypi.org/project/naiwasay/，在新环境验证安装。

也可以在 GitHub Actions 页面手动运行 Publish to PyPI 工作流。
同一版本不要重复上传；PyPI 不允许复用已经上传过的文件名。

## 本地检查

```bash
python -m pip install -e . build twine
python -m unittest discover -s tests -v
python -m build
python -m twine check --strict dist/*
```

## 验证公开版本

```bash
python -m pip install --index-url https://pypi.org/simple naiwasay
python -m naiwasay -t "Hello, 奶蛙!"
```
