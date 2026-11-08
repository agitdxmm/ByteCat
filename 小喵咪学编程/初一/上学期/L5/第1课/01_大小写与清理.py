r'''
════════════════════════════════════════════════════════
  L5 · 第 1 课 · 用法 1        大小写与清理
════════════════════════════════════════════════════════

L1 讲过字符串的「创建、索引、切片、len、in」。

这一课把字符串的**方法**讲全。先说最重要的一类：
**改大小写、去空白。**

────────────────────────────────────────────────────────
【改大小写：五个方法】
════════════════════════════════════════════════════════

        s = "hello World"

        s.upper()       → "HELLO WORLD"     全大写
        s.lower()       → "hello world"     全小写
        s.title()       → "Hello World"     每个单词首字母大写
        s.capitalize()  → "Hello world"     只有第一个字母大写
        s.swapcase()    → "HELLO wORLD"     大小写互换

    ── 全都不修改原字符串 ──

        字符串是不可变的，所以这些方法都**返回新字符串**：

            s = "hello"
            s.upper()
            print(s)        → "hello"      ← 没变！

            s = s.upper()   ← 要接住返回值
            print(s)        → "HELLO"

        这是初学者最常犯的错之一。

    ── 中文不受影响 ──

        "你好".upper()      → "你好"
        "你好".title()      → "你好"

        因为中文没有大小写。

    ── title 的坑 ──

        title() 是「每个单词首字母大写」，但它认的「单词边界」
        是所有非字母字符：

            "it's a dog".title()        → "It'S A Dog"

        注意 `'` 后面的 s 也被大写了。

        想要「正常的标题格式」，得自己处理（或者用正则）。

    ── 什么时候用哪个 ──

        比较时统一大小写  → lower()（最常见）
        显示时统一大写    → upper()（比如股票代码、缩写）
        标题显示          → title()
        只首字母大写      → capitalize()

    ── lower() 最常用的场景 ──

        判断用户输入时：

            if 命令.lower() == "quit":
                break

        这样 "Quit"、"QUIT"、"quit" 都能识别。

        **「用户输入先 lower() 再比较」是个好习惯。**

────────────────────────────────────────────────────────
【去空白：strip 三兄弟】
════════════════════════════════════════════════════════

        s = "  hello  "

        s.strip()       → "hello"       去两端
        s.lstrip()      → "hello  "     只去左边（left）
        s.rstrip()      → "  hello"     只去右边（right）

    ── strip 去的是「所有空白字符」，不只是空格 ──

        "  \t hello \n ".strip()    → "hello"

        空格、制表符 \t、换行 \n 都会被去掉。

    ── 也可以指定要去掉的字符 ──

        "***hello***".strip("*")        → "hello"
        "xxhelloxx".strip("x")           → "hello"
        "abcABC".strip("abc")            → "ABC"

        ⚠ 注意 `strip("abc")` 不是「去掉子串 "abc"」，
          而是「去掉两端的 a、b、c 中的任意字符」。

                "abcabcXYZabc".strip("abc")   → "XYZ"
                （两端的 a、b、c 全被啃掉，直到遇到 X）

        这个区别很容易搞错。

    ── strip 最常用的场景 ──

        处理用户输入：

            名字 = input("请输入名字：").strip()

        用户可能多打了空格，strip 一下就干净了。

        L1 第 4 课讲过：`int(input("...").strip())` 是标准写法。

────────────────────────────────────────────────────────
【一个实用组合：清洗用户输入】
════════════════════════════════════════════════════════

    用户输入往往很脏：

        "  张三  "
        "张三\n"
        "  ZHANG SAN  "
        "  \t 张三 \t "

    ── 一个通用的清洗函数 ──

        def 清洗(文本):
            """去掉两端空白，把连续空白压成一个空格。"""
            return " ".join(文本.split())

    ── `.split()` 不带参数时，按「任意空白」分割 ──

        "  a   b  c ".split()       → ['a', 'b', 'c']

        注意它自动忽略了多余的空格和两端的空白。

        然后用 `" ".join(...)` 拼回来，就得到「标准化的空格」。

    ── 例子 ──

        "  张三   李四   王五  ".split()
        → ['张三', '李四', '王五']

        " ".join(...)
        → "张三 李四 王五"

    这个「split + join」组合是字符串处理的万能套路，
    后面几节会反复用。

────────────────────────────────────────────────────────
【大小写 + 清理，组合使用】
════════════════════════════════════════════════════════

    链式调用：

        "  Hello World  ".strip().lower()
        → "hello world"

    先 strip 再 lower，顺序不影响结果（两个操作互不干扰）。

    ── 但有些组合顺序有影响 ──

        "  hello  ".strip().upper()     → "HELLO"
        "  hello  ".upper().strip()     → "HELLO"

        这两个结果一样。

        但如果是：

            "hello world".title().strip()
            "hello world".strip().title()

        也一样。

        ── 什么时候顺序真的有影响 ──

            文本 = "  a b  "
            文本.split()           → ['a', 'b']
            文本.strip().split()   → ['a', 'b']    （一样的，split 本来就忽略空白）

        或者：

            "abc".replace("a", " ").strip()    → "bc"
            "abc".strip().replace("a", " ")    → " bc"

        这里顺序就重要了。

        —— 原则：**先做「会影响结构」的操作（strip、split），
          再做「只影响内容」的操作（upper、replace）。**

────────────────────────────────────────────────────────
【方法速查】
════════════════════════════════════════════════════════

    ┌──────────────────┬──────────────────────────────┐
    │ s.upper()        │ 全大写                        │
    │ s.lower()        │ 全小写                        │
    │ s.title()        │ 每个单词首字母大写            │
    │ s.capitalize()   │ 只有首字母大写                │
    │ s.swapcase()     │ 大小写互换                    │
    │ s.strip()        │ 去两端空白                    │
    │ s.strip(字符)    │ 去两端指定字符                │
    │ s.lstrip()       │ 只去左边                      │
    │ s.rstrip()       │ 只去右边                      │
    └──────────────────┴──────────────────────────────┘

    ── 全部返回新字符串，不修改原字符串 ──

    因为字符串是不可变的 —— 这条要一直记住。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① 五种改大小写")
s = "hello World"
print("  原文：      ", repr(s))
print("  upper()     ", repr(s.upper()))
print("  lower()     ", repr(s.lower()))
print("  title()     ", repr(s.title()))
print("  capitalize()", repr(s.capitalize()))
print("  swapcase()  ", repr(s.swapcase()))
print("  原文没变：  ", repr(s))

print("\n② 要接住返回值")
s = "hello"
s.upper()
print("  只调用不接住：", repr(s))
s = s.upper()
print("  接住之后：    ", repr(s))

print("\n③ 中文不受影响")
print("  '你好世界'.upper()    =", "你好世界".upper())
print("  '你好世界'.title()    =", "你好世界".title())

print("\n④ title 的小坑")
print("  \"it's a dog\".title() =", repr("it's a dog".title()))
print("  ↑ 撇号后面的 s 也被大写了")

print("\n⑤ 去空白")
s = "  hello  "
print("  原文：    ", repr(s))
print("  strip()   ", repr(s.strip()))
print("  lstrip()  ", repr(s.lstrip()))
print("  rstrip()  ", repr(s.rstrip()))

print("\n⑥ strip 能去所有空白字符")
脏 = " \t\n  hello  \n\t "
print("  原文：", repr(脏))
print("  strip 后：", repr(脏.strip()))

print("\n⑦ strip 指定字符（不是去子串）")
print("  '***hello***'.strip('*')   =", repr("***hello***".strip("*")))
print("  'abcabcXYZabc'.strip('abc')=", repr("abcabcXYZabc".strip("abc")))
print("  ↑ 是「去掉两端的 a、b、c 任意一个」，不是去子串")

print("\n⑧ 实际场景：清洗用户输入")


def 清洗输入(文本):
    """去两端空白、连续空白压成一个。"""
    return " ".join(文本.split())


测试 = [
    "  张三  ",
    "  张三   李四   王五  ",
    "\t hello \n world \t",
    "    ",
]
for 原文 in 测试:
    print(f"  {repr(原文):<28} → {repr(清洗输入(原文))}")

print("\n⑨ 判断命令时先 lower")
命令们 = ["quit", "QUIT", "Quit", "qUiT", "exit"]
for 命令 in 命令们:
    print(f"  {命令:<8} → {'是退出命令' if 命令.lower() == 'quit' else '不是'}")

print("\n⑩ 链式调用")
原文 = "  Hello World  "
print("  原文：              ", repr(原文))
print("  .strip().lower()：  ", repr("  Hello World  ".strip().lower()))
print("  .strip().title()：  ", repr("  hello world  ".strip().title()))

print("\n⑪ 顺序有影响的情况")
print("  'abc'.replace('a',' ').strip() = ", repr("abc".replace("a", " ").strip()))
print("  'abc'.strip().replace('a',' ') = ", repr("abc".strip().replace("a", " ")))
print("  ↑ 先 replace 会产生新的空白，再 strip 就去掉了")
print("    先 strip 时字符串本来就没空白，replace 产生的空白留了下来")

print("\n⑫ 综合：规范化名字输入")


def 规范名字(文本):
    """去空白、统一格式：每个字之间不留空格，首字母大写。"""
    干净 = "".join(文本.split())      # 去掉所有空白
    return 干净


for 原文 in ["  张 三  ", "李 四", "  王五"]:
    print(f"  {repr(原文):<14} → {repr(规范名字(原文))}")

print("\n⑬ 大小写不敏感的比较")


def 是同一句(a, b):
    """忽略大小写和两端空白，判断两句是否相同。"""
    return a.strip().lower() == b.strip().lower()


对 = [
    ("Hello", "hello"),
    ("  World  ", "WORLD"),
    ("Python", "Java"),
]
for a, b in 对:
    print(f"  {repr(a):<12} vs {repr(b):<10} → {是同一句(a, b)}")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  文本规范化
# ─────────────────────────────────────────
#
# 写一个函数：
#
#     def 规范(文本)
#
# 把一段杂乱的文本整理成标准格式：
#   · 去掉两端空白
#   · 连续多个空格压成一个
#   · 所有字母转小写
#   · 标点符号后面加一个空格（如果原来没有）
#   · 去掉中文字符之间的空格
#
# 测试：
#     "  Hello   World  "              → "hello world"
#     "Hello,World"                    → "hello, world"
#     "张 三 和 李 四"                  → "张三和李四"
#     "a.b,c"                          → "a. b, c"
#
# 提示：中文字符的判断可以用 `'\u4e00' <= c <= '\u9fff'`
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  密码强度检查
# ─────────────────────────────────────────
#
# 写一个 `def 检查密码(密码)`，返回 (是否合格, 原因列表)：
#
#   · 长度至少 8
#   · 至少有一个大写字母
#   · 至少有一个小写字母
#   · 至少有一个数字
#   · 不能有空格
#   · 不能全是同一个字符（比如 "aaaaaaaa"）
#
# 测试：
#     "abc123"        → (False, ["长度不足 8 位", "没有大写字母"])
#     "Abc12345"      → (True, [])
#     "AAAAAAAA"      → (False, ["没有小写字母", "没有数字", "全是同一个字符"])
#     "Abc 12345"     → (False, ["有空格"])
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.  "Hello".upper()
#   B.  "Hello".lower()
#   C.  "hello world".title()
#   D.  "hello".capitalize()
#   E.  "  hi  ".strip()
#   F.  "xxhixx".strip("x")
#   G.  "a b  c".split()
#   H.  "Hello".upper().lower()
#   I.  s = "abc"
#       s.upper()
#       print(s)
#   J.  "abc".strip("abc")
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 是中文(c):
        return "\u4e00" <= c <= "\u9fff"


    def 规范(文本):
        """整理文本格式。"""
        # ① 两端去空白 + ② 连续空格压成一个
        干净 = " ".join(文本.split())

        # ③ 转小写
        干净 = 干净.lower()

        # ④ 标点后加空格（如果后面紧跟着字符且不是空格）
        结果 = ""
        for i in range(len(干净)):
            结果 += 干净[i]
            if 干净[i] in ",.?!;:" and i + 1 < len(干净):
                if 干净[i + 1] != " ":
                    结果 += " "

        # ⑤ 去掉中文字符之间的空格
        最后 = ""
        for i in range(len(结果)):
            if 结果[i] == " ":
                # 看前后是不是都是中文
                前 = 结果[i - 1] if i > 0 else ""
                后 = 结果[i + 1] if i + 1 < len(结果) else ""
                if 是中文(前) and 是中文(后):
                    continue        # 跳过这个空格
            最后 += 结果[i]

        return 最后


    测试：

        print(规范("  Hello   World  "))     → "hello world"
        print(规范("Hello,World"))           → "hello, world"
        print(规范("张 三 和 李 四"))         → "张三和李四"
        print(规范("a.b,c"))                 → "a. b, c"

    —— 五个步骤逐个看：

       ① `" ".join(文本.split())`
          一步搞定「去两端空白」+「压缩连续空格」。
          因为 split() 不带参数时按任意空白切，自动忽略多余空白。

       ② `.lower()` 转小写

       ③ 标点后加空格
          遍历每个字符，遇到标点就看下一个是不是空格，
          不是就补一个。

          ⚠ `i + 1 < len(干净)` 这个判断很重要 ——
            最后一个字符是标点时，没有「下一个」，不能补空格。

       ④ 去掉中文之间的空格
          遇到空格时，看前后两个字符是不是都是中文。
          是就跳过（不加入结果）。

          `前 = 结果[i - 1] if i > 0 else ""`
          这是防止 i=0 时索引 -1（会取到最后一个字符，逻辑就错了）。

    —— 一个更简洁的写法（用 replace）：

        中文字符之间加空格的情况，可以先找出来再替换。
        但那样要写更多代码。

        现在的「逐字符扫描」虽然长，但每一步都清楚。

    —— 这道题的实战意义：

       **文本规范化是数据清洗的常见需求。**

       用户输入、网页抓取、OCR 识别的文本，
       经常有多余空格、大小写混乱、标点贴在一起的问题。

       真实项目里会写一套「清洗规则」，逐条应用。

       你这个函数就是最简版本。

题 2
    def 检查密码(密码):
        """返回 (是否合格, 原因列表)。"""
        原因 = []

        if len(密码) < 8:
            原因.append("长度不足 8 位")

        if not any(c.isupper() for c in 密码):
            原因.append("没有大写字母")

        if not any(c.islower() for c in 密码):
            原因.append("没有小写字母")

        if not any(c.isdigit() for c in 密码):
            原因.append("没有数字")

        if any(c.isspace() for c in 密码):
            原因.append("有空格")

        if len(set(密码)) == 1:
            原因.append("全是同一个字符")

        return len(原因) == 0, 原因


    测试：

        print(检查密码("abc123"))
        → (False, ['长度不足 8 位', '没有大写字母'])

        print(检查密码("Abc12345"))
        → (True, [])

        print(检查密码("AAAAAAAA"))
        → (False, ['没有小写字母', '没有数字', '全是同一个字符'])

        print(检查密码("Abc 12345"))
        → (False, ['有空格'])

    —— 几个关键点：

       ① `any(条件 for c in 密码)`
          「只要有一个字符满足条件」就返回 True。

          对应的 `all(...)` 是「所有字符都满足」。

          这两个函数配合「生成器表达式」非常好用：

              any(c.isupper() for c in 密码)     有没有大写
              all(c.isdigit() for c in 密码)     是不是全是数字

       ② `len(set(密码)) == 1`
          用集合去重，如果只剩 1 个元素，说明全是同一个字符。

          —— 这是「集合去重」的一个巧妙应用。

       ③ 原因列表，不是「第一个原因就返回」
          这样用户能一次看到所有问题，不用改一条试一次。

          —— 用户体验上的考虑：**一次说完，别挤牙膏。**

       ④ 没有检查「特殊字符」
          因为题目没要求。真实系统里通常还会要求
          「至少一个特殊字符（!@#$%）」。

    —— 关于 `c.isupper()` 和 `c.islower()`：

       它们对「不是字母的字符」都返回 False。

            "1".isupper()       → False
            "!".isupper()       → False

        所以 `any(c.isupper() for c in "123")` 是 False —— 正确。

题 3
    A.  "Hello".upper() → "HELLO"

    B.  "Hello".lower() → "hello"

    C.  "hello world".title() → "Hello World"

    D.  "hello".capitalize() → "Hello"

    E.  "  hi  ".strip() → "hi"

    F.  "xxhixx".strip("x") → "hi"

        逐字看：x, x, h, i, x, x
            左端两个 x 被去掉 → 剩 "hixx"
            右端两个 x 被去掉 → 剩 "hi"
            中间没有 x 了，停。

        所以结果是 "hi"。

    G.  "a b  c".split() → ['a', 'b', 'c']

        不带参数的 split 按任意空白切，连续的空白算一个。

    H.  "Hello".upper().lower() → "hello"

        先变大写再变小写，最终是小写。

    I.  s = "abc"
        s.upper()
        print(s)
        → "abc"

        **没接住返回值，原字符串不变。**

    J.  "abc".strip("abc") → ""

        两端的所有 a、b、c 都被去掉，剩下空字符串。

    —— 汇总：

           A  "HELLO"
           B  "hello"
           C  "Hello World"
           D  "Hello"
           E  "hi"
           F  "hi"
           G  ['a', 'b', 'c']
           H  "hello"
           I  "abc"
           J  ""

    —— 最容易错的两个：

       ① F：容易以为「只去掉一层」
          实际上 strip 会一直啃，直到遇到不在字符集里的字符。

          这几个都能验证这个规则：

              "xxxhixxx".strip("x")   → "hi"
              "xhxix".strip("x")      → "hxi"
                  （左端去 x → "hxix"，右端是 x 再去掉 → "hxi"，
                    中间的 x 不在两端，保留）
              "abc".strip("abc")      → ""
                  （两边一路啃到底，什么都不剩）

       ② I：以为调用了方法就会改
          字符串不可变，任何方法都返回新字符串。
          这是这一节最核心的一条。
'''
