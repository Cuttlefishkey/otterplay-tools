# Otterplay Tools

[Otterplay](https://otterplay.games/) 的网站维护小工具。Otterplay 是免费网页游戏合集，提供英文、简体中文的游戏介绍与上手指南。

[English](README.md) · [发布步骤](PUBLISHING.md)

## Sitemap 链接检查

检查 XML sitemap 中页面的 HTTP 可用性，支持普通 `urlset` 和多层 `sitemapindex`，可直接读取 Otterplay 的游戏、分类和静态页面 sitemap。

- Python 3.9 及以上，无需安装第三方依赖，也不依赖主站源码。
- 串行发送 GET 请求，报告 HTTP 错误、网络错误和重定向。
- 自动去重；默认最多读取 50 个 sitemap、检查 500 个页面。
- 可导出 JSON 报告。

在本目录运行：

```sh
python scripts/check_sitemap.py --help
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml --output reports/otterplay.json
```

也可用于其他网站：

```sh
python scripts/check_sitemap.py https://otterplay.games/sitemap.xml --max-pages 1000 --timeout 20 --delay 0.5
```

只跟进与起始 sitemap 同源的条目（协议、主机、端口相同），跨源条目会报错。HTTP 重定向会自动跟随并记录，重定向目标可能跨源。默认请求间隔为 0.2 秒，每次请求超时为 15 秒，每个 sitemap 最多读取 10 MiB。

页面结果分为 `OK`、`REDIRECT` 和 `ERROR`。退出码 `0` 表示所有检查页面均直接返回 2xx；`1` 表示出现错误、重定向或检查未完成；`2` 表示命令参数错误。达到数量上限时会明确报告，不会把部分检查当作全部通过；调大上限后会从头检查。

工具不运行 JavaScript、不检查嵌入游戏内容、不校验 canonical，也不测量 Core Web Vitals。HTTP 返回成功只代表地址可访问；超时或被拦截的结果需要人工确认。

## 关于 Otterplay

[Otterplay](https://otterplay.games/) 收录塔防、合成、消除解谜与卡牌等浏览器游戏，并提供中英文介绍和上手指南。游戏通过第三方提供方的播放器加载，Otterplay 不是这些游戏的开发者或版权方。

本仓库只包含维护工具，不包含游戏代码、游戏资源和主站源码。

## 许可证

本仓库代码与文档采用 [MIT License](LICENSE)。
