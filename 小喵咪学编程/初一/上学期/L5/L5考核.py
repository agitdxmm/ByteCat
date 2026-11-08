r'''
════════════════════════════════════════════════════════
  学习成果考核 · 初一上学期 · L5
  字符串 / 文件 / JSON / 异常处理 / 标准库
════════════════════════════════════════════════════════

  共 5 题，难度 1★ ~ 5★
  不给提示，全部自己写完再看末尾的答案。

════════════════════════════════════════════════════════
'''

# ═══════════════════════════════════════════════════════
#  第 1 题  ★
# ═══════════════════════════════════════════════════════
#
# 写这几个字符串处理函数：
#
#     def 规范空白(文本)      去掉两端空白，连续空白压成一个空格
#     def 转标题(文本)        每个词首字母大写，其余小写
#     def 截断(文本, 长度, 后缀="...")
#                            超过长度就截断并加后缀，总长不超过 长度
#     def 计数(文本, 字符)    统计某字符出现次数（不用 count）
#     def 反转每句话(文本)    每句话单独反转，顺序不变
#
# 测试：
#     规范空白("  a   b  c ")   → "a b c"
#     转标题("hello WORLD")     → "Hello World"
#     截断("这是一段很长的文字", 6) → "这是一..."
#     反转每句话("你好。再见。") → "好你。见再。"
#
# 你的代码：


# ═══════════════════════════════════════════════════════
#  第 2 题  ★★
# ═══════════════════════════════════════════════════════
#
# 写一个「文件行数统计工具」：
#
#     def 统计文件(路径)
#
# 返回字典：
#
#     {
#         "总行数": 10,
#         "空行": 2,
#         "注释行": 3,        # 以 # 开头（去掉缩进后）
#         "代码行": 5,
#         "最长行": "...",
#         "最长行号": 7,
#     }
#
# 要求：
#   · 文件不存在返回 None
#   · 编码不是 UTF-8 时也要处理（返回 None 或报错信息）
#   · 自己创建测试文件，测完删除
#   · 用 with + encoding="utf-8"
#
# 你的代码：


# ═══════════════════════════════════════════════════════
#  第 3 题  ★★★
# ═══════════════════════════════════════════════════════
#
# 做一个「配置管理器」：
#
#     def 读配置(路径)
#     def 写配置(路径, 配置)
#     def 改配置(路径, 键, 值)
#     def 重置配置(路径)
#     def 导出配置(路径, 目标CSV)
#
# 要求：
#   · 用 JSON 存储
#   · 默认配置：{"主题": "浅色", "字号": 14, "自动保存": True}
#   · 文件不存在 → 用默认配置创建
#   · 文件损坏 → 备份成 .bak 后用默认配置重建
#   · 读配置时补齐缺失的键（兼容旧版本）
#   · 导出 CSV 时每行是「键,值」
#
# 测试：创建 → 改 → 读 → 破坏文件 → 再读 → 导出
#
# 你的代码：


# ═══════════════════════════════════════════════════════
#  第 4 题  ★★★★
# ═══════════════════════════════════════════════════════
#
# 写一个「批量处理框架」：
#
#     def 批量处理(数据们, 处理函数, 重试次数=0, 遇错即停=False)
#
# 返回：
#
#     {
#         "成功": [(原始数据, 结果), ...],
#         "失败": [(原始数据, 错误信息), ...],
#         "统计": {"总数": n, "成功": x, "失败": y, "重试": z},
#     }
#
# 要求：
#   · 处理函数抛异常时，根据 重试次数 决定重试几次
#   · 遇错即停 = True 时，遇到第一个错误就停止
#   · 错误信息要带上异常类型
#   · 再写几个测试用的处理函数（会失败的那种）
#
# 你的代码：


# ═══════════════════════════════════════════════════════
#  第 5 题  ★★★★★
# ═══════════════════════════════════════════════════════
#
# 综合项目：做一个「学习打卡记录器」。
#
# 功能：
#   1. 打卡（记录日期、科目、时长、备注）
#   2. 查看最近 N 天
#   3. 统计每个科目的总时长
#   4. 找出连续打卡天数（最长连续）
#   5. 导出 CSV
#   6. 数据存 JSON
#
# 要求：
#   · 数据格式自己设计（用字典列表）
#   · 所有函数都要处理异常（文件损坏、数据不合法）
#   · 用 datetime 处理日期
#   · 至少 6 个函数，每个有 docstring
#   · 造 10 条测试数据，跑完整流程
#   · 最后清理测试文件
#
# 你的代码：


# ═══════════════════════════════════════════════════════
#  答案
# ═══════════════════════════════════════════════════════
r'''
第 1 题

    def 规范空白(文本):
        return " ".join(文本.split())

    def 转标题(文本):
        return " ".join(词[0].upper() + 词[1:].lower()
                        for 词 in 文本.split() if 词)

    def 截断(文本, 长度, 后缀="..."):
        if len(文本) <= 长度:
            return 文本
        保留 = 长度 - len(后缀)
        if 保留 <= 0:
            return 后缀[:长度]
        return 文本[:保留] + 后缀

    def 计数(文本, 字符):
        个数 = 0
        for c in 文本:
            if c == 字符:
                个数 += 1
        return 个数

    def 反转每句话(文本):
        结果 = ""
        当前 = ""
        for c in 文本:
            当前 += c
            if c in "。！？.!?":
                结果 += 当前[:-1][::-1] + c
                当前 = ""
        if 当前:
            结果 += 当前[::-1]
        return 结果

    —— 几个点：

       ① `转标题` 不用 `title()` 是因为 `title()` 会把
          "it's" 变成 "It'S"（撇号后面也大写）。

          自己写更可控。

       ② `截断` 要保证「截断后总长度不超过 长度」
          所以要 `长度 - len(后缀)` 算保留几个字符。

       ③ `反转每句话` 里 `当前[:-1][::-1]` 是「去掉句末标点再反转」，
          然后再接上标点。

第 2 题

    import os

    def 统计文件(路径):
        if not os.path.isfile(路径):
            return None

        try:
            with open(路径, "r", encoding="utf-8") as f:
                行们 = f.read().splitlines()
        except (UnicodeDecodeError, OSError):
            return None

        空行 = 0
        注释 = 0
        代码 = 0
        最长 = ""
        最长号 = 0

        for i, 行 in enumerate(行们, 1):
            去掉缩进 = 行.strip()
            if 去掉缩进 == "":
                空行 += 1
            elif 去掉缩进.startswith("#"):
                注释 += 1
            else:
                代码 += 1

            if len(行) > len(最长):
                最长 = 行
                最长号 = i

        return {
            "总行数": len(行们),
            "空行": 空行,
            "注释行": 注释,
            "代码行": 代码,
            "最长行": 最长,
            "最长行号": 最长号,
        }

    —— 注意 `行.strip()` 之后判断，
       这样「缩进的注释」也算注释行。

第 3 题

    import json
    import os
    import csv

    默认配置 = {"主题": "浅色", "字号": 14, "自动保存": True}

    def 读配置(路径):
        if not os.path.isfile(路径):
            写配置(路径, 默认配置)
            return 默认配置.copy()

        try:
            with open(路径, "r", encoding="utf-8") as f:
                配置 = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            # 备份坏文件
            try:
                os.replace(路径, 路径 + ".bak")
            except OSError:
                pass
            写配置(路径, 默认配置)
            return 默认配置.copy()

        if not isinstance(配置, dict):
            写配置(路径, 默认配置)
            return 默认配置.copy()

        结果 = 默认配置.copy()
        结果.update(配置)
        return 结果

    def 写配置(路径, 配置):
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(配置, f, ensure_ascii=False, indent=2)

    def 改配置(路径, 键, 值):
        配置 = 读配置(路径)
        配置[键] = 值
        写配置(路径, 配置)
        return 配置

    def 重置配置(路径):
        写配置(路径, 默认配置)
        return 默认配置.copy()

    def 导出配置(路径, 目标CSV):
        配置 = 读配置(路径)
        with open(目标CSV, "w", encoding="utf-8", newline="") as f:
            写 = csv.writer(f)
            写.writerow(["键", "值"])
            for 键, 值 in 配置.items():
                写.writerow([键, str(值)])
        return len(配置)

    —— `os.replace(路径, 路径 + ".bak")`
       把坏文件改名保留，方便事后查看。

       用 `os.replace` 而不是 `os.rename`，因为前者在目标存在时会覆盖。

第 4 题

    def 批量处理(数据们, 处理函数, 重试次数=0, 遇错即停=False):
        成功 = []
        失败 = []
        重试总数 = 0

        for 数据 in 数据们:
            最后错误 = None
            成功结果 = None

            for 尝试 in range(重试次数 + 1):
                try:
                    成功结果 = 处理函数(数据)
                    最后错误 = None
                    break
                except Exception as e:
                    最后错误 = e
                    if 尝试 < 重试次数:
                        重试总数 += 1

            if 最后错误 is None:
                成功.append((数据, 成功结果))
            else:
                失败.append((数据, f"[{type(最后错误).__name__}] {最后错误}"))
                if 遇错即停:
                    break

        return {
            "成功": 成功,
            "失败": 失败,
            "统计": {
                "总数": len(数据们),
                "成功": len(成功),
                "失败": len(失败),
                "重试": 重试总数,
            },
        }

    —— 测试用的处理函数：

        def 开方(x):
            if x < 0:
                raise ValueError(f"负数不能开方：{x}")
            return x ** 0.5

        def 有时成功(x):
            # 用一个计数器模拟「重试后成功」
            ...

    —— `遇错即停` 时 `break` 跳出的是外层 for 循环 ——
       因为这里的 break 在 for 里（内层是 for 尝试，已经结束了）。

       要小心：`break` 只跳一层。

第 5 题

    import json
    import os
    import csv
    from datetime import datetime, timedelta

    数据文件 = "打卡数据.json"

    def 读记录(路径=数据文件):
        if not os.path.isfile(路径):
            return []
        try:
            with open(路径, "r", encoding="utf-8") as f:
                数据 = json.load(f)
            return 数据 if isinstance(数据, list) else []
        except (json.JSONDecodeError, UnicodeDecodeError, OSError):
            return []

    def 写记录(记录们, 路径=数据文件):
        try:
            with open(路径, "w", encoding="utf-8") as f:
                json.dump(记录们, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    def 打卡(记录们, 科目, 分钟, 备注="", 日期=None):
        if not 科目.strip():
            return None, "科目不能为空"
        try:
            分钟 = int(分钟)
        except (ValueError, TypeError):
            return None, "时长必须是整数"
        if 分钟 <= 0 or 分钟 > 1440:
            return None, "时长必须在 1~1440 分钟之间"

        日期 = 日期 or datetime.now().strftime("%Y-%m-%d")

        记录 = {
            "日期": 日期,
            "科目": 科目.strip(),
            "分钟": 分钟,
            "备注": 备注.strip(),
        }
        记录们.append(记录)
        return 记录, None

    def 最近N天(记录们, n=7):
        今天 = datetime.now().date()
        起始 = (今天 - timedelta(days=n - 1)).strftime("%Y-%m-%d")
        return [r for r in 记录们 if r["日期"] >= 起始]

    def 科目统计(记录们):
        结果 = {}
        for r in 记录们:
            科 = r["科目"]
            结果[科] = 结果.get(科, 0) + r["分钟"]
        return dict(sorted(结果.items(), key=lambda x: -x[1]))

    def 最长连续(记录们):
        if not 记录们:
            return 0
        日期们 = sorted(set(r["日期"] for r in 记录们))

        最长 = 1
        当前 = 1
        for i in range(1, len(日期们)):
            前一天 = datetime.strptime(日期们[i - 1], "%Y-%m-%d").date()
            今天 = datetime.strptime(日期们[i], "%Y-%m-%d").date()
            if (今天 - 前一天).days == 1:
                当前 += 1
                最长 = max(最长, 当前)
            else:
                当前 = 1
        return 最长

    def 导出CSV(记录们, 路径):
        with open(路径, "w", encoding="utf-8", newline="") as f:
            写 = csv.DictWriter(f, fieldnames=["日期", "科目", "分钟", "备注"])
            写.writeheader()
            写.writerows(记录们)

    —— 几个关键点：

       ① `set(r["日期"] for r in 记录们)` 去重
          因为一天可能有多次打卡，连续天数只算一次。

       ② `(今天 - 前一天).days == 1` 判断是否连续

       ③ `记录们` 传进来是**引用**，
          `打卡` 里的 `记录们.append(记录)` 会改到外面 ——
          这是有意的（就地添加），但要在 docstring 里说明。

    —— 测试流程：

        记录 = []
        for i, (科, 分) in enumerate([
            ("数学", 60), ("语文", 45), ("英语", 30),
            ("数学", 90), ("语文", 60), ("英语", 40),
            ("数学", 50), ("语文", 70), ("英语", 35),
            ("数学", 80),
        ]):
            日期 = (datetime.now() - timedelta(days=9 - i)).strftime("%Y-%m-%d")
            打卡(记录, 科, 分, f"第 {i+1} 天", 日期)

        写记录(记录)
        print("最近 7 天：", len(最近N天(记录, 7)), "条")
        print("科目统计：", 科目统计(记录))
        print("最长连续：", 最长连续(记录), "天")
        导出CSV(记录, "打卡.csv")
        os.remove(数据文件)
        os.remove("打卡.csv")
'''
