r'''
════════════════════════════════════════════════════════
  L5 · 第 5 课 · 用法 1        模块与 import
════════════════════════════════════════════════════════

前面用了好几次 `import`，但没解释过它到底是什么。

这一节讲：**怎么用别人写好的代码，怎么让自己的代码被别人用。**

────────────────────────────────────────────────────────
【模块就是一个 .py 文件】
════════════════════════════════════════════════════════

    你自己写的 `工具.py`，就是一个模块。

    别的文件想用它里面的函数：

        # 在 main.py 里
        import 工具

        工具.打招呼()

    ── 关键：必须先「导入」，才能用 ──

        直接写 `打招呼()` 会 NameError ——
        Python 不知道这个名字从哪来。

    ── 调用时要加「模块名.」──

        import 工具
        工具.打招呼()          ✅
        打招呼()               ❌ NameError

    ── 为什么要有这个前缀 ──

        因为不同模块可能有同名函数：

            工具.处理()      ← 工具模块的
            备份.处理()      ← 备份模块的

        带前缀就不会冲突。

────────────────────────────────────────────────────────
【import 的几种写法】
════════════════════════════════════════════════════════

    ── ① 最基本的 ──

        import math
        math.sqrt(16)           → 4.0

        用的时候要写 `math.`

    ── ② 导入特定名字 ──

        from math import sqrt, pi
        sqrt(16)                → 4.0
        pi                      → 3.141592653589793

        **不用写模块名了**，但要注意别和已有名字冲突。

    ── ③ 导入全部（不推荐）──

        from math import *
        sqrt(16)                → 4.0

        ⚠ 问题：
           · 你不知道到底导入了什么
           · 可能覆盖你已有的变量/函数
           · 读代码时看不出 sqrt 是哪来的

        **只在交互式环境里图方便时用。**

    ── ④ 起别名 ──

        import math as m
        m.sqrt(16)              → 4.0

        import numpy as np      ← 这是最常见的别名（第三方库）

        什么时候用：
           · 名字太长
           · 有约定俗成的别名（np、pd、plt）

    ── 四种写法对比 ──

        ┌────────────────────────┬──────────────┬────────────┐
        │ 写法                   │ 调用           │ 推荐度     │
        ├────────────────────────┼──────────────┼────────────┤
        │ import math            │ math.sqrt()  │ ★★★       │
        │ from math import sqrt  │ sqrt()       │ ★★        │
        │ import math as m       │ m.sqrt()     │ ★★        │
        │ from math import *     │ sqrt()       │ ★          │
        └────────────────────────┴──────────────┴────────────┘

    **最稳的是第一种** —— 一眼能看出每个名字的来源。

────────────────────────────────────────────────────────
【标准库：Python 自带的工具箱】
════════════════════════════════════════════════════════

    装 Python 时就带了几百个模块，不用额外安装。

    ── 常用的 ──

        math            数学函数（开方、三角、常量）
        random          随机数
        datetime        日期时间
        os              操作系统（路径、目录、环境变量）
        json            JSON 读写
        csv             CSV 读写
        time            时间戳、睡眠
        sys             Python 解释器相关
        re              正则表达式
        collections     高级数据结构

    ── 怎么知道有哪些 ──

        查官方文档，或者：

            import math
            print(dir(math))          # 列出所有名字
            help(math.sqrt)           # 查看说明

    ── `dir` 和 `help` 是探索模块的最好工具 ──

        不用背，用的时候查就行。

        **尤其是 `help()` —— 它读的就是 L3 讲的 docstring。**

────────────────────────────────────────────────────────
【自己写模块：一个完整的例子】
════════════════════════════════════════════════════════

    ── mymath.py ──

        """我的数学工具。"""

        def 是素数(n):
            """判断 n 是不是素数。"""
            if n < 2:
                return False
            i = 2
            while i * i <= n:
                if n % i == 0:
                    return False
                i += 1
            return True


        def 阶乘(n):
            """返回 n 的阶乘。"""
            结果 = 1
            for i in range(2, n + 1):
                结果 *= i
            return 结果


        if __name__ == "__main__":
            # 只有直接运行这个文件时才执行
            print("测试：", 是素数(97), 阶乘(5))

    ── 在另一个文件里用 ──

        import mymath

        print(mymath.是素数(97))          → True
        print(mymath.阶乘(5))             → 120

────────────────────────────────────────────────────────
【`if __name__ == "__main__":` 是什么】
════════════════════════════════════════════════════════

    这是 Python 里最常见的一行「咒语」。

    ── 它的作用 ──

        **让同一个文件，既能「被导入」，又能「直接运行」。**

        情况一：`python mymath.py` 直接运行
            `__name__` 是 `"__main__"` → 执行里面的代码

        情况二：`import mymath` 被导入
            `__name__` 是 `"mymath"` → 不执行

    ── 没有它会怎样 ──

        如果 mymath.py 末尾直接写 `print("测试：", ...)`：

            import mymath       → 会打印「测试：...」

        被导入时「顺便」执行了一堆测试代码，很糟糕。

    ── 规矩 ──

        **一个模块里的「测试代码」「命令行入口」，
        都要放在 `if __name__ == "__main__":` 下面。**

        模块本身只提供函数，不主动做事。

    ── `__name__` 是什么 ──

        每个模块都有一个 `__name__` 变量：

            直接运行时       "__main__"
            被导入时         模块名

        你可以自己验证：

            print(__name__)

    ── 一个模块的典型结构 ──

        """模块说明（docstring）。"""

        # ① 导入
        import os
        import json

        # ② 常量
        默认路径 = "config.json"

        # ③ 函数
        def 读配置(路径=默认路径):
            ...

        def 处理数据(数据):
            ...

        # ④ 主入口
        if __name__ == "__main__":
            print("自测开始")
            读配置()
            print("自测结束")

    **这个结构几乎所有 Python 文件都长这样。**

────────────────────────────────────────────────────────
【模块搜索路径】
════════════════════════════════════════════════════════

    `import mymath` 时，Python 去哪找这个文件？

    ── 按顺序找 ──

        ① 当前目录（运行脚本所在目录）
        ② 标准库目录
        ③ 第三方库目录（site-packages）
        ④ PYTHONPATH 环境变量里的路径

    ── 常见问题：找不到模块 ──

        ModuleNotFoundError: No module named 'mymath'

        原因：
           ① 文件名拼错
           ② 文件和运行脚本不在同一目录
           ③ 在子目录里，没加路径

    ── 查看 Python 会去哪找 ──

        import sys
        print(sys.path)

    ── 子目录里的模块 ──

        如果 mymath.py 在 `工具/` 子目录里：

            from 工具 import mymath          ← 要写目录名
            mymath.是素数(97)

        或者：

            from 工具.mymath import 是素数

        （子目录里最好有 `__init__.py`，早期版本需要它，
          Python 3.3+ 可以没有。）

    ── 一个坑：自己写的文件名和标准库重名 ──

        如果你写了个 `random.py` 放在当前目录，
        那 `import random` 导入的会是**你的**那个，
        而不是标准库的。

        结果：标准库的 random 功能全没了。

        **别给自己的文件起标准库的名字。**

        常见的撞名：random、math、json、csv、time、os、test。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① import 的四种写法")

import math

print("  import math → math.sqrt(16) =", math.sqrt(16))

from math import sqrt, pi

print("  from math import sqrt → sqrt(16) =", sqrt(16))
print("  pi =", pi)

import math as m

print("  import math as m → m.sqrt(16) =", m.sqrt(16))

print("\n② 标准库能干什么")
print("  math 里的常用函数：")
print("    math.sqrt(2)   =", math.sqrt(2))
print("    math.floor(3.7)=", math.floor(3.7))
print("    math.ceil(3.2) =", math.ceil(3.2))
print("    math.fabs(-5)  =", math.fabs(-5))
print("    math.gcd(48, 18) =", math.gcd(48, 18))
print("    math.pi        =", math.pi)

import random

print("\n  random：")
print("    random.randint(1, 10) =", random.randint(1, 10))
print("    random.choice(['a','b','c']) =", random.choice(["a", "b", "c"]))
名单 = [1, 2, 3, 4, 5]
random.shuffle(名单)
print("    shuffle 之后：", 名单)

import datetime

print("\n  datetime：")
现在 = datetime.datetime.now()
print("    现在：", 现在)
print("    格式化：", 现在.strftime("%Y年%m月%d日 %H:%M"))
print("    三天后：", 现在 + datetime.timedelta(days=3))

print("\n③ dir 和 help")
print("  dir(math) 里有", len(dir(math)), "个名字")
print("  前 10 个：", [x for x in dir(math) if not x.startswith("_")][:10])
print()
print("  help(math.sqrt) 的说明：")
import io
import contextlib

缓冲区 = io.StringIO()
with contextlib.redirect_stdout(缓冲区):
    help(math.sqrt)
for 行 in 缓冲区.getvalue().splitlines()[:6]:
    print("   ", 行)

print("\n④ __name__ 的值")
print("  当前文件的 __name__ =", repr(__name__))
print("  ↑ 直接运行时是 '__main__'，被导入时是模块名")

print("\n⑤ 模拟一个模块")


def 是素数(n):
    """判断 n 是不是素数。"""
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def 阶乘(n):
    """返回 n 的阶乘。"""
    结果 = 1
    for i in range(2, n + 1):
        结果 *= i
    return 结果


print("  是素数(97) =", 是素数(97))
print("  是素数(91) =", 是素数(91))
print("  阶乘(5) =", 阶乘(5))

print("\n⑥ 模块其实就是文件")
print("  你可以想象 mymath.py 这个文件里写了上面两个函数")
print("  然后另一个文件 `import mymath` 就能用")

print("\n⑦ 看看 sys.path")
import sys

print("  Python 会按这个顺序找模块：")
for i, 路径 in enumerate(sys.path[:4], 1):
    print(f"    {i}. {路径}")

print("\n⑧ 标准库模块速览")
模块们 = [
    ("math", "数学函数"),
    ("random", "随机数"),
    ("datetime", "日期时间"),
    ("os", "操作系统接口"),
    ("json", "JSON 读写"),
    ("csv", "CSV 读写"),
    ("time", "时间"),
    ("re", "正则表达式"),
    ("collections", "高级数据结构"),
    ("itertools", "迭代工具"),
]
print(f"  {'模块':<14}用途")
print("  " + "-" * 36)
for 名, 用途 in 模块们:
    print(f"  {名:<14}{用途}")

print("\n⑨ 自己写模块的典型结构（示意）")
print("""
    \"\"\"模块说明。\"\"\"

    import os

    默认路径 = "config.json"

    def 读配置(路径=默认路径):
        \"\"\"读配置文件。\"\"\"
        ...

    if __name__ == "__main__":
        print("自测开始")
""")

print("⑩ 常见错误")
print("  1. ModuleNotFoundError → 文件名拼错 / 不在同一目录")
print("  2. 自己写 random.py → 覆盖了标准库")
print("  3. 忘了 if __name__ == '__main__' → 导入时执行了一堆代码")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  设计一个模块
# ─────────────────────────────────────────
#
# 设计一个 `文本工具` 模块，包含：
#
#   · 常量：常用标点字符串
#   · 函数：
#       切词(文本)          去标点、转小写、跳过空词
#       统计词频(文本)      返回字典
#       高亮(文本, 词)      用【】标出
#       取前几句(文本, n)
#   · 每个函数有 docstring
#   · 末尾有 `if __name__ == "__main__":` 的自测
#
# 要求：
#   因为只有一个文件，就把所有内容写在这个文件里。
#   但要想清楚：如果拆成两个文件，怎么拆？
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  用标准库解决问题
# ═════════════════════════════════════════
#
# 用标准库解决下面这些问题（不许自己手写算法）：
#
#   A. 求 100 以内的所有素数（提示：可以自己写，也可以查 itertools）
#   B. 生成 10 个 1~100 的不重复随机数
#   C. 算出「今天」是这一年的第几天
#   D. 把「2026-03-09」转成「2026年3月9日 星期一」
#   E. 计算 5 的阶乘、最大公约数、平方根
#   F. 把一个列表随机打乱
#
# 要求：
#   · 尽量用 math / random / datetime 里的现成函数
#   · 每个都跑一遍验证
#   · 说明：哪些事标准库做不到，必须自己写
#
# 你的代码：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    """文本工具模块（示意）。"""

    标点 = ".,!?;:\"'()[]{}，。！？；：（）"


    def 切词(文本):
        """去标点、转小写、跳过空词。"""
        词们 = []
        for 词 in 文本.split():
            干净 = 词.strip(标点).lower()
            if 干净:
                词们.append(干净)
        return 词们


    def 统计词频(文本):
        """返回 {词: 次数}。"""
        次数 = {}
        for 词 in 切词(文本):
            次数[词] = 次数.get(词, 0) + 1
        return 次数


    def 高亮(文本, 关键词):
        """把关键词用【】标出来（忽略大小写）。"""
        结果 = ""
        i = 0
        小文本 = 文本.lower()
        小词 = 关键词.lower()
        长度 = len(关键词)

        while i < len(文本):
            if 小文本[i:i + 长度] == 小词:
                结果 += "【" + 文本[i:i + 长度] + "】"
                i += 长度
            else:
                结果 += 文本[i]
                i += 1
        return 结果


    def 取前几句(文本, n=3):
        """按句末标点切句，取前 n 句。"""
        句们 = []
        当前 = ""
        for c in 文本:
            当前 += c
            if c in "。！？.!?":
                句们.append(当前.strip())
                当前 = ""
        if 当前.strip():
            句们.append(当前.strip())
        return 句们[:n]


    if __name__ == "__main__":
        测试 = "The cat and the dog. The cat is happy! And the dog too."
        print("切词：", 切词(测试))
        print("词频：", 统计词频(测试))
        print("高亮：", 高亮(测试, "cat"))
        print("前两句：", 取前几句(测试, 2))

    —— 「如果拆成两个文件，怎么拆」：

       **方案一：按「工具 / 演示」拆**

           文本工具.py       ← 只有函数和常量
           demo.py           ← import 文本工具，然后演示

        `文本工具.py` 末尾不需要 `if __name__ == "__main__"`
        （因为它本来就不是用来直接运行的）。

       **方案二：按功能拆**

           切词.py
           统计.py
           高亮.py

        太碎了。四个函数不值得拆成四个文件。

       —— 判断标准：
           「这一组代码会不会被别的项目复用？」
           会 → 单独成模块
           不会 → 留在主文件里

       **一个模块应该「高内聚」——相关的功能放在一起。**

    —— 一个细节：

       `标点` 这个常量用大写更规范吗？

           Python 的约定：

               普通变量    小写
               常量        全大写（PI、MAX_SIZE）
               但中文没法「全大写」

           所以中文常量直接写就行，或者加个前缀：

               标点_全角 = "..."
               标点_半角 = "...,;"

       命名要让「这是个常量」这件事看得出来。

题 2
    A. 求 100 以内素数

       自己写（因为标准库里没有「求素数」这个函数）：

            def 是素数(n):
                if n < 2:
                    return False
                i = 2
                while i * i <= n:
                    if n % i == 0:
                        return False
                    i += 1
                return True

            素数们 = [n for n in range(2, 101) if 是素数(n)]

       —— 标准库**没有**素数函数，必须自己写。

    B. 10 个 1~100 的不重复随机数

           import random
           结果 = random.sample(range(1, 101), 10)

       `random.sample(序列, k)` 就是「不重复地抽 k 个」。

       —— 注意不是 `random.choice` 用 10 次（会重复）。

    C. 今天是这一年的第几天

           import datetime
           今天 = datetime.date.today()
           第几天 = 今天.timetuple().tm_yday
           # 或者
           第几天 = 今天 - datetime.date(今天.year, 1, 1) + datetime.timedelta(days=1)
           第几天 = 第几天.days

       更简单：

           第几天 = int(今天.strftime("%j"))       ← %j 是「年内第几天」

    D. 日期格式化 + 星期

           import datetime
           d = datetime.datetime.strptime("2026-03-09", "%Y-%m-%d")

           星期们 = ["星期一", "星期二", "星期三", "星期四",
                     "星期五", "星期六", "星期日"]
           星期 = 星期们[d.weekday()]        ← weekday() 周一=0

           print(f"{d.year}年{d.month}月{d.day}日 {星期}")

       或者用 strftime：

           d.strftime("%Y年%m月%d日 %A")

       ⚠ `%A` 输出的是英文（Monday），中文要看系统 locale。

       所以「中文星期」最好自己映射。

    E. 阶乘、最大公约数、平方根

           import math

           math.factorial(5)       → 120
           math.gcd(48, 18)        → 6
           math.sqrt(16)           → 4.0

       —— 三个都有现成的。这是标准库的典型价值。

    F. 打乱列表

           import random
           random.shuffle(名单)        ← 原地打乱
           random.sample(名单, len(名单))  ← 返回新的

    —— 「哪些事标准库做不到」：

       ① 求素数 —— 没有内置
       ② 中文分词 —— 没有（要 jieba 这类第三方库）
       ③ 中文星期/月份 —— 没有内置映射
       ④ 复杂的日期计算（「下个月的第 3 个星期五」）—— 要用 dateutil 或自己算
       ⑤ 业务规则 —— 当然只能自己写

       —— 标准库覆盖的是「通用需求」。
          越具体的业务，越要自己写。

    —— 一个实用的习惯：

       遇到一个「应该有现成解法」的问题，先搜一下：

            Python 怎么算最大公约数
            → 找到 math.gcd

       别急着自己写循环 —— 标准库的实现更快更可靠。
'''
