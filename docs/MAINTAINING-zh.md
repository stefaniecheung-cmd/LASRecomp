# 中文界面版：维护与构建指南

这个分支（`zh-cn`）是 [peiikai/LASRecomp](https://github.com/peiikai/LASRecomp) 的长期维护分支，只做一件事：
**把界面文字换成中文**。游戏逻辑、图形、音频、构建系统都没有改。

上游一旦发新版，按本文第 6 节的步骤合并即可。

---

## 1. 这个分支改了什么

| 位置 | 内容 |
|---|---|
| `runtime/ui/localization_strings.h` | 词表：`UI_TEXT(英文, 简体, 繁体)`，英文原文当 key |
| `runtime/ui/*.mm` | 把写死的英文换成 `ui_tr()` / `ui_label()`；右栏说明、传送点、追踪器、软键盘、存档编辑、作弊页等 |
| `zh_table.py` | **词表唯一数据源**（554 条补充译文），改了这里才算改了译文 |
| `gen_strings.py` | 由 `zh_table.py` 生成词表区块，幂等，支持 `--check` |
| `scripts/check_zh.py` | 提交前自检（重复键、占位符、换行转义、繁体漏转等） |
| `.github/workflows/zh-build.yml` | 只构建 Windows exe 的轻量工作流（可选） |

上游自带的 495 条译文（`localization_strings.h` 里「补充翻译」标记行**之前**的部分）保持原样，
改它们直接编辑 header；我们不维护那一段。

## 2. 译文是怎么生效的

- 查表：`ui_tr("English")` 返回 `const char*`，查不到就原样返回英文。**缺条目 = 显示英文**，不会崩。
- 按钮/标签：`ui_label("English")` 返回 `译文 + "###" + English`。`###` 后面是 ImGui 的内部 ID，
  所以译文怎么改，控件 ID 都不变，不会让布局状态错乱。
- 动态文案：用带占位符的整条词条，例如
  `snprintf(buf, sizeof buf, ui_tr("%d small keys"), n)`，
  不要自己拼「中文片段 + 数字」，否则顺序和量词没法按语言调整。
- **静态数组的坑**：`static const char* steps[] = { ui_tr("...") }` 会在进程启动时定死语言，
  之后切语言不生效。改成函数里现取。
- 字体：渲染器只吃 TrueType，不吃 CFF 轮廓。Noto Sans CJK 这类 `.otf`（CFF）无效；
  上游 Beta 5.4 起（#389）改用系统中文字体，正常系统不需要额外操作。

## 3. 改译文的正确姿势

```bash
# 1) 改 zh_table.py（英文原文做 key，值是 (简体, 繁体)）
# 2) 重新生成词表区块
python gen_strings.py
# 3) 自检
python gen_strings.py --check      # 生成物是否与数据源一致
python scripts/check_zh.py         # 结构检查，必须「全部通过」
```

规则：

- **不要**再运行 `gen_strings_legacy.py`。它用「列表下标」对译文，一旦错位整段串行——历史事故就是这么来的。
- 繁体那一列可以留空由 OpenCC 生成，但推荐直接写死：`s2twp` 会把「哈希」转成「雜湊」这类地区词。
- 一条英文对应一条译文。单复数、大小写不同就是不同的 key（`Bottle` / `Bottles` 各占一行）。
- 说明文字的换行写在 Python 里就是真的 `\n`，生成器会转成 C 的单层转义；**不要手写 `\\n`**。

## 4. 新增界面文案怎么补

上游加了新界面，中文会先显示英文。补的步骤：

```bash
# 找出代码里所有直接写死的 ui_tr/ui_label 文案
python scripts/check_zh.py          # 先看现有表是否健康
grep -rn 'ui_tr("' runtime/ui | wc -l
```

- 直接写字面量的：把英文原文加进 `zh_table.py` 即可。
- 走变量的（选项标题、传送点名、道具名来自数据表）：要在数据源头找英文原文，
  同样以原文作 key 加进 `zh_table.py`。
- 加完跑一遍 `python gen_strings.py && python scripts/check_zh.py`，再构建。

## 5. 构建与发布

发布走上游的 `.github/workflows/release.yml`（四平台 + draft release），**不要**用 `zh-build.yml`
出正式包（它只编 Windows exe，方便快速验证）。

```bash
# tag 必须等于 runtime/ui/launcher.mm 里的 LARECOMP_VERSION（当前 beta_5.4）
gh workflow run release.yml --ref zh-cn -f tag=beta_5.4 -f ref=$(git rev-parse HEAD)
```

要点：

- **`ref` 要传完整 40 位 SHA**。传短 SHA（如 `11c733d`）会让 `actions/checkout` 直接失败。
- 产物名带版本：`LAS Recomp-beta_5.4-linux-x86_64.AppImage`、`windows.zip`、`macos.dmg`、`linux-aarch64.AppImage`。
- 同一版本反复构建会堆出多个同名 artifact，**下载前先核对 digest**：
  ```bash
  curl -s -H "Authorization: Bearer $TOKEN" \
    https://api.github.com/repos/<owner>/LASRecomp/actions/artifacts/<id> | grep digest
  ```
  本地 `sha256sum` 与之比对，确认拿的是这一次的包（曾因同名 artifact 拿错过一次）。
- 国内到 GitHub 的下载常被掐断（约 40 KB/s，中途断流）。用续传，多轮直到字节数对上：
  ```bash
  curl -sL -C - -H "Authorization: Bearer $TOKEN" -o out.zip \
    https://api.github.com/repos/<owner>/LASRecomp/actions/artifacts/<id>/zip
  ```
- 解出来的 AppImage 直接改名发布即可（例如 `LAS.Recomp-beta.AppImage`）；Steam 上启动参数用
  `APPIMAGE_EXTRACT_AND_RUN=1 %command%`，不要走 Proton。

### 发布作业（`release`）常见失败

| 现象 | 原因 | 处理 |
|---|---|---|
| `HTTP 403: Resource not accessible by integration` (POST /releases) | fork 的 **Settings → Actions → General → Workflow permissions** 默认是 *Read repository contents*，`jobs.release` 里的 `permissions: contents: write` 不足以提权 | 改成 **Read and write**（或用 PAT 手动建）：`curl -X PUT .../actions/permissions/workflow -d '{"default_workflow_permissions":"write"}'`。改完必须**重新 dispatch 一个新运行**——重跑（re-run）会沿用旧运行的权限快照，仍然 403 |
| 草稿 release 里是旧产物 | 上一次运行留下的草稿仍在，`gh release edit` 把 target 指回旧 SHA 或直接失败 | 先删草稿：`curl -X DELETE .../releases/<id>`，再 dispatch。草稿的 target 应等于本次 `check` 输出的 SHA |
| `expected 4 files` | 四个平台产物没齐（某个 job 挂了，或同名 artifact 被覆盖） | 看哪个 job 失败先修，不要绕过这条断言 |

## 6. 上游同步

```bash
git remote add upstream https://github.com/peiikai/LASRecomp   # 只需一次
git fetch upstream
git checkout zh-cn
git merge upstream/beta_5        # 上游主线分支名以实际为准
```

冲突集中在两类，处理原则：

| 冲突文件 | 处理 |
|---|---|
| `runtime/ui/localization_strings.h` | 上游新增的条目直接保留；「补充翻译」区块整段丢给生成器：`python gen_strings.py` 覆盖 |
| `runtime/ui/*.mm` | 保留我们的 `ui_tr(...)` 调用，把上游新写的英文串包进 `ui_tr(...)`；新文案记进 `zh_table.py` |

合并完：

1. 看 `runtime/ui/launcher.mm` 的 `LARECOMP_VERSION` 有没有变，变了就改 tag 再构建。
2. `python gen_strings.py && python scripts/check_zh.py`。
3. 本地跑一遍菜单，重点看新增页面（上游每次都会加设置项或随机化选项）。
4. 重新构建、校验 digest、发版。

## 7. 踩过的坑

| 现象 | 原因 | 现在的做法 |
|---|---|---|
| 右栏某条说明变成了别的条目的话 | 译文按列表下标对齐，中途多一条就整体串行 | 改为按英文原文做 key（`zh_table.py`） |
| 说明里显示字面的 `\n\n` | 生成时把换行转义了两层 | 生成器统一单层转义，`check_zh.py` 拦截 |
| 繁体界面里混着简体 | 只写了简体列，繁体没转 | 数据源直接存两列 |
| 下载到的包功能是旧的 | 同名 artifact 有多个，拿错了 | 用 API 的 `digest` 与本地 sha256 比对 |
| 构建在 checkout 就失败 | 手动触发时传了短 SHA | 传完整 SHA |
| 下载中途断了 | 链路限速 | `curl -C -` 多轮续传，比对总字节数 |
| 切语言后部分文字不变 | `static` 数组在启动时就取了 `ui_tr` | 改到函数内取值 |

## 8. 术语表（保持一致，别再另起译名）

尾巴洞窟 / 瓶之洞窟 / 钥匙洞窟 / 钓鱼人洞窟 / 鲶鱼之口 / 脸之神殿 / 鹰之塔 / 龟岩 / 色彩迷宫 ·
马贝村 / 动物村 / 乌库库草原 / 塔塔尔高地 / 卡纳莱特城堡 / 贝壳馆 / 漂流竞速 / 时髦抓娃娃 ·
林克 / 玛林 / 塔林 / 汪汪 / 飞天鸡 / 风鱼 / 塞壬乐器 / 三角神力 / 心之容器 / 心之碎片 ·
小钥匙 / 噩梦钥匙 / 石喙 / 魔法粉 / 天马靴 / 钩索 / 脚蹼

一致性检查：`grep -o` 一把可疑变体（如「瓶子洞窟」「面之神殿」），出现即说明有人另起炉灶。
