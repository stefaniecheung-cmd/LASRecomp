# -*- coding: utf-8 -*-
"""二级界面（软键盘、随机化、剧透、存档编辑、作弊、按键、宠物、开始界面弹窗、追踪器图例）的译文。"""

TRANS = {
    # ---- 通用按钮/标签
    "Choose": "选择",
    "Done": "完成",
    "Close": "关闭",
    "Cancel": "取消",
    "OK": "确定",
    "Space": "空格",
    "Delete": "删除",
    "Move": "移动",
    "Rename": "重命名",
    "Play": "游玩",
    "Play Now": "立即游玩",
    "Use it": "使用它",
    "Start fresh": "重新开始",
    "Keep here": "就放这里",
    "Change...": "更改……",
    "update": "更新",
    "None": "无",
    "Settings": "设置",
    "Game Files": "游戏文件",
    "Filters": "筛选",
    "one-way": "单向",
    "leads to A": "通往 A",
    "No matches.": "没有匹配的结果。",
    "SEED HASH": "种子哈希",
    # ---- 提示行
    "Load a save file and get into the game to use cheats.": "读取存档并进入游戏后即可使用作弊功能。",
    "Esc cancels.": "按 Esc 取消。",
    "Load a save file first: the editor changes the save that's currently being played.":
        "请先读取一个存档：编辑器改的是当前正在游玩的存档。",
    "Companion:": "同伴：",
    "(also on the pause menu's Items page: LEFT from the item grid)":
        "（也可以在暂停菜单的道具页操作：在道具格上按左方向键）",
    "Game files ready.": "游戏文件已就绪。",
    "Seed ready.": "种子已就绪。",
    # ---- 开始界面
    "!  This folder is synced by OneDrive": "!  这个文件夹由 OneDrive 同步",
    "All game files (about %.0f GB) will be uploaded to your OneDrive.":
        "全部游戏文件（约 %.0f GB）都会被上传到你的 OneDrive。",
    "Choose another folder": "选择其他文件夹",
    "How would you like to play?": "你想怎么玩？",
    "You can change this any time in Settings.": "随时可以在设置里更改。",
    "Authentic 16:9": "原版 16:9",
    "Unlocked (fill the screen)": "不限制（铺满屏幕）",
    "LAS Recomp has its own menu for settings, the randomizer, cosmetics and more.":
        "LAS Recomp 自带菜单，可用来调整设置、随机化、外观等等。",
    "Open it in game with F1 or Esc, or on a controller with the %s (or %s together).":
        "在游戏里按 F1 或 Esc 打开，手柄上按 %s（或同时按 %s）。",
    "Moving your data": "正在迁移你的数据",
    "Data folder": "数据文件夹",
    "This folder is synced by OneDrive too.": "这个文件夹也由 OneDrive 同步。",
    "This folder already has LAS Recomp data. Use it?": "这个文件夹里已经有 LAS Recomp 数据，要用它吗？",
    "Move your saves, seeds, settings and game files (%.1f GB) there, or start fresh?":
        "把存档、种子、设置和游戏文件（%.1f GB）迁移过去，还是重新开始？",
    "Not enough free space there to move them (%.1f GB free).":
        "那边的可用空间不够迁移（剩余 %.1f GB）。",
    "Restarting...": "正在重启……",
    "Copying...": "正在复制……",
    "Checking the copy...": "正在校验副本……",
    "Removing the old copy...": "正在删除旧副本……",
    "Your data is still in %s": "你的数据仍然在 %s",
    "Show in Explorer": "在资源管理器中显示",
    "Open folder": "打开文件夹",
    "Show in Finder": "在访达中显示",
    "Delete game files": "删除游戏文件",
    "Are you sure?": "确定吗？",
    "This deletes LAS Recomp's copy of the game files (%.1f GB).":
        "这会删除 LAS Recomp 保存的游戏文件副本（%.1f GB）。",
    "Saves, seeds and settings are kept. Your own game files aren't touched.":
        "存档、种子和设置都会保留，你自己的游戏文件不会被动到。",
    "Dev checkout: this is %s": "开发版检出：当前是 %s",
    "Text: %s    Chinese / Korean: %s    Button icons: %s": "正文：%s    中文/韩文：%s    按键图标：%s",
    "Fonts aren't included. For the original look, import your own copies of "
    "nintendo_udsg-r_std_003.bfttf (text), the same-named files for Chinese and Korean "
    "(nintendo_udsg-r_org_zh-cn_003, nintendo_udsg-r_ext_zh-cn_003, nintendo_udjxh-db_zh-tw_003, "
    "nintendo_udsg-r_ko_003) and nintendo_ext_003.bfttf (button icons). "
    ".ttf versions with the same names work too.":
        "字体不随程序附带。想要原版观感，请自行导入 nintendo_udsg-r_std_003.bfttf（正文）、"
        "中韩文同名文件（nintendo_udsg-r_org_zh-cn_003、nintendo_udsg-r_ext_zh-cn_003、"
        "nintendo_udjxh-db_zh-tw_003、nintendo_udsg-r_ko_003）以及 nintendo_ext_003.bfttf（按键图标）。"
        "同名的 .ttf 版本也可以。",
    "Nintendo font (imported)": "任天堂字体（已导入）",
    "substitute (this OS's, per language)": "替代字体（本机系统，按语言）",
    "substitute": "替代字体",
    "imported": "已导入",
    "Switch fonts": "Switch 字体",
    "Import fonts": "导入字体",
    "Use substitute font": "使用替代字体",
    # ---- 随机化面板
    "Delete this seed and its save files?": "删除这个种子及其存档？",
    "Delete seed + saves": "删除种子和存档",
    "Spoiler log (locked)": "剧透日志（已锁定）",
    "Spoiler log": "剧透日志",
    "Copy seed ID": "复制种子 ID",
    "With the entrance randomizer on, at least one kind of entrance must be shuffled.":
        "开启入口随机化时，至少要有一类入口参与乱序。",
    "How many pieces finish the game: 1 to 50.": "多少心之碎片算通关：1 到 50。",
    # ---- 剧透视图
    "< Back": "< 返回",
    "Spoiler log - %s": "剧透日志 - %s",
    "No readable spoiler for this seed yet. Generate it with: tools/rando/spoiler_view.py rando/%s":
        "这个种子还没有可读的剧透。可以这样生成：tools/rando/spoiler_view.py rando/%s",
    "This shows where every item is, plus a step-by-step route to beat the seed.":
        "这里会显示每个道具的位置，以及一条分步通关这个种子的路线。",
    "Reveal spoilers": "显示剧透",
}
