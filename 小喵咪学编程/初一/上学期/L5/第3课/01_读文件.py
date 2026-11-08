r'''
════════════════════════════════════════════════════════
  L5 · 第 3 课 · 用法 1        读文件
════════════════════════════════════════════════════════

前四级所有数据都在内存里，程序一关就没了。

文件让数据活下来。

────────────────────────────────────────────────────────
【open 的基本形状】
════════════════════════════════════════════════════════

        f = open("data.txt", "r", encoding="utf-8")
        内容 = f.read()
        f.close()

    三个参数：

        文件名          可以是相对路径或绝对路径
        "r"             模式：r 读、w 写、a 追加
        encoding="utf-8" 编码，中文必写

    ── 必须 close ──

        不关文件会怎样：
            · 数据可能没写完（缓冲没刷新）
            · 系统资源泄漏（打开的文件句柄有上限）
            · Windows 上文件被占用，别的程序改不了

    ── 但手动 close 容易忘 ──

        而且中间如果报错，close 就不会执行了。

────────────────────────────────────────────────────────
【推荐写法：with】
════════════════════════════════════════════════════════

        with open("data.txt", "r", encoding="utf-8") as f:
            内容 = f.read()
        # 出了 with 块，文件自动关闭

    ── with 的好处 ──

        ① 不用记着 close
        ② 就算中间报错，也会正确关闭

        **几乎所有文件操作都该用 with。**

    ── 缩进范围就是「文件打开的时间」──

        with open(...) as f:
            行1 = f.readline()
        行2 = f.readline()      ← 这里文件已经关了，会报错
                                   ValueError: I/O operation on closed file

────────────────────────────────────────────────────────
【三种读法】
════════════════════════════════════════════════════════

    假设 data.txt 内容是：

        第一行
        第二行
        第三行

    ── ① read()：全读成一个字符串 ──

        with open(...) as f:
            内容 = f.read()

        内容 = "第一行\n第二行\n第三行\n"

    ── ② readlines()：全读成一个列表 ──

        with open(...) as f:
            行们 = f.readlines()

        行们 = ['第一行\n', '第二行\n', '第三行\n']

        ⚠ 每行末尾的 `\n` 还在！

        要去掉：`[行.strip() for 行 in 行们]`

    ── ③ 逐行遍历（推荐）──

        with open(...) as f:
            for 行 in f:
                行 = 行.strip()
                print(行)

        **这是处理大文件的标准写法。**

    ── 为什么推荐逐行 ──

        一个 1GB 的日志文件，`read()` 会把整个 1GB 读进内存。

        逐行读只占一行的内存，能处理任意大的文件。

        **内存占用：read() = 文件大小，逐行 = 一行大小。**

────────────────────────────────────────────────────────
【编码：中文必写】
════════════════════════════════════════════════════════

        open("data.txt", encoding="utf-8")

    ── 不写会怎样 ──

        Windows 上 Python 默认用系统的编码（可能是 GBK）。

        如果文件是 UTF-8 存的，读的时候用 GBK 解 → 乱码或报错：

            UnicodeDecodeError: 'gbk' codec can't decode byte ...

        **养成「open 必写 encoding="utf-8"」的习惯。**

    ── 写文件时也一样 ──

        open("out.txt", "w", encoding="utf-8")

    ── 一个常见的坑：BOM ──

        Windows 记事本保存 UTF-8 时，可能在开头加一个 BOM（\ufeff）。

        读进来第一行会变成 "\ufeff第一行"。

        解决：用 `encoding="utf-8-sig"` 读，会自动跳过 BOM。

────────────────────────────────────────────────────────
【路径】
════════════════════════════════════════════════════════

    ── 相对路径：相对于「运行时所在目录」──

        open("data.txt")            当前目录
        open("数据/data.txt")        当前目录下的 数据/ 子目录
        open("../data.txt")          上一级目录

    ⚠ 相对路径是相对于「你运行程序时所在的目录」，
      不是「脚本文件所在的目录」。

      这意味着：在不同目录下运行同一个脚本，读到的文件可能不同。

    ── 绝对路径 ──

        open("C:/Users/test/data.txt")      Windows

    （正斜杠 `/` 在 Python 里通用，不用写 `\\`。）

    ── 更稳的做法：基于脚本位置 ──

        import os

        目录 = os.path.dirname(os.path.abspath(__file__))
        路径 = os.path.join(目录, "data.txt")

        with open(路径, encoding="utf-8") as f:
            ...

        `__file__` 是当前脚本的路径。

        这样不管从哪里运行，都能找到同目录下的文件。

        （`import os` 是 L5 第 5 课的内容，这里先知道有这么个写法。）

────────────────────────────────────────────────────────
【先判断文件存在】
════════════════════════════════════════════════════════

        import os

        if os.path.exists("data.txt"):
            with open("data.txt", encoding="utf-8") as f:
                ...
        else:
            print("文件不存在")

    ── 但「先判断再打开」有个隐患 ──

        判断和打开之间，文件可能被别的程序删掉。

        更稳的做法是直接打开，用 try/except 捕获：

            try:
                with open("data.txt", encoding="utf-8") as f:
                    ...
            except FileNotFoundError:
                print("文件不存在")

        （try/except 是 L5 第 4 课的内容。）

    ── 常用判断 ──

        os.path.exists(路径)       存在吗（文件或目录）
        os.path.isfile(路径)       是文件吗
        os.path.isdir(路径)        是目录吗
        os.path.getsize(路径)      大小（字节）

────────────────────────────────────────────────────────
【读文件会遇到的错误】
════════════════════════════════════════════════════════

    ┌────────────────────────┬──────────────────────────────┐
    │ FileNotFoundError      │ 文件不存在 / 路径写错        │
    │ PermissionError        │ 没权限（或者文件被占用）     │
    │ IsADirectoryError      │ 打开的是个目录               │
    │ UnicodeDecodeError     │ 编码不对                     │
    └────────────────────────┴──────────────────────────────┘

    ── 最常见的是 FileNotFoundError ──

        90% 的情况是「路径不对」。

        排查方法：把 `os.path.abspath(路径)` 打出来，看它到底在哪找。

            print(os.path.abspath("data.txt"))

────────────────────────────────────────────────────────
【一个完整的读文件函数】
════════════════════════════════════════════════════════

        def 读行们(路径, 去空白=True):
            """读文件所有行，返回列表。"""
            行们 = []
            with open(路径, "r", encoding="utf-8") as f:
                for 行 in f:
                    if 去空白:
                        行 = 行.strip()
                    if 行:                     ← 跳过空行
                        行们.append(行)
            return 行们

    ── 三个设计决定 ──

        ① `去空白=True` 默认去空白（大多数场景需要）
        ② 跳过空行（可选，看需求）
        ③ 用逐行读（能处理大文件）

    —— 这种「读 → 清洗 → 返回列表」的函数，
       几乎每个项目都会写一个。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

import os

# 准备一个演示文件
演示文件 = "演示数据.txt"
with open(演示文件, "w", encoding="utf-8") as f:
    f.write("第一行：苹果 5.5\n")
    f.write("第二行：香蕉 3.2\n")
    f.write("第三行：橘子 4.0\n")

print("① 准备演示文件")
print("  文件：", os.path.abspath(演示文件))
print("  大小：", os.path.getsize(演示文件), "字节")

print("\n② read()：全读成一个字符串")
with open(演示文件, "r", encoding="utf-8") as f:
    内容 = f.read()
print("  repr：", repr(内容))
print("  长度：", len(内容))

print("\n③ readlines()：读成列表")
with open(演示文件, "r", encoding="utf-8") as f:
    行们 = f.readlines()
print("  ", 行们)
print("  ↑ 每行末尾都带 \\n")

print("\n④ 去掉 \\n")
with open(演示文件, "r", encoding="utf-8") as f:
    干净 = [行.strip() for 行 in f]
print("  ", 干净)

print("\n⑤ 逐行遍历（推荐）")
with open(演示文件, "r", encoding="utf-8") as f:
    for i, 行 in enumerate(f, 1):
        print(f"  第 {i} 行：{行.strip()}")

print("\n⑥ with 之外文件已关闭")
with open(演示文件, "r", encoding="utf-8") as f:
    第一行 = f.readline()
print("  读到：", repr(第一行))
print("  再读会报 ValueError（文件已关闭）")

print("\n⑦ 判断文件是否存在")
print("  演示数据.txt 存在：", os.path.exists(演示文件))
print("  不存在的文件：    ", os.path.exists("根本没有.txt"))
print("  是文件吗：        ", os.path.isfile(演示文件))
print("  是目录吗：        ", os.path.isdir(演示文件))

print("\n⑧ 读文件并做处理")


def 读商品(路径):
    """读 '名字 价格' 格式的文件，返回 [(名字, 价格), ...]。"""
    结果 = []
    with open(路径, "r", encoding="utf-8") as f:
        for 行 in f:
            行 = 行.strip()
            if not 行:
                continue
            # 格式："第一行：苹果 5.5"
            部分 = 行.split("：")
            if len(部分) != 2:
                continue
            名字价格 = 部分[1].split()
            if len(名字价格) != 2:
                continue
            结果.append((名字价格[0], float(名字价格[1])))
    return 结果


商品 = 读商品(演示文件)
print("  读到", len(商品), "条：")
for 名, 价 in 商品:
    print(f"    {名}：{价} 元")

print("\n⑨ 读汉字编码")
with open(演示文件, "rb") as f:      # rb = 二进制读
    前几字节 = f.read(30)
print("  前 30 字节：", 前几字节)
print("  ↑ 中文在 UTF-8 里占 3 字节")

print("\n⑩ 常见错误演示")
print("  读不存在的文件 → FileNotFoundError")
print("  读目录 → IsADirectoryError")
print("  编码不对 → UnicodeDecodeError")

print("\n⑪ 统计文件信息")


def 文件信息(路径):
    """返回文件的基本信息。"""
    if not os.path.exists(路径):
        return {"存在": False}

    信息 = {
        "存在": True,
        "绝对路径": os.path.abspath(路径),
        "大小(字节)": os.path.getsize(路径),
    }

    with open(路径, "r", encoding="utf-8") as f:
        内容 = f.read()
    信息["字符数"] = len(内容)
    信息["行数"] = len(内容.splitlines())
    信息["字节数(重新编码)"] = len(内容.encode("utf-8"))
    return 信息


for 键, 值 in 文件信息(演示文件).items():
    print(f"  {键}：{值}")

# 清理演示文件
os.remove(演示文件)
print("\n⑫ 演示文件已删除：", not os.path.exists(演示文件))


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  文件读取工具
# ─────────────────────────────────────────
#
# 写这几个函数（都用 try/except 之外的判断方式）：
#
#   A. def 读全部(路径)         返回所有行（去掉换行，跳过空行）
#   B. def 读第N行(路径, n)     返回第 n 行（n 从 1 开始），越界返回 None
#   C. def 读最后N行(路径, n)   返回最后 n 行
#   D. def 搜索(路径, 关键词)   返回含关键词的行（带行号）
#
# 要求：
#   · 都处理「文件不存在」的情况（返回空列表或 None）
#   · 自己创建测试文件（用 with open 写几行）
#   · 测试完删除测试文件
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  统计文件
# ─────────────────────────────────────────
#
# 写一个 `def 统计文本文件(路径)`，返回：
#
#     {
#         "行数": 10,
#         "非空行数": 8,
#         "字符数": 350,
#         "单词数": 60,
#         "最长行": "...",
#         "最长行的字符数": 45,
#         "平均行长": 35.0,
#     }
#
# 要求：
#   · 文件不存在时返回 None
#   · 记录文件里最长的行（如果有并列，取第一个）
#   · 用一个中英混合的测试文件验证
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
# 假设 data.txt 内容正好是："a\nb\nc\n"
#
#   A.  with open("data.txt", encoding="utf-8") as f:
#           内容 = f.read()
#       print(repr(内容))
#
#   B.  with open("data.txt", encoding="utf-8") as f:
#           行们 = f.readlines()
#       print(行们)
#
#   C.  with open("data.txt", encoding="utf-8") as f:
#           行们 = [x.strip() for x in f]
#       print(行们)
#
#   D.  with open("data.txt", encoding="utf-8") as f:
#           行们 = [x.strip() for x in f]
#       print(len(行们))
#
#   E.  print(len("中文"))
#       print(len("中文".encode("utf-8")))
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    import os


    def 读全部(路径):
        """读所有行，去换行，跳过空行。"""
        if not os.path.isfile(路径):
            return []
        结果 = []
        with open(路径, "r", encoding="utf-8") as f:
            for 行 in f:
                行 = 行.strip()
                if 行:
                    结果.append(行)
        return 结果


    def 读第N行(路径, n):
        """返回第 n 行（从 1 开始），越界返回 None。"""
        if n < 1 or not os.path.isfile(路径):
            return None
        with open(路径, "r", encoding="utf-8") as f:
            for i, 行 in enumerate(f, 1):
                if i == n:
                    return 行.strip()
        return None


    def 读最后N行(路径, n):
        """返回最后 n 行。"""
        if n < 1 or not os.path.isfile(路径):
            return []
        所有行 = 读全部(路径)
        return 所有行[-n:]


    def 搜索(路径, 关键词):
        """返回 [(行号, 行内容), ...]。"""
        if not os.path.isfile(路径):
            return []
        结果 = []
        with open(路径, "r", encoding="utf-8") as f:
            for i, 行 in enumerate(f, 1):
                行 = 行.strip()
                if 关键词 in 行:
                    结果.append((i, 行))
        return 结果


    —— 测试：

        测试文件 = "test_临时.txt"
        with open(测试文件, "w", encoding="utf-8") as f:
            f.write("第一行\n\n第三行\n第四行 Python\n第五行\n")

        print(读全部(测试文件))
        → ['第一行', '第三行', '第四行 Python', '第五行']

        print(读第N行(测试文件, 2))
        → ''

        ⚠ 注意第 2 行是空行，`行.strip()` 得到 ""。
          所以返回的是空字符串，不是 None。

          这说明「读第 N 行」和「读全部（跳过空行）」的口径不同 ——
          前者是「文件里的第 N 行」，后者是「非空行的列表」。

          **函数名要说清楚是哪种口径。**

        print(读最后N行(测试文件, 2))
        → ['第四行 Python', '第五行']

        print(搜索(测试文件, "Python"))
        → [(4, '第四行 Python')]

        os.remove(测试文件)

    —— 几个设计点：

       ① 每个函数都先检查 `os.path.isfile`
          不存在就返回空值，不抛异常。

          —— 这是「宽容」的设计。
             也可以用 try/except 让异常传出去，看调用方需求。

       ② `读最后N行` 复用了 `读全部`
          简单的复用，虽然不是最高效（大文件会全读一遍）。

          高效版要「从文件末尾倒着读」，很麻烦。
          除非文件特别大，不值得。

       ③ `enumerate(f, 1)` 直接在文件对象上用
          文件对象是可迭代的，每轮给一行。

题 2
    import os


    def 统计文本文件(路径):
        """统计文本文件的各种指标。"""
        if not os.path.isfile(路径):
            return None

        with open(路径, "r", encoding="utf-8") as f:
            内容 = f.read()

        行们 = 内容.splitlines()
        非空行 = [行 for 行 in 行们 if 行.strip()]

        最长行 = ""
        for 行 in 行们:
            if len(行) > len(最长行):
                最长行 = 行

        总长 = sum(len(行) for 行 in 行们)

        return {
            "行数": len(行们),
            "非空行数": len(非空行),
            "字符数": len(内容),
            "单词数": len(内容.split()),
            "最长行": 最长行,
            "最长行的字符数": len(最长行),
            "平均行长": 总长 / len(行们) if 行们 else 0,
        }


    —— 测试：

        测试文件 = "统计测试.txt"
        with open(测试文件, "w", encoding="utf-8") as f:
            f.write("Hello World\n")
            f.write("\n")
            f.write("这是一行中文\n")
            f.write("Python is fun\n")

        结果 = 统计文本文件(测试文件)
        for 键, 值 in 结果.items():
            print(f"  {键}：{repr(值)}")

        os.remove(测试文件)

    —— 输出：
           行数：4
           非空行数：3
           字符数：38
           单词数：7
           最长行：'这是一行中文'
           最长行的字符数：6
           平均行长：9.5

    —— 几个点：

       ① `splitlines()` 而不是 `split("\n")`
          前者不会因为末尾换行多出一个空字符串（L5 第 1 课讲过）。

       ② 最长行从空字符串开始
          `最长行 = ""` 是安全的初始值 ——
          任何行的长度都 >= 0，所以第一个非空行一定会替换它。

          （如果允许「长度为 0 的行是最长的」，那 `>` 会保留第一个空行，
            也符合「并列取第一个」。）

       ③ 平均行长用「总字符数 / 行数」
          分母是「所有行」（包括空行）。

          如果想算「非空行的平均」，分母换成 `len(非空行)`。

          **口径要写清楚。**

       ④ 文件不存在返回 None
          让调用方判断。也可以返回空字典 `{}`，
          但 None 更容易区分「不存在」和「空文件」。

题 3
    A.  print(repr(内容))
        → 'a\nb\nc\n'

        read() 读全部，包括末尾的换行。

    B.  print(行们)
        → ['a\n', 'b\n', 'c\n']

        readlines() 每行都带换行符。

    C.  print(行们)
        → ['a', 'b', 'c']

        strip 去掉了换行。

    D.  print(len(行们))
        → 3

        文件里有 3 行（最后那个 \n 不产生第 4 行）。

    E.  print(len("中文"))                 → 2
        print(len("中文".encode("utf-8"))) → 6

        2 个字符，6 个字节。

    —— 汇总：

           A  'a\nb\nc\n'
           B  ['a\n', 'b\n', 'c\n']
           C  ['a', 'b', 'c']
           D  3
           E  2 / 6

    —— 最容易错的：

       ① B：以为 readlines 会自动去掉换行
          不会，必须自己 strip。

       ② D：以为末尾的 \n 会产生一个空行
          `"a\nb\nc\n".splitlines()` → ['a','b','c']（3 个）
          但 `"a\nb\nc\n".split("\n")` → ['a','b','c','']（4 个）

          **这就是 splitlines 比 split("\n") 好的地方。**
'''
