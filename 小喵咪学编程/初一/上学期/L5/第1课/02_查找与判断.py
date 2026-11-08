r'''
════════════════════════════════════════════════════════
  L5 · 第 1 课 · 用法 2        查找与判断
════════════════════════════════════════════════════════

上一节讲「改」，这一节讲「查」和「判断」。

────────────────────────────────────────────────────────
【查找子串：find 和 index】
════════════════════════════════════════════════════════

        s = "hello world hello"

        s.find("world")     → 6        返回第一次出现的**索引**
        s.find("hello")     → 0
        s.find("python")    → -1       找不到返回 -1
        s.rfind("hello")    → 12       从右边找（最后一次出现）

    ── index 和 find 的区别 ──

        s.index("python")
        → ValueError: substring not found

        find  找不到返回 -1
        index 找不到**报错**

    ── 这正好和列表的 index 相反 ──

        列表：`列表.index(x)` 找不到 → ValueError，没有 find
        字符串：两种都有

        **字符串比列表多一个「安全的 find」。**

    ── 用哪个 ──

        ─ 想「有没有」，用 `in`（最简单）
        ─ 想「在哪」，用 find（安全）或 index（严格）
        ─ 确定存在，用 index（错了会立刻知道）

    ── 一个常见错误 ──

            if s.find("x"):          ← 错！
                ...

        因为 `find` 返回 0 时（在开头找到），`0` 是假值，
        if 会判断为 False。

        正确写法：

            if s.find("x") != -1:    ✅
            if "x" in s:             ✅ 更好

    ── find 可以指定范围 ──

        s.find("o", 5)              → 从索引 5 开始找
        s.find("o", 5, 10)          → 在 [5, 10) 范围内找

────────────────────────────────────────────────────────
【数一数：count】
════════════════════════════════════════════════════════

        s = "hello world"

        s.count("l")        → 3
        s.count("o")        → 2
        s.count("ll")       → 1
        s.count("xyz")      → 0

    count 数的是「不重叠的出现次数」。

        "aaaa".count("aa")      → 2     不是 3
        （第一个 aa 用掉了索引 0-1，第二个用 2-3，剩下的 a 不够）

────────────────────────────────────────────────────────
【开头和结尾：startswith / endswith】
════════════════════════════════════════════════════════

        s = "report_2026.txt"

        s.startswith("report")      → True
        s.endswith(".txt")          → True
        s.endswith(".csv")          → False

    ── 参数可以是元组（多个候选）──

        s.endswith((".txt", ".csv", ".md"))     → True

        「是不是这几个扩展名之一」，一行搞定。

    ── 这个在文件处理里特别常用 ──

        for 文件名 in 文件们:
            if 文件名.endswith(".py"):
                ...

────────────────────────────────────────────────────────
【is 系列：判断内容类型】
════════════════════════════════════════════════════════

    这组方法都返回 True / False，名字都以 `is` 开头。

    ── isdigit：是不是全部数字 ──

        "123".isdigit()         → True
        "12.5".isdigit()        → False     ← 小数点不算
        "-5".isdigit()          → False     ← 负号不算
        "".isdigit()            → False     ← 空字符串

    ⚠️ `isdigit` 只认「数字字符」，不认负号和小数点。

        所以判断「能不能转成整数」不能只用 isdigit：

            "-5" 是合法的整数，但 isdigit 返回 False。

        （要判断「能不能转」，最稳的还是 try/except，第 4 课讲。）

    ── isalpha：是不是全部字母 ──

        "abc".isalpha()         → True
        "中文".isalpha()        → True      ← 汉字也算
        "abc1".isalpha()        → False

    ── isalnum：字母或数字 ──

        "abc123".isalnum()      → True
        "abc 123".isalnum()     → False     ← 空格不算

    ── isspace：是不是全部空白 ──

        "   ".isspace()         → True
        " \t\n".isspace()       → True
        " a ".isspace()         → False

    ── isupper / islower：有没有大小写 ──

        "ABC".isupper()         → True
        "Abc".isupper()         → False
        "abc".islower()         → True

        ⚠️ 对「没有字母的字符串」，两个都返回 False：

            "123".isupper()     → False
            "123".islower()     → False

        （这个容易误解，以为「没有大写字母就是小写」。）

    ── istitle：是不是标题格式 ──

        "Hello World".istitle()     → True
        "Hello world".istitle()     → False

    ── 一个通用规律 ──

        **空字符串的 is 系列全部返回 False。**

            "".isdigit()    → False
            "".isalpha()    → False
            "".isspace()    → False

        因为没有内容，谈不上「是不是全数字」。

────────────────────────────────────────────────────────
【组合使用：验证输入】
════════════════════════════════════════════════════════

    ── 验证「是不是纯数字组成的正整数」──

        def 是正整数(s):
            return s.isdigit() and s != "0"

    ── 验证「是不是合法变量名」──

        def 是变量名(s):
            if len(s) == 0:
                return False
            if not (s[0].isalpha() or s[0] == "_"):
                return False
            for c in s:
                if not (c.isalnum() or c == "_"):
                    return False
            return True

    ── 验证「是不是像手机号」──

        def 像手机号(s):
            return len(s) == 11 and s.isdigit() and s[0] == "1"

    —— 这类函数在真实项目里叫「校验函数」，
       通常返回 True/False，名字用「是...」「像...」开头。

────────────────────────────────────────────────────────
【in：最简单的「有没有」】
════════════════════════════════════════════════════════

        s = "hello"
        "ell" in s          → True
        "el" in s           → True       ← 子串匹配
        "h" in s            → True
        "xyz" in s          → False

    ── 字符串的 in 是「子串匹配」──

        这一点和列表不同：

            "h" in ["hello"]        → False   列表是「元素」匹配
            "h" in "hello"          → True    字符串是「子串」匹配

        （L4 第 1 课讲过这个区别。）

    ── 什么时候用 in，什么时候用 find ──

        只判断有没有  → `in`（最快、最清楚）
        还要知道在哪  → `find`

────────────────────────────────────────────────────────
【一个实用的查找函数】
════════════════════════════════════════════════════════

    需求：找出一段文字里某个词出现的所有位置。

    ── find 只能找第一个，所以要循环 ──

        def 所有位置(文本, 词):
            """返回词出现的所有起始索引。"""
            位置 = []
            开始 = 0
            while True:
                下标 = 文本.find(词, 开始)
                if 下标 == -1:
                    break
                位置.append(下标)
                开始 = 下标 + 1          ← 注意 +1，不是 +len(词)
            return 位置

    ── 为什么是 `下标 + 1` 而不是 `+ len(词)` ──

        `+1` 允许重叠匹配：

            "aaaa".find("aa") 在第 0 位
            从 1 开始找 → 第 1 位也是 "aa"
            从 2 开始找 → 第 2 位也是 "aa"

        `+len(词)` 是不允许重叠：

            第 0 位找到后，从 2 开始找 → 第 2 位

        两个都对，看需求。

        **一般「找词出现几次」应该用不重叠**（因为同一个词重着算两个不合理）。

        那种情况直接用 `count()` 就行。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① find 和 rfind")
s = "hello world hello"
print("  s =", repr(s))
print("  find('world')   =", s.find("world"))
print("  find('hello')   =", s.find("hello"))
print("  rfind('hello')  =", s.rfind("hello"), " ← 从右往左找第一次")
print("  find('python')  =", s.find("python"), " ← 找不到返回 -1")

print("\n② index 找不到会报错")
print("  s.index('world') =", s.index("world"))
print("  s.index('python') 会报 ValueError: substring not found")

print("\n③ find 返回 0 的坑")
s = "hello"
print("  'hello'.find('h') =", s.find("h"))
print("  如果写 `if s.find('h'):` → 0 是假值，判断失败")
print("  正确写法：`if s.find('h') != -1:` 或 `if 'h' in s:`")

print("\n④ find 指定范围")
s = "hello world"
print("  s.find('o')       =", s.find("o"))
print("  s.find('o', 5)    =", s.find("o", 5), " ← 从索引 5 开始")
print("  s.find('o', 5, 8) =", s.find("o", 5, 8), " ← 在 [5,8) 里找")

print("\n⑤ count")
print("  'hello world'.count('l')  =", "hello world".count("l"))
print("  'hello world'.count('o')  =", "hello world".count("o"))
print("  'hello world'.count('xyz')=", "hello world".count("xyz"))
print("  'aaaa'.count('aa')        =", "aaaa".count("aa"), " ← 不重叠计数")

print("\n⑥ startswith / endswith")
文件名 = "report_2026.txt"
print("  文件名 =", repr(文件名))
print("  startswith('report') =", 文件名.startswith("report"))
print("  endswith('.txt')     =", 文件名.endswith(".txt"))
print("  endswith('.csv')     =", 文件名.endswith(".csv"))
print("  endswith(('.txt','.csv','.md')) =",
      文件名.endswith((".txt", ".csv", ".md")))

print("\n⑦ 批量判断文件类型")
文件们 = ["a.py", "b.txt", "c.py", "d.md", "e.csv"]
print("  所有文件：", 文件们)
print("  .py 文件：",
      [f for f in 文件们 if f.endswith(".py")])
print("  文本类文件：",
      [f for f in 文件们 if f.endswith((".txt", ".md"))])

print("\n⑧ is 系列：isdigit")
for s in ["123", "12.5", "-5", "", " 1", "１２３"]:
    print(f"  {repr(s):<8} .isdigit() = {s.isdigit()}")

print("\n⑨ isalpha / isalnum / isspace")
for s in ["abc", "中文", "abc1", "abc 123", "   ", ""]:
    print(f"  {repr(s):<10} isalpha={str(s.isalpha()):<6} "
          f"isalnum={str(s.isalnum()):<6} isspace={s.isspace()}")

print("\n⑩ isupper / islower 的坑")
for s in ["ABC", "abc", "Abc", "123", "A1"]:
    print(f"  {repr(s):<6} isupper={str(s.isupper()):<6} islower={s.islower()}")

print("\n⑪ istitle")
print("  'Hello World'.istitle() =", "Hello World".istitle())
print("  'Hello world'.istitle() =", "Hello world".istitle())

print("\n⑫ 实用的校验函数")


def 是正整数(s):
    return s.isdigit() and s != "0"


def 像手机号(s):
    return len(s) == 11 and s.isdigit() and s[0] == "1"


def 是变量名(s):
    if len(s) == 0:
        return False
    if not (s[0].isalpha() or s[0] == "_"):
        return False
    for c in s:
        if not (c.isalnum() or c == "_"):
            return False
    return True


print("  是正整数：", [(x, 是正整数(x)) for x in ["123", "0", "-5", "1.5"]])
print("  像手机号：", [(x, 像手机号(x)) for x in ["13800138000", "1380013800", "23800138000"]])
print("  是变量名：", [(x, 是变量名(x)) for x in ["abc", "_x1", "1abc", "a-b", "中文名"]])

print("\n⑬ 找所有出现位置")


def 所有位置(文本, 词):
    """返回词出现的所有起始索引（允许重叠）。"""
    位置 = []
    开始 = 0
    while True:
        下标 = 文本.find(词, 开始)
        if 下标 == -1:
            break
        位置.append(下标)
        开始 = 下标 + 1
    return 位置


print("  'aaaa' 里 'aa' 在：", 所有位置("aaaa", "aa"))
print("  'hello world' 里 'o' 在：", 所有位置("hello world", "o"))

print("\n⑭ in 是子串匹配")
print("  'ell' in 'hello'   →", "ell" in "hello")
print("  'h' in 'hello'     →", "h" in "hello")
print("  'h' in ['hello']   →", "h" in ["hello"], " ← 列表是元素匹配")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  文本检索器
# ─────────────────────────────────────────
#
# 写一个函数 `def 检索(文本, 关键词)`，返回一个字典：
#
#     {
#         "出现次数": 3,
#         "首次位置": 5,
#         "所有位置": [5, 20, 41],
#         "是否在开头": False,
#         "是否在结尾": False,
#     }
#
# 要求：
#   · 关键词不存在时，「出现次数」为 0，「首次位置」为 -1
#   · 大写小写算同一个词（提示：都转 lower 再找）
#   · 测试："The cat and the dog and the bird", "the"
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  输入验证
# ─────────────────────────────────────────
#
# 写这几个校验函数：
#
#   A. def 是整数(s)        "123" → True，"−5" → True，"1.5" → False
#                           注意负号的问题
#   B. def 是合法日期(s)     "2026-03-09" → True，"2026-13-01" → False
#   C. def 是英文名(s)       "John Smith" → True，"john" → False
#                            （要求：首字母都大写，只有字母和空格）
#   D. def 是纯中文(s)       "张三" → True，"张三abc" → False
#
# 要求：
#   · 全部只返回 True/False，不 print
#   · 每个至少测 4 个用例（包括边界情况）
#   · 说明：为什么「是整数」不能只用 isdigit()
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.  "hello".find("l")
#   B.  "hello".rfind("l")
#   C.  "hello".find("z")
#   D.  "hello".count("l")
#   E.  "hello".startswith("he")
#   F.  "hello".endswith(("lo", "p"))
#   G.  "123".isdigit()
#   H.  "-5".isdigit()
#   I.  "".isdigit()
#   J.  "123".isupper()
#   K.  "a1".isalnum()
#   L.  "hello".index("z")
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 检索(文本, 关键词):
        """返回关键词在文本中的统计信息。"""
        小文本 = 文本.lower()
        小词 = 关键词.lower()

        位置 = []
        开始 = 0
        while True:
            下标 = 小文本.find(小词, 开始)
            if 下标 == -1:
                break
            位置.append(下标)
            开始 = 下标 + 1

        return {
            "出现次数": len(位置),
            "首次位置": 位置[0] if 位置 else -1,
            "所有位置": 位置,
            "是否在开头": 小文本.startswith(小词),
            "是否在结尾": 小文本.endswith(小词),
        }


    测试：

        文本 = "The cat and the dog and the bird"
        print(检索(文本, "the"))

    输出：
        {'出现次数': 3,
         '首次位置': 0,
         '所有位置': [0, 12, 24],
         '是否在开头': True,
         '是否在结尾': False}

    —— 验证位置：

        "The cat and the dog and the bird"
         0123456789...

        T=0, h=1, e=2
        第一个 "the" 在 0
        "The cat and " 是 12 个字符 → 第二个 the 在 12
        "The cat and the dog and " 是 24 个字符 → 第三个在 24

        （`"The cat and "` 数一下：T-h-e-空格-c-a-t-空格-a-n-d-空格 = 12 ✓）

    —— 几个关键点：

       ① 先转 lower 再找
          这样 "The" 和 "the" 都能匹配。

          ⚠ 但「位置」是基于小写后的字符串算的 ——
            如果原文本有大写字母，位置不会变（因为 lower 不改变长度）。

            对中文、英文都成立（lower 不改变字符数）。

            但如果原文本里有某些特殊字符（比如土耳其语的 İ），
            lower 可能改变长度 —— 那种情况要小心。

       ② `位置[0] if 位置 else -1`
          列表为空时不能 `位置[0]`（IndexError）。
          这是「空列表的默认值」，L4 讲过好几次的写法。

       ③ `是否在开头` / `是否在结尾` 直接用方法
          不用自己比较索引。

       ④ 用 `+1` 允许重叠
          "the" 这种词不太会重叠，但如果是 "aa" 就有影响了。

    —— 如果要用「不重叠」的版本：

        把 `开始 = 下标 + 1` 改成 `开始 = 下标 + len(小词)`。

    题 2
    def 是整数(s):
        """判断是不是整数字符串（允许负号）。"""
        if len(s) == 0:
            return False
        if s[0] in "+-":
            return s[1:].isdigit() and len(s) > 1
        return s.isdigit()


    def 是合法日期(s):
        """判断 YYYY-MM-DD 格式的日期是否合法。"""
        if len(s) != 10:
            return False
        if s[4] != "-" or s[7] != "-":
            return False

        年部分, 月部分, 日部分 = s[:4], s[5:7], s[8:10]
        if not (年部分.isdigit() and 月部分.isdigit() and 日部分.isdigit()):
            return False

        年, 月, 日 = int(年部分), int(月部分), int(日部分)
        if 年 < 1 or 月 < 1 or 月 > 12:
            return False

        每月天数 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        # 闰年 2 月 29 天
        if (年 % 4 == 0 and 年 % 100 != 0) or 年 % 400 == 0:
            每月天数[1] = 29

        return 1 <= 日 <= 每月天数[月 - 1]


    def 是英文名(s):
        """判断是不是「首字母大写的英文名」（可以有空格）。"""
        if len(s) == 0:
            return False
        for 词 in s.split():
            if len(词) == 0:
                return False
            if not 词.isalpha():
                return False
            if not 词[0].isupper():
                return False
            if not 词[1:].islower() and len(词) > 1:
                return False
        return True


    def 是纯中文(s):
        """判断是不是全由中文字符组成。"""
        if len(s) == 0:
            return False
        for c in s:
            if not ("\u4e00" <= c <= "\u9fff"):
                return False
        return True


    —— 测试：

        print([(x, 是整数(x)) for x in ["123", "-5", "+7", "1.5", "", "-"]])
        → [('123', True), ('-5', True), ('+7', True), ('1.5', False),
           ('', False), ('-', False)]

        print([(x, 是合法日期(x)) for x in
               ["2026-03-09", "2026-13-01", "2024-02-29", "2026-02-29",
                "2026-3-9", "2026-03-32"]])
        → [('2026-03-09', True), ('2026-13-01', False),
           ('2024-02-29', True),   ← 闰年
           ('2026-02-29', False),  ← 平年
           ('2026-3-9', False),    ← 格式不对
           ('2026-03-32', False)]

        print([(x, 是英文名(x)) for x in
               ["John Smith", "john", "John", "John smith", "J"]])
        → [('John Smith', True), ('john', False), ('John', True),
           ('John smith', False), ('J', True)]

        print([(x, 是纯中文(x)) for x in ["张三", "张三abc", "", "李 四"]])
        → [('张三', True), ('张三abc', False), ('', False), ('李 四', False)]

    —— 「为什么是整数不能只用 isdigit」：

       **因为 `isdigit()` 不认负号和小数点。**

           "-5".isdigit()      → False
           "+7".isdigit()      → False
           "1.5".isdigit()     → False

       但 `-5` 和 `+7` 确实是合法的整数，只是不能直接 `int()` 吗？

           int("-5")   → -5      ✅ 能转
           int("+7")   → 7       ✅ 能转
           int("1.5")  → 报错

       所以「能不能转成整数」和「isdigit 是不是 True」
       是两件事。

       正确做法有两种：

           ① 手写检查（上面的写法）
           ② 直接用 try/except（第 4 课讲，最稳）

                   def 是整数(s):
                       try:
                           int(s)
                           return True
                       except ValueError:
                           return False

       —— 第二种能覆盖所有情况（包括 "  123  " 这种带空格的，
          int 会自动去空格），但要知道 except 怎么写。

       —— 而且 try 版会把 "1_000" 也判成 True（Python 3.6+ 支持下划线），
          这可能不是你要的。

          **所以「手写规则」和「试转换」各有适用场景。**

    —— 日期那个函数值得注意：

       ① 格式检查（长度、横线位置）+ 内容检查（数字、范围）
          两步都要，缺一不可。

       ② 闰年判断用 L2 第 2 课的公式。

       ③ 用列表存每月天数，闰年时改 2 月
          —— 比一长串 if-elif 清楚。

       ④ `每月天数[月 - 1]`
          月份是 1~12，索引要 0~11，所以减 1。

题 3
    A.  "hello".find("l")   → 2       第一个 l 在索引 2

    B.  "hello".rfind("l")  → 3       最后一个 l 在索引 3

    C.  "hello".find("z")   → -1      找不到

    D.  "hello".count("l")  → 2       两个 l

    E.  "hello".startswith("he") → True

    F.  "hello".endswith(("lo", "p")) → True
        参数可以是元组，「是其中任意一个」就 True。

    G.  "123".isdigit()     → True

    H.  "-5".isdigit()      → False    负号不算数字字符

    I.  "".isdigit()        → False    空字符串全部 False

    J.  "123".isupper()     → False
        没有字母的字符串，isupper 和 islower 都是 False。

    K.  "a1".isalnum()      → True     字母 + 数字

    L.  "hello".index("z")  → ValueError: substring not found

    —— 汇总：

           A  2
           B  3
           C  -1
           D  2
           E  True
           F  True
           G  True
           H  False
           I  False
           J  False
           K  True
           L  ValueError

    —— 最容易错的三个：

       ① H：以为 "-5" 是数字
          isdigit 只认 0~9 这十个字符。

       ② J：以为 "123".isupper() 是 True
          没有字母时两个都返回 False。

       ③ C vs L：find 返回 -1，index 报错
          这是「安全」和「严格」的两种设计，
          选哪个看你的需求。
'''
