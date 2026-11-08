r'''
════════════════════════════════════════════════════════
  L5 · 第 3 课 · 用法 4        综合项目：文件清单工具
════════════════════════════════════════════════════════

需求：给一个目录，列出里面所有文件，统计信息，生成报告。

这个项目把「目录遍历 + 字符串处理 + 文件写入」串起来。

────────────────────────────────────────────────────────
【第一件事：怎么遍历目录】
════════════════════════════════════════════════════════

        import os

    ── 列出目录内容 ──

        os.listdir("某个目录")
        → ['a.txt', 'b.py', '子目录']

        只给名字，不含路径。

    ── 更常用：os.scandir ──

        with os.scandir("某个目录") as 项们:
            for 项 in 项们:
                print(项.name, 项.is_file(), 项.is_dir())

        每项有 `.name`、`.path`、`.is_file()`、`.is_dir()`、`.stat()`。

        比 `os.listdir` + `os.path.isfile` 快（信息一次拿到）。

    ── 递归遍历（含子目录）──

        for 根, 子目录们, 文件们 in os.walk("某个目录"):
            for 文件名 in 文件们:
                完整路径 = os.path.join(根, 文件名)

        `os.walk` 会自动钻到每一层子目录。

    ── 拿文件信息 ──

        os.path.getsize(路径)           字节数
        os.path.getmtime(路径)          修改时间（时间戳）
        os.path.splitext(路径)          拆成 (主干, 扩展名)

    ── 时间戳转人话 ──

        import time
        time.strftime("%Y-%m-%d %H:%M", time.localtime(时间戳))

────────────────────────────────────────────────────────
【第二件事：格式化文件大小】
════════════════════════════════════════════════════════

    文件大小是字节数，直接显示「1234567 字节」不好读。

    ── 转成 KB / MB / GB ──

        def 人性化大小(字节):
            """把字节数转成易读的字符串。"""
            单位们 = ["B", "KB", "MB", "GB", "TB"]
            值 = float(字节)
            for 单位 in 单位们:
                if 值 < 1024:
                    if 单位 == "B":
                        return f"{int(值)} B"
                    return f"{值:.1f} {单位}"
                值 /= 1024
            return f"{值:.1f} PB"

    ── 为什么是 1024 不是 1000 ──

        计算机用二进制，1 KB = 2^10 = 1024 字节。

        （硬盘厂商喜欢用 1000，所以「买 1TB 硬盘只有 931GB」
          就是这个原因 —— 两边算法不同。）

    ── 测试 ──

        人性化大小(500)          → "500 B"
        人性化大小(1500)         → "1.5 KB"
        人性化大小(1234567)      → "1.2 MB"
        人性化大小(5 * 1024**3)  → "5.0 GB"

────────────────────────────────────────────────────────
【第三件事：按扩展名分类】
════════════════════════════════════════════════════════

    ── 取扩展名 ──

        os.path.splitext("report.tar.gz")
        → ('report.tar', '.gz')

        ⚠ 只拆最后一个点。所以 `.tar.gz` 只会认成 `.gz`。

        要正确处理双扩展名，得自己判断：

            def 真扩展名(文件名):
                部分 = 文件名.split(".")
                if len(部分) >= 3 and 部分[-2] in ("tar", "user"):
                    return "." + ".".join(部分[-2:])
                return os.path.splitext(文件名)[1]

        （大多数场景不需要这么细。）

    ── 分类 ──

        类别表 = {
            ".py": "Python",
            ".txt": "文本",
            ".md": "Markdown",
            ".csv": "表格",
            ".json": "数据",
            ".jpg": "图片",
            ".png": "图片",
            ".zip": "压缩包",
        }

        扩展名 = os.path.splitext(文件名)[1].lower()
        类别 = 类别表.get(扩展名, "其他")

    ── 用字典做「映射表」──

        比 if-elif 链清楚得多，而且加一项只要加一行。

────────────────────────────────────────────────────────
【第四件事：生成报告】
════════════════════════════════════════════════════════

    ── 控制台报告 ──

        用中文字符对齐那套（L5 第 1 课讲过）：

            def 显示宽度(s):
                return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in s)

            def 补齐(s, 宽, 右=False):
                差 = 宽 - 显示宽度(s)
                if 差 <= 0:
                    return s
                return (" " * 差 + s) if 右 else (s + " " * 差)

    ── 文件报告（CSV）──

        用 csv.DictWriter，字段是：文件名、大小、类别、修改时间

    ── 文件报告（JSON）──

        用 json.dump，保留完整信息（包括分类统计）

    ── 为什么要生成两种格式 ──

        · CSV 给人看（Excel 打开）
        · JSON 给程序读（下次分析用）

        **同一次分析，输出多种格式，是很常见的需求。**

────────────────────────────────────────────────────────
【第五件事：健壮性】
════════════════════════════════════════════════════════

    ── 目录不存在 ──

        if not os.path.isdir(路径):
            print("目录不存在")
            return

    ── 没权限读某个文件 ──

        try:
            大小 = os.path.getsize(路径)
        except OSError:
            大小 = 0

    ── 符号链接（快捷方式）──

        `os.path.isfile` 对符号链接会返回它指向的东西的类型。

        想判断「是不是链接本身」用 `os.path.islink`。

    ── 大目录会很慢 ──

        遍历 10 万个文件要几秒。

        如果只是统计，不需要 `stat` 每个文件，
        可以只 `listdir` 拿名字。

        **性能问题在文件操作里很常见，因为 I/O 比内存慢几个数量级。**

────────────────────────────────────────────────────────
【一个真实的用途】
════════════════════════════════════════════════════════

    这个工具实际能用来：

        · 找出「占空间最多」的文件
        · 统计「这个项目有多少行代码」
        · 生成「交付清单」
        · 分析「哪种文件类型最多」

    稍加改动就能变成实用工具。

    **L5 学完，你已经能写「能解决实际问题」的程序了。**
'''

# ═══════════════════════════════════════
#  完整项目
# ═══════════════════════════════════════

import os
import csv
import json
import time

类别表 = {
    ".py": "Python",
    ".txt": "文本",
    ".md": "Markdown",
    ".csv": "表格",
    ".json": "数据",
    ".log": "日志",
    ".jpg": "图片",
    ".png": "图片",
    ".zip": "压缩包",
}


def 人性化大小(字节):
    """字节数转易读字符串。"""
    单位们 = ["B", "KB", "MB", "GB", "TB"]
    值 = float(字节)
    for 单位 in 单位们:
        if 值 < 1024:
            if 单位 == "B":
                return f"{int(值)} B"
            return f"{值:.1f} {单位}"
        值 /= 1024
    return f"{值:.1f} PB"


def 文件信息(路径):
    """返回单个文件的信息字典。"""
    文件名 = os.path.basename(路径)
    主干, 扩展名 = os.path.splitext(文件名)
    扩展名 = 扩展名.lower()

    try:
        大小 = os.path.getsize(路径)
        修改时间 = os.path.getmtime(路径)
    except OSError:
        return None

    return {
        "文件名": 文件名,
        "扩展名": 扩展名 or "(无)",
        "类别": 类别表.get(扩展名, "其他"),
        "大小": 大小,
        "大小文本": 人性化大小(大小),
        "修改时间": time.strftime("%Y-%m-%d %H:%M",
                                 time.localtime(修改时间)),
    }


def 收集文件(目录, 递归=True):
    """收集目录下所有文件的信息。"""
    结果 = []

    if not os.path.isdir(目录):
        return 结果

    if 递归:
        for 根, 子目录们, 文件们 in os.walk(目录):
            for 文件名 in 文件们:
                信息 = 文件信息(os.path.join(根, 文件名))
                if 信息:
                    信息["相对路径"] = os.path.relpath(
                        os.path.join(根, 文件名), 目录)
                    结果.append(信息)
    else:
        for 名 in os.listdir(目录):
            路径 = os.path.join(目录, 名)
            if os.path.isfile(路径):
                信息 = 文件信息(路径)
                if 信息:
                    信息["相对路径"] = 名
                    结果.append(信息)

    return 结果


def 显示宽度(s):
    return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in s)


def 补齐(s, 宽, 右=False):
    差 = 宽 - 显示宽度(s)
    if 差 <= 0:
        return s
    return (" " * 差 + s) if 右 else (s + " " * 差)


def 打印报告(目录, 文件们):
    print("=" * 70)
    print("文件清单报告".center(66))
    print("=" * 70)
    print(f"  目录：{os.path.abspath(目录)}")
    print(f"  文件数：{len(文件们)}")

    if not 文件们:
        print("  （没有文件）")
        print("=" * 70)
        return

    总大小 = sum(f["大小"] for f in 文件们)
    print(f"  总大小：{人性化大小(总大小)}")
    print("-" * 70)

    # 按类别统计
    类别统计 = {}
    for f in 文件们:
        类 = f["类别"]
        if 类 not in 类别统计:
            类别统计[类] = {"个数": 0, "大小": 0}
        类别统计[类]["个数"] += 1
        类别统计[类]["大小"] += f["大小"]

    print(f"  {'类别':<10}{'个数':>6}{'大小':>12}")
    print("  " + "-" * 28)
    for 类, 数据 in sorted(类别统计.items(),
                           key=lambda x: -x[1]["大小"]):
        print(f"  {类:<10}{数据['个数']:>6}{人性化大小(数据['大小']):>12}")

    print("-" * 70)

    # 最大的 5 个文件
    print("  最大的 5 个文件：")
    for f in sorted(文件们, key=lambda x: -x["大小"])[:5]:
        print(f"    {补齐(f['相对路径'], 40)}"
              f"{f['大小文本']:>10}  {f['修改时间']}")

    print("=" * 70)


def 写CSV(路径, 文件们):
    """写 CSV 报告。"""
    字段 = ["相对路径", "文件名", "扩展名", "类别", "大小", "大小文本", "修改时间"]
    with open(路径, "w", encoding="utf-8", newline="") as f:
        写 = csv.DictWriter(f, fieldnames=字段, extrasaction="ignore")
        写.writeheader()
        写.writerows(文件们)
    return len(文件们)


def 写JSON(路径, 目录, 文件们):
    """写 JSON 报告。"""
    类别统计 = {}
    for f in 文件们:
        if f["类别"] not in 类别统计:
            类别统计[f["类别"]] = {"个数": 0, "总字节": 0}
        类别统计[f["类别"]]["个数"] += 1
        类别统计[f["类别"]]["总字节"] += f["大小"]

    报告 = {
        "目录": os.path.abspath(目录),
        "生成时间": time.strftime("%Y-%m-%d %H:%M:%S"),
        "文件总数": len(文件们),
        "总字节": sum(f["大小"] for f in 文件们),
        "类别统计": 类别统计,
        "文件列表": 文件们,
    }

    with open(路径, "w", encoding="utf-8") as f:
        json.dump(报告, f, ensure_ascii=False, indent=2)
    return 报告


# ── 演示 ──

演示目录 = "演示文件目录"
if not os.path.isdir(演示目录):
    os.makedirs(演示目录)

# 造几个文件
演示文件们 = {
    "readme.txt": "这是一个测试文件。\n" * 20,
    "script.py": "print('hello')\n" * 50,
    "data.csv": "a,b,c\n1,2,3\n" * 30,
    "notes.md": "# 笔记\n" * 10,
    "unknown.xyz": "未知类型\n" * 5,
}
for 名, 内容 in 演示文件们.items():
    with open(os.path.join(演示目录, 名), "w", encoding="utf-8") as f:
        f.write(内容)

子目录 = os.path.join(演示目录, "子目录")
if not os.path.isdir(子目录):
    os.makedirs(子目录)
with open(os.path.join(子目录, "nested.log"), "w", encoding="utf-8") as f:
    f.write("日志内容\n" * 100)

print("① 人性化大小")
for 字节 in [500, 1500, 1234567, 5 * 1024**3]:
    print(f"  {字节:>12} 字节 → {人性化大小(字节)}")

print("\n② 收集文件（不递归）")
文件们 = 收集文件(演示目录, 递归=False)
for f in 文件们:
    print(f"  {f['文件名']:<16}{f['类别']:<8}{f['大小文本']:>10}")

print("\n③ 收集文件（递归）")
全部 = 收集文件(演示目录, 递归=True)
print(f"  共 {len(全部)} 个文件")

print("\n④ 完整报告")
打印报告(演示目录, 全部)

print("\n⑤ 写 CSV 报告")
CSV路径 = "文件清单.csv"
数量 = 写CSV(CSV路径, 全部)
with open(CSV路径, "r", encoding="utf-8") as f:
    print("  CSV 前 3 行：")
    for i, 行 in enumerate(f):
        if i >= 3:
            break
        print("    " + 行.rstrip())

print("\n⑥ 写 JSON 报告")
JSON路径 = "文件清单.json"
报告 = 写JSON(JSON路径, 演示目录, 全部)
print(f"  文件总数：{报告['文件总数']}")
print(f"  总字节：{报告['总字节']}")
print("  类别统计：")
for 类, 数据 in 报告["类别统计"].items():
    print(f"    {类}：{数据['个数']} 个，{人性化大小(数据['总字节'])}")

print("\n⑦ 读回 JSON 验证")
with open(JSON路径, "r", encoding="utf-8") as f:
    读回 = json.load(f)
print("  文件列表条数：", len(读回["文件列表"]))
print("  第一项：", 读回["文件列表"][0]["文件名"])

print("\n⑧ 清理")
for f in os.listdir(演示目录):
    路径 = os.path.join(演示目录, f)
    if os.path.isfile(路径):
        os.remove(路径)
if os.path.isdir(子目录):
    for f in os.listdir(子目录):
        os.remove(os.path.join(子目录, f))
    os.rmdir(子目录)
os.rmdir(演示目录)
os.remove(CSV路径)
os.remove(JSON路径)
print("  演示文件和目录已清理")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  代码行数统计器
# ─────────────────────────────────────────
#
# 写一个 `def 统计代码(目录)`，递归遍历目录，统计所有 .py 文件：
#
#   · 总文件数
#   · 总行数
#   · 总字符数
#   · 空行数 / 注释行数（以 # 开头）/ 代码行数
#   · 最长的文件（文件名 + 行数）
#
# 要求：
#   · 用 os.walk
#   · 跳过空行和纯空白行
#   · 输出一张表
#   · 自己造几个测试 .py 文件，测完删除
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  文件去重（按大小先筛）
# ─────────────────────────────────────────
#
# 找出目录里「大小完全相同」的文件（可能是重复文件）：
#
#   A. def 按大小分组(目录)   返回 {大小: [路径, ...]}，只保留有多个的
#   B. def 找重复(目录)       在大小相同的组里，再比较内容
#
# 要求：
#   · 先用大小筛，能排除 99% 的不重复文件
#   · 真正比较内容时才读文件
#   · 说明：为什么不能直接比内容（性能角度）
#   · 测试：造几个内容相同和不同的文件
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.  os.path.splitext("report.tar.gz")
#   B.  os.path.splitext("README")
#   C.  os.path.basename("/home/user/a.txt")
#   D.  os.path.join("a", "b", "c.txt")
#   E.  人性化大小的 2048 字节
#   F.  人性化大小的 1023 字节
#   G.  len("文件".encode("utf-8"))
#   H.  json.dumps({"a": [1, 2]})
#   I.  os.path.exists("一个肯定不存在的文件.xyz")
#   J.  "a.py".lower().endswith(".py")
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 统计代码(目录):
        """统计目录下所有 .py 文件。"""
        if not os.path.isdir(目录):
            return None

        统计 = {
            "文件数": 0,
            "总行数": 0,
            "总字符": 0,
            "空行": 0,
            "注释行": 0,
            "代码行": 0,
        }
        最长文件 = ("", 0)

        for 根, 子目录们, 文件们 in os.walk(目录):
            for 文件名 in 文件们:
                if not 文件名.lower().endswith(".py"):
                    continue

                路径 = os.path.join(根, 文件名)
                try:
                    with open(路径, "r", encoding="utf-8") as f:
                        行们 = f.read().splitlines()
                except (OSError, UnicodeDecodeError):
                    continue

                统计["文件数"] += 1
                统计["总行数"] += len(行们)

                for 行 in 行们:
                    统计["总字符"] += len(行)
                    if 行.strip() == "":
                        统计["空行"] += 1
                    elif 行.strip().startswith("#"):
                        统计["注释行"] += 1
                    else:
                        统计["代码行"] += 1

                if len(行们) > 最长文件[1]:
                    最长文件 = (文件名, len(行们))

        统计["最长文件"] = 最长文件[0]
        统计["最长文件行数"] = 最长文件[1]
        return 统计


    —— 测试：

        print(统计代码("./"))

    输出（大概是）：
        {'文件数': 4, '总行数': 1200, '总字符': 45000,
         '空行': 200, '注释行': 150, '代码行': 850,
         '最长文件': '...', '最长文件行数': 500}

    —— 几个点：

       ① `文件名.lower().endswith(".py")`
          处理 `.PY` 这种大写扩展名。

       ② `try/except` 包住读文件的代码
          有些文件可能是别的编码，或者没权限。

          读不了就跳过，不中断整个统计。

       ③ 分类顺序：先判空行，再判注释
          因为空行的 `strip()` 是空字符串，
          而 `"".startswith("#")` 是 False，
          所以顺序其实不影响。但「先判空」更清楚。

       ④ `行.strip().startswith("#")`
          处理「缩进的注释」（函数里的 # 前面有空格）。

    —— 这个工具的实际用途：

       `统计代码(项目目录)` 就能知道项目有多少行代码。

       很多项目管理工具都有这个功能。

题 2
    def 按大小分组(目录):
        """返回 {大小: [路径, ...]}，只保留有多个的。"""
        分组 = {}
        for 根, 子目录们, 文件们 in os.walk(目录):
            for 文件名 in 文件们:
                路径 = os.path.join(根, 文件名)
                try:
                    大小 = os.path.getsize(路径)
                except OSError:
                    continue
                分组.setdefault(大小, []).append(路径)

        # 只留「有多个」的组
        return {大小: 路径们 for 大小, 路径们 in 分组.items()
                if len(路径们) > 1}


    def 找重复(目录):
        """找出内容完全相同的文件。"""
        结果 = []

        for 大小, 路径们 in 按大小分组(目录).items():
            # 在这一组里，按内容再分组
            内容组 = {}
            for 路径 in 路径们:
                try:
                    with open(路径, "rb") as f:
                        内容 = f.read()
                except OSError:
                    continue
                内容组.setdefault(内容, []).append(路径)

            for 内容, 同内容们 in 内容组.items():
                if len(同内容们) > 1:
                    结果.append({
                        "大小": 大小,
                        "文件": 同内容们,
                    })

        return 结果


    —— 「为什么要先用大小筛」：

       比较内容的成本：

           读一个 1MB 的文件 → 约 1 毫秒
           1000 个文件全读一遍 → 1 秒

       而读文件大小：

           `os.path.getsize()` 只查元数据，不读内容 → 微秒级
           1000 个文件 → 几毫秒

       **差 1000 倍以上。**

       而「大小不同 → 内容肯定不同」，
       所以先用大小分组，能排除绝大多数。

       假设 1000 个文件里只有 10 对是重复的：
           不筛：读 1000 个文件
           先筛：只读那几个大小相同的文件（可能 20 个）

       差 50 倍。

    —— 还可以进一步优化：

       ① 先比「前 1KB」（大部分重复文件前 1KB 就不同）
       ② 用哈希（MD5/SHA1）代替全文比较
          哈希一次算完，之后比较哈希值就行

          但哈希本身也要读全文，所以只适合「多次比较」。

    —— 一个实际问题：

       这个工具在真实场景里叫「重复文件查找器」，
       有很多现成软件（比如 dupeGuru）。

       自己写主要是练手。

题 3
    A.  os.path.splitext("report.tar.gz")
        → ('report.tar', '.gz')

        只拆最后一个点。

    B.  os.path.splitext("README")
        → ('README', '')

        没有扩展名时，第二部分是空字符串。

    C.  os.path.basename("/home/user/a.txt")
        → 'a.txt'

    D.  os.path.join("a", "b", "c.txt")
        → 'a/b/c.txt'（Linux/macOS）
        → 'a\\b\\c.txt'（Windows）

        os.path.join 会用当前系统的分隔符。

    E.  2048 字节 → "2.0 KB"

    F.  1023 字节 → "1023 B"

        因为 1023 < 1024，还是按 B 显示。

    G.  len("文件".encode("utf-8"))
        → 6

        两个中文，各 3 字节。

    H.  json.dumps({"a": [1, 2]})
        → '{"a": [1, 2]}'

    I.  os.path.exists("一个肯定不存在的文件.xyz")
        → False

    J.  "a.py".lower().endswith(".py")
        → True

    —— 汇总：

           A  ('report.tar', '.gz')
           B  ('README', '')
           C  'a.txt'
           D  'a/b/c.txt' 或 'a\\b\\c.txt'
           E  '2.0 KB'
           F  '1023 B'
           G  6
           H  '{"a": [1, 2]}'
           I  False
           J  True

    —— 最容易错的：

       ① A：以为会拆出 ('.tar.gz')
          实际只拆最后一个点。

       ② F：以为 1023 字节是 "1.0 KB"
          1023 < 1024，还是 B。

       ③ D：路径分隔符是系统相关的
          写代码时用 `os.path.join`，不要手写 `/` 或 `\`。

          （Python 里 `/` 在大多数情况也能用，
            但 `os.path.join` 更规范。）
'''
