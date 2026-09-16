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

## 最近更新

- **LilToNonToon Switcher 1.1.5**（2026-09-17）：阴影渐变改成按 lilToon 的过渡窗口采样（`[border ± blur/2]`，阴影色 alpha 当强度），
  修掉脸上硬边 + 阶梯状的明暗分界。
- **LilToNonToon Switcher 1.1.4**（2026-09-17）：lilToon 透明遮罩（`_AlphaMask`）改 alpha 的效果现在会烘进基础贴图
  （半透明轻纱不再变实心）；描边宽度按对象缩放折算，并新增「描边宽度倍数」手动系数。
- **NonToon Light Limit 1.1.8**（2026-09-16）：亮度模块的生效范围改成显式开关，修掉共享遮罩把亮度整个挡掉的问题。

浏览器打开 <https://njsgdd10086.github.io/vpm-listing/> 可以看每个包的版本、下载链接和源码仓库。

## 怎么用

1. VCC / ALCOM → **Settings → Packages → Add Repository**；
2. 填入 `https://njsgdd10086.github.io/vpm-listing/index.json`；
3. 回到工程的 **Manage Project**，按需 Install。

装哪个插件由你决定，索引里不会有任何东西被强制安装。

## 浏览器里看

用浏览器打开仓库根地址（<https://njsgdd10086.github.io/vpm-listing/>）会看到一个人看的页面：
每个包的名称、最新版本、说明、全部版本下载链接和源码仓库，以及该填进 Add Repository 的地址。
页面和 `index.json` 都是 GitHub Actions 每次跟进插件仓库的新版本后自动重新生成的。

## 索引怎么更新

`scripts/make_vpm_repo.py` 把两个插件仓库的 Release 合并成一份索引，工作流每 15 分钟跟一次；
发版后想立刻刷新，就在 Actions 页面手动跑一次 `重建 VPM 索引`（或往本仓库 push 一次）。

## 许可

MIT。
