# ATRI_NAIXU VPM Listing

个人 VPM 包索引仓库。VCC / ALCOM 里只需要添加**这一个地址**，就能看到全部插件：

```
https://njsgdd10086.github.io/vpm-listing/index.json
```

## 包含的插件

| 包名 | 插件 | 仓库 |
| --- | --- | --- |
| `com.nontoon.switcher` | LilToNonToon Switcher —— 右键把 lilToon 材质一键转成 NonToon，并生成一键切换开关 | [LilToNonToonSwitcher](https://github.com/njsgdd10086/LilToNonToonSwitcher) |
| `com.atrinaxu.nontoon.lightlimit` | NonToon Light Limit —— NonToon 的亮度上下限 / 亮度倍数 / 全局控制，附一键生成全局亮度动画 + 菜单 | [NonToonLightLimit](https://github.com/njsgdd10086/NonToonLightLimit) |

## 怎么用

1. VCC / ALCOM → **Settings → Packages → Add Repository**；
2. 填入 `https://njsgdd10086.github.io/vpm-listing/index.json`；
3. 回到工程的 **Manage Project**，按需 Install。

装哪个插件由你决定，索引里不会有任何东西被强制安装。

## 索引是怎么来的

`index.json` 不是手写的，而是由本仓库的 GitHub Actions 自动生成：

* 抓取 `PACKAGE_REPOS` 里各插件仓库的 Release 资产（`<包名>-<版本>.zip`）；
* 合并成一份索引，每个版本的下载地址直接指向对应仓库的 Release；
* 推送到本仓库的 `gh-pages` 分支。

触发时机：本仓库有提交、每天定时一次、也可以在 Actions 页面手动运行。
插件仓库发新版本时，其 Release 会自动带上新版本，索引在定时任务里跟进
（想立刻刷新就手动跑一次 `重建 VPM 索引`）。

要新增插件，只要把它的仓库加进 `.github/workflows/index.yml` 的 `PACKAGE_REPOS`
和 `scripts/make_vpm_repo.py` 的 `PACKAGE_INFO` 即可。

## 许可

本仓库只是索引与构建脚本，MIT。
