# 发布到 GitHub

本目录是一份可独立发布的仓库内容。当前创建这些文件不会自动创建远程仓库或发布任何内容。

## 仓库设置

| 字段 | 建议填写 |
| --- | --- |
| Repository name | `otterplay-tools` |
| Visibility | Public |
| Description | Sitemap and link-checking utilities from Otterplay, a curated browser games website. |
| About → Website | `https://otterplay.games/` |
| Topics | `sitemap`, `link-checker`, `website-maintenance`, `python`, `otterplay` |

## 上传方法

1. 将本目录整体复制到主站项目之外，例如 `D:\WorkSpace\otterplay-tools`。确认 README、LICENSE 和 scripts 都在新目录根部。
2. 在 GitHub 创建空的 `otterplay-tools` 公开仓库。不要勾选自动生成 README、许可证或 `.gitignore`，这些文件已准备好。
3. 在新目录打开终端，执行下列命令。将 `YOUR_ACCOUNT` 替换成实际账号或组织名称。

```sh
git init
git add .
git commit -m "Add sitemap link checker and Otterplay documentation"
git branch -M main
git remote add origin https://github.com/YOUR_ACCOUNT/otterplay-tools.git
git push -u origin main
```

不要直接在当前主站项目的 `doc/otterplay-tools` 内执行 `git init`，以免产生嵌套仓库。

4. 在仓库页面右侧 About 的设置中填写 Website、Description 和 Topics。
5. 确认 README 的官网链接可打开，Usage 命令可运行。

也可以通过 GitHub 网页的 Add file → Upload files 上传本目录中的文件和 `scripts` 文件夹，保留其目录结构。隐藏的 `.gitignore` 需确认一并上传。

## 发布内容与维护

- 本目录中的 MIT 许可证适用于这里新增的工具和文档；不代表主站或第三方游戏也采用 MIT。
- 不要把主站 `.git`、环境变量、凭据、数据库文件、用户数据或第三方游戏资源复制进来。
- 无需另外购买域名、部署 GitHub Pages 或公开主站源码。
- 当前版本只包含实际实现的 sitemap 检查功能。后续有真实需求再增加其他工具。
- 后续修改主站中的这份副本不会自动同步到独立仓库，需要自行同步。

## 外链预期

README 的介绍和 About 的官网字段用于说明项目与 Otterplay 的关系。公开仓库不保证被搜索引擎收录、提升排名或获得 AI 引用。保持内容准确、工具可运行，比重复堆放链接更有意义。
