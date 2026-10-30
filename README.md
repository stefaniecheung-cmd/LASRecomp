# LAS Recomp Beta 5.4 — 中文界面版

> **Windows / Linux** 构建：官方 Beta 5.4 加中文界面。
> 不含任何游戏文件、密钥或转储工具——那些需要你自己的正版备份。

这个仓库是 [peiikai/LASRecomp](https://github.com/peiikai/LASRecomp) 的 fork，只做了一件事：
**把界面中文化**。游戏本身的逻辑、图形、性能一行没改。

界面翻译移植自 [hjqcan/LASRecomp](https://github.com/hjqcan/LASRecomp) 的 Multi 分支（MIT），
再补上官方 Beta 5 自己的界面文字。

## 这一版跟上游的对应关系

基于官方 **Beta 5.4**（2026-10-29），包含 Beta 5 之后的三个热修：

| 版本 | 内容 |
|---|---|
| Beta 5.1 | Shellsanity 出道具崩溃（#349） |
| Beta 5.2 | 老 Intel 核显黑屏、Mali 崩溃、随机化水下道具、含重音/日文字符的名字选档崩溃 |
| Beta 5.3 | 游戏文件缺失/损坏检测、CFG 导致安装卡 10%、BowWow 在房屋内显示错乱、Steam Deck 60fps、存档编辑器「给予任意道具」 |
Beta 5.3 给 release 构建加了 `--strip-debug`，所以 exe 从 16.3 MB 缩到 **4.0 MB**，功能不变。

**Beta 5.4 修的问题**（上游 release notes 摘译）：

- 开始界面在「外观」页签点颜色行时崩溃
- 字体里缺某个字母时的崩溃（例如坑洞田野的德文猫头鹰文本，#452）
- macOS / Windows / Linux 上 BowWow 离开房屋或换区后外观错乱（牙齿闪烁、眼睛抖动，#463）
- 高分辨率下草地出现黑线或雾状条纹（#356），以及 Windows 与 Linux 缩放比例不一致时的同类问题（#413）
- 手柄只跟着第一个连上的设备，现在跟随当前正在用的那只（#455、#456）
- 界面文字改用系统中文字体（#389）——这是中文能正常显示的前提

随机化与追踪器：

- 灌木、花盆、挖出来的道具第一次碰到就能拾取
- 敌人随机化时，Armos 雕像下的楼梯保持开启
- 桃色衣服不会再变成肤色
- 随机生成器在 Windows 上能正确读取种子文件（挖掘点、贝壳点、三角神力碎片、灵魂、敌人）
- 乌尔丽拉的电话仍会把衣服当作升级处理
- 房间重排：逻辑知道你只能从哪些平台门跳下去
- 房间重排：配对模式下，一扇门不会通回自己的房间
- 房间重组：跨多个房间的大房间保留自己的天花板并渐隐
- 房间重排：罐子按所在房间的逻辑计数；铁栅门需要能击败该房间敌人的道具（比如打尖刺甲虫要盾）
- Windows 上的追踪器：显示种子设置、Tarin 与海滩的已收集计数，并隐藏被排除的检查点（#441）
- 卢比的作弊与存档编辑都上限 9999，和游戏内一致（感谢 @gsel001）
---

## 下载与安装

到 [Releases](https://github.com/xinghee/LASRecomp/releases) 下载 `lasrecomp-zh-*.zip`（约 1.6 MB，内含 4 MB 的 exe）。

```
1. 解压，得到 lasrecomp.exe
2. 用它覆盖程序目录里同名的 lasrecomp.exe
3. 启动，进游戏，按 F1
```

**不要删**程序目录里的这些：

| 文件 / 目录 | 作用 |
|---|---|
| `data_root.txt` | 数据目录位置（删了会回落到默认，数据看起来"消失"） |
| `extracted\` | 游戏库 + 游戏文件（140 MB 的 `lasgame.dll` 在这里） |
| `save\` | 存档 |
| `larecomp.ini` | 设置与键位 |
| `fonts\` | 字体 |
| `start.bat` | 启动脚本（可选） |

### 不用重建游戏库

界面改动只在 `runtime/ui\` 里，`gamelib.h` / `gamelib.c` / `cpu.h` / 生成器都没动：

```
GAMELIB_ABI  = 1        （未变）
GAMELIB_ID              （未变）
```

所以现有的 `lasgame.dll` **直接加载**，不用重新编那 27 分钟，存档也照读。

---

## 中文什么时候生效

菜单语言**跟随游戏的语言设置**：

```
F1 → 操作 (Inputs) → 语言 (Language) → 中文（简体）
```

设成「自动」时，系统语言是中文也会自动认出来（`zh-CN` / `zh-SG` / `zh-TW` / `zh-HK` / `zh-MO`）。

---

## 翻译范围

| | 内容 |
|---|---|
| ✅ | F1 菜单的全部页签、选项名、选项值（**495 条**，上游自带） |
| ✅ | 右栏的详细说明文字（包括多行拼接的段落） |
| ✅ | 开始界面的 Settings 页 |
| ✅ | 随机化选项、道具名、地名、乐器曲名、作弊项、传送点、追踪器 |
| ✅ | 二级界面：软键盘、剧透日志、存档编辑、作弊页、按键设置、弹窗 |
| — | 游戏内文本（对话框、道具说明、剧情）**不在此范围**：它们来自 romfs，本来就跟着游戏语言走 |

合计 **1049 条**（上游 495 + 本分支补充 554），全部同时提供简体与繁体。

品牌名和实体按键名保留英文：`Nintendo` / `PlayStation` / `Xbox` / `Minus + Plus` / `View + Menu` / `Create + Options`。

---

## 需要你自己的游戏文件

本项目**不包含、也不会提供**游戏文件、密钥、固件、转储或解密工具。

需要你自己的《塞尔达传说：织梦岛》Switch 版备份，版本 **1.0.0 / 1.0.1 / 1.1.0** 之一，
并自己解出：

```
extracted\
  exefs\   main, main.npdm, rtld, sdk, subsdk0
  romfs\   完整 RomFS
```

游戏代码的重编译在**你自己的机器上**、用你自己的文件完成。

---

## 自己构建

本仓库只改 `runtime/ui\`，所以不需要上游那套"四平台 + 打包辅助工具"的流水线。

推送到 `zh-cn` 分支会自动跑 [`.github/workflows/zh-build.yml`](.github/workflows/zh-build.yml)：

```
checkout → MSYS2 (UCRT64) → make deps-windows（有缓存）
        → make -j B=build/win-release DEPS=... RELEASE=1 build/win-release/lasrecomp.exe
        → nm 校验（不含游戏代码）→ 上传 exe
```

| | 上游 `release.yml` | 本仓库 `zh-build.yml` |
|---|---|---|
| 平台 | 4 个 | **仅 Windows** |
| 内容 | exe + 生成器 + zig + 打 zip | **只出 exe** |
| 耗时 | 约 13 分钟 | **约 5 分钟** |
| 产物 | 98.8 MB | **约 1.6 MB**（strip 之后的 exe） |

本地想编也行，按上游的 [`docs/BUILD-windows.md`](docs/BUILD-windows.md) 装好 MSYS2 后：

```bash
make -j"$(nproc)" B=build/win-release DEPS="$(pwd)/build/deps-win" RELEASE=1 build/win-release/lasrecomp.exe
```

---

## 维护这个分支

译文全部放在 [`zh_table.py`](zh_table.py)（英文原文 → 简体/繁体），由它生成
`runtime/ui/localization_strings.h` 里的「补充翻译」区块：

```bash
python gen_strings.py          # 改了 zh_table.py 之后重新生成
python gen_strings.py --check  # 只比对，不写盘
python scripts/check_zh.py     # 结构自检：重复键、占位符、换行转义、繁体漏转
```

上游发新版后按 [`docs/MAINTAINING-zh.md`](docs/MAINTAINING-zh.md) 合并：
`git remote add upstream … && git fetch upstream && git merge upstream/beta_5`，
冲突集中在 `localization_strings.h`（整段交给生成器）和 `runtime/ui/*.mm`（保留 `ui_tr` 调用）。

那份文档里还有构建/发版的完整步骤、术语表和踩过的坑，改文案之前建议先看一眼。

---

## 目录关系

```
程序目录\             lasrecomp.exe、DLL、zig\、lasgen\、data_root.txt
数据目录\             cache\  extracted\  fonts\  save\  larecomp.ini
游戏文件目录\         exefs\  romfs\     （重选游戏文件时指向这里）
```

- **数据目录**和**游戏文件目录**是两回事：前者放存档和游戏库，后者只放 exefs/romfs
- 升级到新版本时，数据目录可以继续用（存档、设置全沿用），游戏库视 ABI 是否变化决定要不要重建

---

## 许可证

MIT，见 [`LICENSE`](LICENSE)。

- 重编译引擎：[peiikai/LASRecomp](https://github.com/peiikai/LASRecomp)
- 界面翻译来源：[hjqcan/LASRecomp](https://github.com/hjqcan/LASRecomp)（Multi）
- 上游原有的完整文档（英文）：[`README.upstream.md`](README.upstream.md)
