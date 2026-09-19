#!/usr/bin/env python3
"""由 GitHub Release 资产生成 VPM 仓库索引（vpm.json / index.json）。

用法：
    python scripts/make_vpm_repo.py --releases releases-a.json releases-b.json \
        --repository owner/repo --output-dir pages

`releases-*.json` 是 GitHub API `/repos/{owner}/{repo}/releases` 的返回内容，
可以传多个仓库的结果，脚本会把它们合并成同一份「作者总仓库」索引。
生成的索引里，每个包版本的 url 直接指向 Release 资产（browser_download_url），
这样 VCC / ALCOM 下载时走的是 GitHub Release，不依赖 GitHub Pages 的可用性。
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import pathlib
import re

REPO_NAME = "ATRI_NAIXU VPM Packages"
AUTHOR_NAME = "ATRI_NAIXU"

# 每个包在 VCC / ALCOM 里显示的信息
PACKAGE_INFO = {
    "com.nontoon.switcher": {
        "displayName": "LilToNonToon Switcher",
        "description": "右键把 lilToon 材质一键转换为 NonToon（输出 <名称>_nontoon.mat），"
                       "并自动生成 Modular Avatar 的 MA Material Setter + 菜单开关。",
        "keywords": ["liltoon", "nontoon", "shader", "modular-avatar", "vrchat"],
        "license": "MIT",
    },
    "com.nontoon.modules": {
        "displayName": "NonToon Modules",
        "description": "NonToon 的扩展模块集合（Shader Core 模块）：织物/法线细节（布料质感）、"
                       "亮度上下限与亮度倍数。可以在 Tools/NonToon 模块 里逐项勾选；"
                       "装了下面对应的插件时会自动勾选所需模块。",
        "keywords": ["nontoon", "shader", "module", "fabric", "light-limit", "vrchat"],
        "license": "MIT",
    },
    "com.atrinaxu.nontoon.lightlimit": {
        "displayName": "NonToon Light Limit",
        "description": "给 NonToon 加上亮度上下限与亮度倍数，并支持全局统一控制，"
                       "做 Light Limit Changer 式的亮度调节；另附一键生成全局亮度动画 + 表情菜单滑块的小工具。",
        "keywords": ["nontoon", "shader", "light-limit", "vrchat"],
        "license": "MIT",
    },
}
DEFAULT_UNITY = "2022.3"

# 资产名规则：<包名>-<版本>.zip，包名里含连字符，所以从右侧取版本
ASSET_PATTERN = re.compile(r"^(?P<name>.+)-(?P<version>\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.\-]+)?)\.zip$")
# 从 release 的 API url 里取出它属于哪个仓库
REPO_PATTERN = re.compile(r"repos/(?P<slug>[^/]+/[^/]+)/releases")


def version_key(version: str) -> tuple:
    """把 x.y.z 变成可比较的数字元组，正式版排在预发布版前面。"""
    main, _, suffix = version.partition("-")
    numbers = tuple(int(part) for part in main.split(".") if part.isdigit())
    return numbers, suffix == ""


def build_page(vpm: dict, author_url: str, published: dict | None = None) -> str:
    """生成给人看的页面：用浏览器打开索引地址时不再是看不懂的 JSON。"""
    published = published or {}

    def version_link(v: dict) -> str:
        date = (published.get(v["version"]) or "")[:10]
        label = html.escape(v["version"]) + (f"（{date}）" if date else "")
        return f'<li><a href="{html.escape(v["url"])}">{label}</a></li>'

    cards = []
    for pkg_name, pkg in vpm["packages"].items():
        versions = list(pkg["versions"].values())
        latest = versions[0]
        items = "".join(version_link(v) for v in versions)
        cards.append(
            f'    <section class="card">\n'
            f'      <h2>{html.escape(latest["displayName"])}</h2>\n'
            f'      <p class="meta">{html.escape(pkg_name)} · 最新 {html.escape(latest["version"])}'
            f' · Unity {html.escape(latest["unity"])}</p>\n'
            f'      <p class="desc">{html.escape(latest["description"])}</p>\n'
            f'      <ul class="versions">{items}</ul>\n'
            f'      <p class="meta">源码仓库：<a href="{html.escape(latest["repo"])}">'
            f'{html.escape(latest["repo"])}</a></p>\n'
            f'    </section>'
        )
    total = sum(len(pkg["versions"]) for pkg in vpm["packages"].values())
    index_url = vpm["url"]
    generated = datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %z")
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(vpm["name"])}</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ margin: 0 auto; max-width: 46rem; padding: 2.5rem 1.25rem;
         font: 16px/1.7 -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif; }}
  h1 {{ font-size: 1.5rem; margin: 0 0 .25rem; }}
  .meta {{ color: #6a737d; font-size: .85rem; margin: .2rem 0; }}
  .desc {{ margin: .6rem 0; }}
  .card {{ border: 1px solid #d0d7de; border-radius: 10px; padding: 1rem 1.25rem; margin: 1rem 0; }}
  .versions {{ margin: .4rem 0 .6rem; padding-left: 1.2rem; columns: 4; }}
  code, pre {{ font-family: ui-monospace, Consolas, monospace; font-size: .85rem; }}
  pre {{ background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px; padding: .7rem .85rem; overflow-x: auto; }}
  @media (prefers-color-scheme: dark) {{
    .card, pre {{ border-color: #30363d; }}
    pre {{ background: #161b22; }}
    .meta {{ color: #8b949e; }}
  }}
</style>
</head>
<body>
  <h1>{html.escape(vpm["name"])}</h1>
  <p class="meta">{len(vpm["packages"])} 个包 · {total} 个版本 · 作者
    <a href="{html.escape(author_url)}">{html.escape(vpm["author"])}</a></p>

  <p>在 VCC / ALCOM 里「Add Repository」填下面这个地址，就能看到并安装这里的插件：</p>
  <pre>{html.escape(index_url)}</pre>

{chr(10).join(cards)}

  <p class="meta">本页与 <a href="index.json">index.json</a> 由 GitHub Actions 在每次跟进插件仓库的
    Release 后自动重新生成。发版后没立刻看到新版本的话，可以在本仓库的 Actions 页面手动跑一次
    「重建 VPM 索引」（定时任务有时会被 GitHub 延后）。<br>
    生成时间 {html.escape(generated)}</p>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--releases", required=True, nargs="+",
                        help="GitHub releases API 返回的 JSON 文件（可以传多个仓库的结果）")
    parser.add_argument("--repository", required=True, help="索引所在仓库 owner/repo")
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    login, repo_name = args.repository.split("/", 1)

    packages: dict[str, dict] = {}
    published: dict[str, str] = {}
    for path in args.releases:
        # utf-8-sig 兼容带 BOM 的 JSON（例如用 PowerShell 写出来的文件）
        releases = json.loads(pathlib.Path(path).read_text(encoding="utf-8-sig"))
        for release in releases:
            if release.get("draft"):
                continue

            match_repo = REPO_PATTERN.search(release.get("url", ""))
            slug = match_repo.group("slug") if match_repo else args.repository

            for asset in release.get("assets", []):
                match = ASSET_PATTERN.match(asset["name"])
                if not match:
                    continue
                pkg_name = match.group("name")
                version = match.group("version")
                info = PACKAGE_INFO.get(pkg_name, {})
                entry = {
                    "name": pkg_name,
                    "displayName": info.get("displayName", pkg_name),
                    "version": version,
                    "unity": info.get("unity", DEFAULT_UNITY),
                    "description": info.get("description", ""),
                    "url": asset["browser_download_url"],
                    "repo": f"https://github.com/{slug}",
                    "changelogUrl": f"https://github.com/{slug}/releases",
                    "license": info.get("license", "MIT"),
                    "keywords": info.get("keywords", []),
                    # 版本级的 author 是对象（VCC 的包模型就是这么定义的），跟仓库级的字符串不一样
                    "author": {"name": AUTHOR_NAME, "url": f"https://github.com/{login}"},
                }
                # GitHub 给了 zip 的 sha256 就带上（VCC 会用它校验下载的包）
                digest = asset.get("digest") or ""
                if digest.startswith("sha256:"):
                    entry["zipSHA256"] = digest[len("sha256:"):]
                # 只给网页用（不写进 index.json，避免多出未知字段）：这个版本的发布时间
                stamp = release.get("published_at") or asset.get("created_at") or ""
                if stamp:
                    published.setdefault(version, stamp)
                packages.setdefault(pkg_name, {"versions": {}})["versions"][version] = entry

    # 同一版本号在多个 release 里出现时，发布时间取最新的那次（重发 / 修资产的情况）
    for pkg in packages.values():
        for version in pkg["versions"]:
            stamps = [published.get(version)] if published.get(version) else []
            if stamps and max(stamps) != published.get(version):
                published[version] = max(stamps)

    # 版本从新到旧排：先按发布时间，缺失的再按版本号，VCC / ALCOM 里看起来更顺
    def order_key(version: str):
        return (published.get(version) or "", version_key(version))

    ordered = {name: {"versions": dict(sorted(pkg["versions"].items(), key=lambda kv: order_key(kv[0]), reverse=True))}
               for name, pkg in sorted(packages.items())}

    vpm = {
        "name": REPO_NAME,
        "id": f"com.{login}.vpm-repo",
        "url": f"https://{login}.github.io/{repo_name}/index.json",
        # VCC 的仓库模型里 author 是**字符串**（写成对象会让 VCC 直接报「不是有效的仓库列表」，
        # ALCOM 因为是宽松解析所以看不出来），版本级的 author 才是对象。
        "author": AUTHOR_NAME,
        "packages": ordered,
    }

    text = json.dumps(vpm, ensure_ascii=False, indent=2) + "\n"
    output = pathlib.Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    # VCC / ALCOM 读 index.json；vpm.json 作为兼容别名一并保留
    (output / "index.json").write_text(text, encoding="utf-8")
    (output / "vpm.json").write_text(text, encoding="utf-8")
    # 浏览器直接打开索引地址时给一个人看的页面
    (output / "index.html").write_text(build_page(vpm, f"https://github.com/{login}", published), encoding="utf-8")

    total = sum(len(pkg["versions"]) for pkg in ordered.values())
    print(f"已生成索引：包 {len(ordered)} 个，版本 {total} 个")
    for pkg_name, pkg in ordered.items():
        versions = list(pkg["versions"])
        stamp = (published.get(versions[0]) or "")[:10]
        print(f"  {pkg_name}: {', '.join(versions)}" + (f"（最新 {versions[0]}，{stamp}）" if stamp else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
