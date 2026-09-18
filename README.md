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

- **NonToon 亮度控制 1.1.9 / LilToNonToon Switcher 1.1.12**（2026-09-17）：两个插件都加了**版本号显示与更新检查** ——
  菜单「关于与更新检查…」显示当前版本与索引里的最新版本，窗口顶部也有版本号和按钮，编辑器启动后每天自动检查一次。
- **LilToNonToon Switcher 1.1.11**（2026-09-17）：源 shader 没有描边变体时不再照搬残留的 _OutlineWidth —— 之前透明/特效层会凭空多出一圈**不透明**描边壳，在 VR 里就像有东西挡住视野。
- **LilToNonToon Switcher 1.1.10**（2026-09-17）：共享遮罩的多个遮罩不再挤在同一个通道上互相覆盖（烘焙时自动分配空闲通道）。
- **LilToNonToon Switcher 1.1.9**（2026-09-17）：与另一个转换插件逐属性对拍后修掉 4 个问题 —— 阴影/边缘阴影渐变索引串位、
  `_UseReflection = 0` 时凭空多出的高光、没挂法线贴图时照搬的 `_BumpScale`、alpha 通道混合系数的误换算。
- **LilToNonToon Switcher 1.1.8**（2026-09-17）：边缘光按 `_UseRim` 开关处理（作者没启用时不再凭空多出一圈），
  并补上 `_RimFresnelPower` 的幂次空间换算。
- **LilToNonToon Switcher 1.1.7**（2026-09-17）：lilToon 的透明是**预乘 alpha**（`Blend One OneMinusSrcAlpha`），NonToon 不预乘 ——
  照搬会把颜色原样叠上去，半透明的腮红/薄纱层就会变成实心块。现在自动做等价换算（源系数换成 `SrcAlpha`）。
- **LilToNonToon Switcher 1.1.6**（2026-09-17）：渐变资产写文件时不再把关键点压回 4 个等距点（1.1.5 的阴影修复因此没生效），
  并补上 `_ShadowStrength`。
- **NonToon Light Limit 1.1.8**（2026-09-16）：亮度模块的生效范围改成显式开关，修掉共享遮罩把亮度整个挡掉的问题。

浏览器打开 <https://njsgdd10086.github.io/vpm-listing/> 可以看每个包的版本、下载链接（带发布时间）和源码仓库。

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
