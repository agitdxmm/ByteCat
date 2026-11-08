r'''
════════════════════════════════════════════════════════
  L5 · 第 3 课 · 用法 2        写文件
════════════════════════════════════════════════════════

写文件比读文件更危险 —— 因为你可能**覆盖掉已有的数据**。

────────────────────────────────────────────────────────
【三种写模式】
════════════════════════════════════════════════════════

    ── "w"：覆盖写 ──

        with open("out.txt", "w", encoding="utf-8") as f:
            f.write("第一行\n")

    ⚠ **如果文件已存在，内容会全部消失！**

        打开的那一刻文件就被清空了（不是写入时）。

        所以「打开 w 模式 → 程序崩了」也会导致文件变空。

    ── "a"：追加写 ──

        with open("out.txt", "a", encoding="utf-8") as f:
            f.write("追加一行\n")

    在文件末尾加内容，原有内容保留。

    ── "x"：独占创建 ──

        with open("out.txt", "x", encoding="utf-8") as f:
            f.write("...")

    文件已存在就报错：

        FileExistsError: [Errno 17] File exists: 'out.txt'

    ── 什么时候用哪个 ──

        ┌──────────┬────────────────────────────────┐
        │ w        │ 生成新文件（明确要覆盖）        │
        │ a        │ 日志、追加记录                  │
        │ x        │ 想确保「不覆盖任何已有文件」    │
        └──────────┴────────────────────────────────┘

    ── 一个保险的做法 ──

        如果要写「可能已存在」的文件，先备份：

            import shutil
            shutil.copy("out.txt", "out.txt.bak")

        或者用时间戳命名：

            import time
            名字 = f"报告_{time.strftime('%Y%m%d_%H%M%S')}.txt"

────────────────────────────────────────────────────────
【写什么：write 和 writelines】
════════════════════════════════════════════════════════

    ── write：写一个字符串 ──

        f.write("hello")

        ⚠ **不会自动加换行！**

        想要换行必须自己写：

            f.write("第一行\n")
            f.write("第二行\n")

    ── writelines：写一组字符串 ──

        f.writelines(["a\n", "b\n", "c\n"])

        ⚠ **也不会自动加换行**，列表里必须自己带。

        （名字叫 writelines，但它不是「按行写」，
          而是「写一串字符串」。容易误解。）

    ── 更常用的写法：join ──

        行们 = ["a", "b", "c"]
        f.write("\n".join(行们))

        或者带末尾换行：

        f.write("\n".join(行们) + "\n")

    **「先拼成一个大字符串，再写一次」** 比「循环 write」快得多。

    ── write 的返回值 ──

        返回写了多少个字符：

            f.write("hello")        → 5

        一般不用，偶尔用来检查。

────────────────────────────────────────────────────────
【换行符：Windows 的坑】
════════════════════════════════════════════════════════

    ── 三种换行符 ──

        Unix / Linux / macOS    \n
        Windows                 \r\n
        老 Mac（OS 9 之前）      \r

    ── Python 的文本模式会自动转换 ──

        在 Windows 上：

            写 "\n"  → 实际写入 "\r\n"
            读 "\r\n" → 自动变成 "\n"

        这叫「通用换行」（universal newlines）。

        —— 好处：你只管写 `\n`，跨平台都对。
        —— 坑：文件里的字节数比你想的多。

            前一个文件里那个 `72 字节 vs 69 字符`的例子，
            就是 3 个 `\r` 造成的。

    ── 不想要转换 ──

        用二进制模式，或者 `newline=""`：

            with open("out.txt", "w", encoding="utf-8", newline="") as f:
                f.write("a\nb\n")

        这样写进去的就是纯 `\n`。

        —— 什么时候需要：
           生成要给别的系统（比如 Linux 服务器）读的文件。
           或者要精确控制字节数。

────────────────────────────────────────────────────────
【flush：什么时候真正写进去】
════════════════════════════════════════════════════════

    Python 写文件有「缓冲」：先攒在内存里，攒够了一定大小才真正写磁盘。

    ── 所以 write 之后，文件里可能还没有内容 ──

        要强制写出：

            f.flush()

    ── 什么时候需要 ──

        ① 程序可能被强制结束（比如日志）
        ② 别的程序要立刻读到内容

    ── with 结束时会自动 flush + close ──

        所以正常写法不需要手动 flush。

        **这也是「用 with」的理由之一。**

────────────────────────────────────────────────────────
【一个完整的写报告函数】
════════════════════════════════════════════════════════

        def 写报告(路径, 数据):
            """把数据写成一份报告文件。"""
            行们 = []
            行们.append("=" * 50)
            行们.append("报告".center(46))
            行们.append("=" * 50)

            for 条 in 数据:
                行们.append(f"  {条['名字']:<10}{条['值']:>10}")

            行们.append("=" * 50)

            with open(路径, "w", encoding="utf-8") as f:
                f.write("\n".join(行们))

    ── 三个设计点 ──

        ① 先攒到列表，最后 join 一次写
           比循环 write 快，而且「要么全写成，要么全不写」的概率更高。

        ② 用 `with` 保证关闭

        ③ 明确 `encoding="utf-8"`

    ── 返回什么 ──

        可以返回写了几行，或者文件名，方便调用方确认。

            返回值 = len(行们)

────────────────────────────────────────────────────────
【写文件会遇到的错误】
════════════════════════════════════════════════════════

    ┌────────────────────────┬──────────────────────────────┐
    │ PermissionError        │ 没权限 / 文件被别的程序占用  │
    │ FileNotFoundError      │ 目录不存在（不是文件不存在） │
    │ IsADirectoryError      │ 路径是个目录                 │
    │ FileExistsError        │ x 模式下文件已存在           │
    └────────────────────────┴──────────────────────────────┘

    ── 最常见：目录不存在 ──

        open("不存在目录/a.txt", "w")

        → FileNotFoundError: [Errno 2] No such file or directory

        **open 不会自动创建目录**，要自己建：

            import os
            os.makedirs("不存在目录", exist_ok=True)

        `exist_ok=True` 表示「已存在也不报错」。

    ── Windows 特有：文件被占用 ──

        用 Excel 打开了一个 csv，Python 再想写就会 PermissionError。

        （Linux 下允许「同时打开」，Windows 不允许。）

        解决：关掉占用它的程序。

────────────────────────────────────────────────────────
【读写小抄】
════════════════════════════════════════════════════════

    ┌──────────────┬──────────────────────────────────┐
    │ "r"          │ 读（默认），文件必须存在          │
    │ "w"          │ 写，**清空已有内容**              │
    │ "a"          │ 追加，不存在则创建                │
    │ "x"          │ 独占创建，已存在则报错            │
    │ "r+"         │ 读写，文件必须存在                │
    │ "b" 后缀     │ 二进制模式（如 "rb"、"wb"）      │
    └──────────────┴──────────────────────────────────┘

    ── 记住这一条 ──

        **`w` 会清空文件，而且是在打开的一瞬间。**
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

import os

临时 = "写文件演示.txt"

print("① w 模式：写新文件")
with open(临时, "w", encoding="utf-8") as f:
    f.write("第一行\n")
    f.write("第二行\n")

with open(临时, "r", encoding="utf-8") as f:
    print("  内容：", repr(f.read()))

print("\n② w 模式会清空已有内容")
with open(临时, "w", encoding="utf-8") as f:
    f.write("只剩下这一行\n")

with open(临时, "r", encoding="utf-8") as f:
    print("  内容：", repr(f.read()), " ← 前两行没了")

print("\n③ a 模式：追加")
with open(临时, "a", encoding="utf-8") as f:
    f.write("追加的内容\n")

with open(临时, "r", encoding="utf-8") as f:
    print("  内容：", repr(f.read()))

print("\n④ x 模式：独占创建")
try:
    with open(临时, "x", encoding="utf-8") as f:
        f.write("不会执行")
except FileExistsError:
    print("  文件已存在，x 模式报 FileExistsError")

新文件 = "独占演示.txt"
if os.path.exists(新文件):
    os.remove(新文件)
with open(新文件, "x", encoding="utf-8") as f:
    f.write("创建成功\n")
print("  新建文件成功：", os.path.exists(新文件))
os.remove(新文件)

print("\n⑤ write 不会自动换行")
with open(临时, "w", encoding="utf-8") as f:
    f.write("a")
    f.write("b")
    f.write("c")
with open(临时, "r", encoding="utf-8") as f:
    print("  连写三个 write：", repr(f.read()), " ← 都挤在一行")

print("\n⑥ 用 join 写多行")
行们 = ["第一行", "第二行", "第三行"]
with open(临时, "w", encoding="utf-8") as f:
    f.write("\n".join(行们))
with open(临时, "r", encoding="utf-8") as f:
    print("  ", repr(f.read()))

print("\n⑦ writelines 也不会加换行")
with open(临时, "w", encoding="utf-8") as f:
    f.writelines(["x", "y", "z"])
with open(临时, "r", encoding="utf-8") as f:
    print("  ", repr(f.read()))
print("  要自己带换行：", end="")
with open(临时, "w", encoding="utf-8") as f:
    f.writelines(["x\n", "y\n", "z\n"])
with open(临时, "r", encoding="utf-8") as f:
    print(repr(f.read()))

print("\n⑧ 换行符的转换")
with open(临时, "w", encoding="utf-8") as f:
    f.write("a\nb\n")
print("  文本模式写入 'a\\nb\\n'：")
print("  文件大小：", os.path.getsize(临时), "字节")
print("  （Windows 上 \\n 被写成了 \\r\\n，所以是 6 字节而不是 4）")

with open(临时, "w", encoding="utf-8", newline="") as f:
    f.write("a\nb\n")
print("  newline='' 写入：", os.path.getsize(临时), "字节 ← 不转换了")

print("\n⑨ 写一个报告")


def 写报告(路径, 标题, 数据):
    """把数据写成报告文件。"""
    行们 = []
    行们.append("=" * 44)
    行们.append(标题.center(40))
    行们.append("=" * 44)
    for 名, 值 in 数据:
        行们.append(f"  {名:<16}{值:>12}")
    行们.append("=" * 44)

    with open(路径, "w", encoding="utf-8") as f:
        f.write("\n".join(行们) + "\n")

    return len(行们)


行数 = 写报告(临时, "销售报告", [
    ("一月", 12345),
    ("二月", 23456),
    ("三月", 34567),
])
print(f"  写了 {行数} 行，内容：")
with open(临时, "r", encoding="utf-8") as f:
    for 行 in f:
        print("    " + 行.rstrip())

print("\n⑩ 追加日志的常见写法")


def 记日志(路径, 消息):
    """往日志文件追加一行（带时间戳）。"""
    import time
    时间 = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(路径, "a", encoding="utf-8") as f:
        f.write(f"[{时间}] {消息}\n")


日志文件 = "日志演示.log"
if os.path.exists(日志文件):
    os.remove(日志文件)

记日志(日志文件, "程序启动")
记日志(日志文件, "读取配置")
记日志(日志文件, "处理完成")

with open(日志文件, "r", encoding="utf-8") as f:
    print(f.read())

print("⑪ 读 → 改 → 写（最常见的组合）")


def 替换文件内容(路径, 旧, 新):
    """把文件里的 旧 替换成 新。"""
    with open(路径, "r", encoding="utf-8") as f:
        内容 = f.read()

    内容 = 内容.replace(旧, 新)

    with open(路径, "w", encoding="utf-8") as f:
        f.write(内容)


替换文件内容(临时, "销售报告", "季度汇总")
with open(临时, "r", encoding="utf-8") as f:
    print("  替换后第一行：", f.readline().rstrip())
    print("  第二行：", f.readline().rstrip())

print("\n⑫ 清理演示文件")
for 文件 in [临时, 日志文件]:
    if os.path.exists(文件):
        os.remove(文件)
        print(f"  已删除 {文件}")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  文件读写工具集
# ─────────────────────────────────────────
#
# 写这几个函数：
#
#   A. def 写行(路径, 行们)        把列表写成文件（每行一个）
#   B. def 追加行(路径, 行)        往文件末尾加一行
#   C. def 复制文件(源, 目标)      读源、写目标
#   D. def 替换(路径, 旧, 新)      把文件里的内容替换掉，返回替换了几处
#   E. def 合并(路径们, 目标)      把多个文件按顺序合并成一个
#
# 要求：
#   · 全都用 with + encoding="utf-8"
#   · 复制前检查源文件是否存在
#   · 替换函数要返回替换次数
#   · 全部测试，最后清理临时文件
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  生成一份成绩单文件
# ─────────────────────────────────────────
#
# 给定数据：
#
#     学生 = [
#         {"名字": "张三", "语文": 92, "数学": 88, "英语": 95},
#         {"名字": "李四", "语文": 78, "数学": 90, "英语": 85},
#         {"名字": "王五", "语文": 55, "数学": 48, "英语": 62},
#     ]
#
# 要求：
#   · 写到 "成绩单.txt"
#   · 格式要对齐（中文按显示宽度算）
#   · 包括表头、分隔线、每个人的数据、总计行
#   · 总分和平均分都要算
#   · 写完之后再读回来打印，确认内容正确
#   · 检查文件大小，说明为什么和字符数不一样
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.  with open("t.txt", "w", encoding="utf-8") as f:
#           f.write("a")
#           f.write("b")
#       读回来是什么？
#
#   B.  write 的返回值是什么？
#
#   C.  writelines(["a", "b"]) 之后文件内容是什么？
#
#   D.  对已存在的文件用 "x" 模式会怎样？
#
#   E.  对已存在的文件用 "w" 模式会怎样？
#
#   F.  os.path.getsize() 返回的是什么单位？
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    import os


    def 写行(路径, 行们):
        """把列表写成文件，每行一个。"""
        with open(路径, "w", encoding="utf-8") as f:
            f.write("\n".join(行们) + "\n")
        return len(行们)


    def 追加行(路径, 行):
        """往文件末尾加一行。"""
        with open(路径, "a", encoding="utf-8") as f:
            f.write(行 + "\n")


    def 复制文件(源, 目标):
        """复制文件，返回 (成功, 说明)。"""
        if not os.path.isfile(源):
            return False, f"源文件不存在：{源}"

        with open(源, "r", encoding="utf-8") as f:
            内容 = f.read()

        with open(目标, "w", encoding="utf-8") as f:
            f.write(内容)

        return True, f"复制了 {len(内容)} 个字符"


    def 替换(路径, 旧, 新):
        """替换文件内容，返回替换次数。"""
        if not os.path.isfile(路径):
            return 0

        with open(路径, "r", encoding="utf-8") as f:
            内容 = f.read()

        次数 = 内容.count(旧)
        if 次数 == 0:
            return 0

        内容 = 内容.replace(旧, 新)

        with open(路径, "w", encoding="utf-8") as f:
            f.write(内容)

        return 次数


    def 合并(路径们, 目标):
        """把多个文件合并成一个。"""
        总数 = 0
        with open(目标, "w", encoding="utf-8") as 输出:
            for 路径 in 路径们:
                if not os.path.isfile(路径):
                    continue
                with open(路径, "r", encoding="utf-8") as f:
                    内容 = f.read()
                输出.write(内容)
                if 内容 and not 内容.endswith("\n"):
                    输出.write("\n")
                总数 += 1
        return 总数


    —— 测试：

        a, b, c = "t_a.txt", "t_b.txt", "t_c.txt"
        写行(a, ["第一行", "第二行"])
        写行(b, ["第三行"])
        追加行(a, "追加的第四行")

        print(替换(a, "第二行", "改过的第二行"))     → 1
        print(替换(a, "不存在", "x"))                → 0

        print(合并([a, b], c))
        with open(c, encoding="utf-8") as f:
            print(f.read())

        for 文件 in [a, b, c]:
            os.remove(文件)

    —— 几个点：

       ① `替换` 先 count 再 replace
          因为 replace 不告诉你换了几处。

          —— 或者用 `内容.count(旧)` 得到次数，
             再用 replace。两次遍历，但清楚。

       ② `合并` 里检查 `内容.endswith("\n")`
          防止前一个文件末尾没换行，导致两个文件的内容黏在一起。

       ③ `复制文件` 返回 (bool, 说明)
          这样调用方能知道「为什么失败」。

          —— 比「返回空字符串表示失败」清楚。

       ④ `写行` 加末尾 `+ "\n"`
          这样文件末尾有换行，符合 POSIX 规范（很多工具依赖这个）。

题 2
    def 显示宽度(s):
        return sum(2 if "\u4e00" <= c <= "\u9fff" else 1 for c in s)


    def 补齐(s, 宽, 右=False):
        差 = 宽 - 显示宽度(s)
        if 差 <= 0:
            return s
        return (" " * 差 + s) if 右 else (s + " " * 差)


    def 生成成绩单(路径, 学生):
        宽 = [10, 8, 8, 8, 10, 10, 8]

        行们 = []
        行们.append("=" * sum(宽))
        行们.append(补齐("成绩单", sum(宽)).center(1))    ← 简化，见下
        行们.append("=" * sum(宽))

        # 表头
        头 = 补齐("姓名", 宽[0]) + 补齐("语文", 宽[1], True) \
             + 补齐("数学", 宽[2], True) + 补齐("英语", 宽[3], True) \
             + 补齐("总分", 宽[4], True) + 补齐("平均", 宽[5], True) \
             + 补齐("等级", 宽[6], True)
        行们.append(头)
        行们.append("-" * sum(宽))

        总总和 = 0
        总人数 = 0

        for 人 in 学生:
            总 = 人["语文"] + 人["数学"] + 人["英语"]
            均 = 总 / 3
            等 = "A" if 均 >= 90 else ("B" if 均 >= 80 else
                                       ("C" if 均 >= 70 else
                                        ("D" if 均 >= 60 else "E")))

            行们.append(
                补齐(人["名字"], 宽[0])
                + 补齐(str(人["语文"]), 宽[1], True)
                + 补齐(str(人["数学"]), 宽[2], True)
                + 补齐(str(人["英语"]), 宽[3], True)
                + 补齐(str(总), 宽[4], True)
                + 补齐(f"{均:.1f}", 宽[5], True)
                + 补齐(等, 宽[6], True)
            )

            总总和 += 总
            总人数 += 1

        行们.append("-" * sum(宽))
        行们.append(补齐("平均", 宽[0])
                    + 补齐("", 宽[1] + 宽[2] + 宽[3])
                    + 补齐(f"{总总和 / 总人数:.1f}", 宽[4] + 宽[5], True))
        行们.append("=" * sum(宽))

        with open(路径, "w", encoding="utf-8") as f:
            f.write("\n".join(行们) + "\n")

         return len(行们)


    —— 上面那个「标题居中」写得太绕了。
       简单点：`行们.append("成绩单".center(sum(宽)))` 就行
       （只是中文会稍偏，接受）。

    —— 关于「文件大小和字符数不一样」：

       文件大小 = 字节数。

       字符数 ≠ 字节数，因为：
           ① 中文在 UTF-8 里占 3 字节
           ② Windows 上 `\n` 写成 `\r\n`（多 1 字节）

       验证方法：

           with open(路径, "rb") as f:
               字节 = f.read()
           print(len(字节))              ← 字节数

           with open(路径, encoding="utf-8") as f:
               文本 = f.read()
           print(len(文本))              ← 字符数
           print(len(文本.encode("utf-8")))  ← 应该是字节数减去 \r 的数量

    —— 这题的核心：

       **「写报告」= 先用列表攒好每一行，再 join 一次写。**

       不要边算边 write，因为：
           ① 慢（每 write 一次都要走 I/O）
           ② 出错时文件是「写了一半」的状态

题 3
    A.  文件内容是 "ab"

        两次 write 都不加换行，所以连在一起。

    B.  write 返回「写了多少个字符」。

            f.write("hello")        → 5

    C.  writelines(["a", "b"]) 之后文件内容是 "ab"

        因为 writelines 不会自动加换行。

    D.  报 FileExistsError: [Errno 17] File exists

    E.  文件内容会被清空，然后写新内容。

        ⚠ 注意是「打开时立刻清空」，不是「写入时」。

    F.  字节（bytes）。

        `os.path.getsize("a.txt")` 返回的是字节数，
        不是字符数，也不是 KB。

        要转成 KB：`大小 / 1024`。

    —— 汇总：

           A  "ab"
           B  字符数
           C  "ab"
           D  FileExistsError
           E  清空后重写
           F  字节

    —— 最容易错的：

       ① A 和 C：以为 write/writelines 会自动加换行
          都不会。必须自己写 `\n`。

       ② E：以为 w 模式是「写入时才清空」
          实际是「打开时就清空」。

          所以「先 w 打开，再检查要不要写」这个逻辑是错的 ——
          打开的那一刻数据已经没了。

          正确做法：先判断，再决定用哪个模式打开。
'''
