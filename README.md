# LAS Recomp Beta 5.4 — 中文界面版

> 个人自用的 **Windows** 构建：官方 Beta 5.4 加中文界面。
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
Beta 5.3 还给 release 构建加了 `--strip-debug`，所以 exe 从 16.3 MB 缩到 **4.0 MB**，功能不变。
Beta 5.4修复了崩溃问题、BowWow 在加载区域后的外观问题、草地上的线条问题以及控制器和随机化器问题。
固定的

点击“化妆品”选项卡上的颜色行时，开始屏幕不再崩溃。
游戏不再因字体中没有的字母而崩溃，例如 Pothole Field 中的德语猫头鹰文字（#452）。
在 Mac、Windows 和 Linux 系统上，BowWow 在离开房屋或加载区域后不再出现损坏（牙齿闪烁、眼睛摇晃）的情况（#463）。
在高分辨率下，草地上不再出现雾霾或黑线（#356），包括在 Windows 和 Linux 上分辨率比例不一致的情况下（#413）。
游戏会跟随你正在使用的控制器，而不仅仅是第一个连接的控制器（#455，#456）。
中文文本全部使用中文系统字体（#389）。
随机化：第一次触摸即可拾取灌木丛、花盆和挖掘出的物品。
随机化：敌人随机出现时，阿莫斯雕像下的楼梯会保持开放状态。
随机化：桃色束腰外衣不再变成肤色。
随机生成器：在 Windows 上可以正确读取种子文件（挖掘地点、贝壳地点、三角力量碎片、灵魂和敌人）。
随机化：乌尔丽拉的电话仍然适用于将束腰外衣视为升级。
地牢房间洗牌：逻辑知道你只能从哪些壁架门跳下去。
地牢房间洗牌：在配对模式下，一扇门永远不会通往它自己的房间。
地牢房间重组：跨越多个牢房的房间保留了自己的屋顶并逐渐消失。
地牢房间洗牌：地牢罐子按其所在房间的逻辑计数，百叶门需要击败该房间敌人的物品（例如，尖刺甲虫的盾牌）。
Windows 上的 Tracker：种子设置显示，Tarin 和海滩计数已收集，并且排除的检查已隐藏（#441）。
卢比作弊码和存档编辑器都只能修改到9999卢比，和游戏里一样。感谢……@gsel001。
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
| ✅ | F1 菜单的全部页签、选项名、选项值（**495 条**） |
| ✅ | 开始界面的 Settings 页 |
| ✅ | 随机化选项、道具名、地名、乐器曲名、作弊项、传送点 |
| ❌ | 右栏的详细说明文字（仍是英文——那些是多行拼接的字符串，需要单独处理） |
| — | 游戏内文本（对话框、道具说明、剧情）**不在此范围**：它们来自 romfs，本来就跟着游戏语言走 |

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

推送到 `zh` 分支会自动跑 [`.github/workflows/zh-build.yml`](.github/workflows/zh-build.yml)：

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
