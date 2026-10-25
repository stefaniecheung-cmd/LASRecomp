# LAS Recomp Beta 5 — 中文界面版

> 个人自用的 **Windows** 构建：官方 Beta 5 加中文界面。
> 不含任何游戏文件、密钥或转储工具——那些需要你自己的正版备份。

这个仓库是 [peiikai/LASRecomp](https://github.com/peiikai/LASRecomp) 的 fork，只做了一件事：
**把界面中文化**。游戏本身的逻辑、图形、性能一行没改。

界面翻译移植自 [hjqcan/LASRecomp](https://github.com/hjqcan/LASRecomp) 的 Multi 分支（MIT），
再补上官方 Beta 5 自己的界面文字。

---

## 下载与安装

到 [Releases](https://github.com/xinghee/LASRecomp/releases) 下载 `lasrecomp-zh-*.zip`（约 5 MB）。

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
| 产物 | 98.8 MB | **5 MB** |

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
