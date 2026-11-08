r'''
════════════════════════════════════════════════════════
  L5 · 第 5 课 · 用法 2        常用标准库实战
════════════════════════════════════════════════════════

上一节讲了「怎么导入」，这一节讲「导进来能干什么」。

挑六个最常用的模块，每个讲最实用的部分。

────────────────────────────────────────────────────────
【os：路径和文件系统】
════════════════════════════════════════════════════════

        import os

    ── 路径拼接：os.path.join ──

        os.path.join("数据", "2026", "a.csv")
        → "数据/2026/a.csv"        （Linux）
        → "数据\\2026\\a.csv"       （Windows）

    ⚠ **永远用 join，不要手写 `"数据/" + "a.csv"`**

        因为不同系统的分隔符不同。

    ── 拆路径 ──

        os.path.basename("a/b/c.txt")    → "c.txt"
        os.path.dirname("a/b/c.txt")     → "a/b"
        os.path.splitext("c.txt")        → ("c", ".txt")

    ── 判断 ──

        os.path.exists(路径)             存在吗
        os.path.isfile(路径)             是文件吗
        os.path.isdir(路径)              是目录吗

    ── 操作 ──

        os.makedirs(路径, exist_ok=True)   创建目录（含中间层）
        os.listdir(目录)                   列出内容
        os.remove(文件)                    删文件
        os.rmdir(目录)                     删空目录
        os.rename(旧, 新)                  改名/移动

    ── 创建目录的标准写法 ──

        os.makedirs("数据/2026/03", exist_ok=True)

        `exist_ok=True` 表示「已存在也不报错」。

        不加的话，目录已存在会抛 FileExistsError。

    ── 一个坑：删目录 ──

        `os.rmdir` 只能删**空目录**。

        要删非空目录：

            import shutil
            shutil.rmtree(路径)        ← 危险！会删掉所有内容

        ⚠ 这个操作不可恢复。用之前想三遍。

────────────────────────────────────────────────────────
【datetime：日期时间】
════════════════════════════════════════════════════════

        from datetime import datetime, date, timedelta

    ── 现在 ──

        datetime.now()              → 2026-03-09 10:23:45.123456
        date.today()                → 2026-03-09

    ── 格式化：strftime ──

        常见占位符：

            %Y      四位年        2026
            %m      两位月        03
            %d      两位日        09
            %H      24 小时       10
            %M      分            23
            %S      秒            45
            %A      星期（英文）   Monday
            %j      年内第几天     068

        例：

            现在.strftime("%Y年%m月%d日 %H:%M")
            → "2026年03月09日 10:23"

    ── 解析：strptime ──

        datetime.strptime("2026-03-09", "%Y-%m-%d")
        → datetime(2026, 3, 9, 0, 0)

        ⚠ 格式必须完全匹配，否则 ValueError：

            strptime("2026/03/09", "%Y-%m-%d")     ❌

    ── 时间加减：timedelta ──

        现在 + timedelta(days=3)          三天后
        现在 - timedelta(hours=2)         两小时前
        日期2 - 日期1                      得到 timedelta（差多少天）

        (date(2026,3,9) - date(2026,3,1)).days     → 8

    ── 星期 ──

        d.weekday()        周一=0，周日=6
        d.isoweekday()     周一=1，周日=7

        中文星期要自己映射：

            星期们 = ["一", "二", "三", "四", "五", "六", "日"]
            f"星期{星期们[d.weekday()]}"

────────────────────────────────────────────────────────
【random：随机】
════════════════════════════════════════════════════════

        import random

        random.random()             0.0 ~ 1.0 的浮点
        random.randint(1, 10)       1~10 的整数（含两端）
        random.uniform(1, 10)       1.0~10.0 的浮点
        random.choice(列表)         随机选一个
        random.sample(列表, k)      不重复地选 k 个
        random.shuffle(列表)        原地打乱

    ── 关键：可重现的随机 ──

        random.seed(42)
        random.randint(1, 100)      → 每次运行都是同一个数

        用途：测试时固定随机结果，方便调试。

        **不加 seed，每次运行结果不同；加了 seed，可以重现。**

    ── 一个常见误解 ──

        「random 是真随机吗？」不是，它是「伪随机」——
        用一个确定的算法生成看起来随机的序列。

        对普通用途足够了。真随机要用 `secrets` 模块。

    ── 抽奖的正确写法 ──

        ❌ 抽 3 个不同的：
              [random.choice(名单) for _ in range(3)]
              ← 可能重复

        ✅
              random.sample(名单, 3)

────────────────────────────────────────────────────────
【collections.Counter：计数器】
════════════════════════════════════════════════════════

    这个模块能省掉一堆手写代码。

        from collections import Counter

    ── 一句话统计 ──

        Counter("hello")
        → Counter({'l': 2, 'h': 1, 'e': 1, 'o': 1})

        Counter(["a", "b", "a", "c"])
        → Counter({'a': 2, 'b': 1, 'c': 1})

    **比手写 `次数[词] = 次数.get(词, 0) + 1` 短多了。**

    ── 取前 N 个 ──

        Counter(词们).most_common(3)
        → [('the', 5), ('a', 3), ('is', 2)]

    ── 它就是个字典 ──

        c = Counter("aab")
        c["a"]              → 2
        c["z"]              → 0        ← 不存在的键返回 0，不报错！
        dict(c)             → {'a': 2, 'b': 1}

        —— 这个「默认 0」的特性让它特别好用：

            c["新词"] += 1      ← 不需要先判断存不存在

    ── 其他好用的方法 ──

        c.most_common()            按次数降序
        c.total()                  总数（Python 3.10+）
        c1 + c2                    合并计数
        c1 - c2                    相减（只保留正数）

────────────────────────────────────────────────────────
【math：数学】
════════════════════════════════════════════════════════

        import math

        math.sqrt(16)          4.0        平方根
        math.floor(3.7)        3          向下取整
        math.ceil(3.2)         4          向上取整
        math.fabs(-5)          5.0        绝对值（浮点）
        math.factorial(5)      120        阶乘
        math.gcd(48, 18)       6          最大公约数
        math.isclose(a, b)                浮点比较（L5 第 2 课）
        math.pi                3.14159... 圆周率
        math.e                 2.71828... 自然常数

    ── `floor` 和 `int()` 的区别 ──

        math.floor(-3.5)    → -4        向下（更小）
        int(-3.5)           → -3        向零（更接近 0）

        L1 第 3 课讲过这个区别。

    ── `round` 是内置的，不在 math 里 ──

        round(3.5)          → 4        内置
        math.floor(3.5)     → 3        math 里的

────────────────────────────────────────────────────────
【time：时间和睡眠】
════════════════════════════════════════════════════════

        import time

        time.time()                 当前时间戳（秒，浮点）
        time.sleep(1.5)             睡 1.5 秒
        time.strftime("%Y-%m-%d")   格式化当前时间
        time.perf_counter()         高精度计时（测性能用）

    ── 测代码性能的标准写法 ──

        开始 = time.perf_counter()
        做点事()
        耗时 = time.perf_counter() - 开始
        print(f"耗时 {耗时 * 1000:.2f} 毫秒")

        `perf_counter` 比 `time.time()` 精度更高，
        而且不受系统时间调整的影响。

    ── `time.strftime` 和 `datetime.strftime` ──

        两个都能格式化，但 `datetime` 更灵活（能处理任意日期）。

        `time.strftime` 只能格式化「当前时间」或「时间戳」。

────────────────────────────────────────────────────────
【什么时候用哪个】
════════════════════════════════════════════════════════

    ┌──────────────────┬────────────────────────────────┐
    │ 要处理路径/文件  │ os.path                        │
    │ 要处理日期       │ datetime                       │
    │ 要随机           │ random                         │
    │ 要计数           │ collections.Counter            │
    │ 要数学运算       │ math                           │
    │ 要测性能         │ time.perf_counter              │
    └──────────────────┴────────────────────────────────┘

    ── 一个原则 ──

        **先查标准库，再自己写。**

        你想到的「通用需求」，99% 已经有现成实现，
        而且比自己写的更快、更可靠。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① os.path：路径处理")
import os

print("  join('数据', '2026', 'a.csv') =",
      os.path.join("数据", "2026", "a.csv"))
print("  basename('a/b/c.txt') =", os.path.basename("a/b/c.txt"))
print("  dirname('a/b/c.txt')  =", os.path.dirname("a/b/c.txt"))
print("  splitext('c.tar.gz')  =", os.path.splitext("c.tar.gz"))
print("  当前目录存在：", os.path.isdir("."))

print("\n② datetime：日期时间")
from datetime import datetime, date, timedelta

现在 = datetime.now()
今天 = date.today()

print("  现在：", 现在.strftime("%Y-%m-%d %H:%M:%S"))
print("  今天：", 今天)
print("  格式化：", 现在.strftime("%Y年%m月%d日 %H:%M"))
print("  年内第几天：", 现在.strftime("%j"))

星期们 = ["一", "二", "三", "四", "五", "六", "日"]
print("  星期：星期" + 星期们[今天.weekday()])

print("\n  三天后：", (今天 + timedelta(days=3)))
print("  一周前：", (今天 - timedelta(weeks=1)))

差 = date(2026, 3, 9) - date(2026, 3, 1)
print("  3月9日 - 3月1日 =", 差.days, "天")

print("\n  解析字符串：")
解析 = datetime.strptime("2026-03-09 14:30", "%Y-%m-%d %H:%M")
print("    ", 解析)
print("    类型：", type(解析).__name__)

print("\n③ random：随机")
import random

random.seed(42)
print("  seed(42) 之后：")
print("    randint(1, 100) =", random.randint(1, 100))
print("    random() =", round(random.random(), 4))

random.seed(42)
print("  再次 seed(42)：")
print("    randint(1, 100) =", random.randint(1, 100))
print("    ↑ 和上面一样（可重现）")

random.seed()
名单 = list(range(1, 11))
print("\n  原始列表：", 名单)
random.shuffle(名单)
print("  打乱后：  ", 名单)
print("  抽 3 个不重复：", random.sample(名单, 3))
print("  随机选一个：", random.choice(名单))

print("\n④ Counter：计数器")
from collections import Counter

文本 = "the cat and the dog and the bird"
词们 = 文本.split()

计数 = Counter(词们)
print("  Counter(词们) =", 计数)
print("  most_common(3) =", 计数.most_common(3))
print("  计数['the'] =", 计数["the"])
print("  计数['不存在'] =", 计数["不存在"], " ← 返回 0，不报错")

print("\n  字符统计：")
print("  Counter('hello') =", Counter("hello"))
print("  最常见的字符：", Counter("hello").most_common(1))

print("\n  Counter 加法的妙用：")
a = Counter("aab")
b = Counter("abbc")
print("    a =", a)
print("    b =", b)
print("    a + b =", a + b)
print("    a - b =", a - b, " ← 只保留正数部分")

print("\n⑤ math")
import math

print("  sqrt(16)      =", math.sqrt(16))
print("  floor(3.7)    =", math.floor(3.7))
print("  floor(-3.5)   =", math.floor(-3.5))
print("  int(-3.5)     =", int(-3.5), " ← 向零取整，和 floor 不同")
print("  ceil(3.2)     =", math.ceil(3.2))
print("  factorial(5)  =", math.factorial(5))
print("  gcd(48, 18)   =", math.gcd(48, 18))
print("  pi            =", round(math.pi, 6))

print("\n⑥ time：测性能")
import time

开始 = time.perf_counter()
总 = 0
for i in range(1000000):
    总 += i
耗时 = time.perf_counter() - 开始
print(f"  100 万次加法：{耗时 * 1000:.2f} 毫秒")

开始 = time.perf_counter()
总2 = sum(range(1000000))
耗时2 = time.perf_counter() - 开始
print(f"  用 sum()：    {耗时2 * 1000:.2f} 毫秒")
print(f"  内置快了 {耗时 / 耗时2:.0f} 倍")

print("\n⑦ 综合：一段带日期和随机的日志")
random.seed(1)
级别们 = ["INFO", "WARN", "ERROR"]
for i in range(5):
    时间 = datetime.now() + timedelta(minutes=i * 7)
    级别 = random.choice(级别们)
    print(f"  [{时间.strftime('%H:%M:%S')}] [{级别}] 第 {i + 1} 条记录")

print("\n⑧ 综合：统计日志级别")
假日志 = [random.choice(级别们) for _ in range(100)]
分布 = Counter(假日志)
for 级别, n in 分布.most_common():
    print(f"  {级别:<8}{n:>3} 次  {'█' * (n // 2)}")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  日期工具集
# ─────────────────────────────────────────
#
# 用 datetime 写这几个函数：
#
#   A. def 中文日期(日期对象)       "2026年3月9日 星期一"
#   B. def 几天后(日期字符串, n)    输入 "2026-03-09"，返回 n 天后的字符串
#   C. def 相差几天(日期1, 日期2)   两个日期字符串相差几天
#   D. def 是周末(日期字符串)       True/False
#   E. def 本月的天数(年, 月)       返回那个月有多少天
#
# 要求：
#   · 全部用 datetime
#   · 处理「日期格式不对」的情况（抛异常或返回 None）
#   · 测试 5 个用例，包括跨年、闰年
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  抽奖程序
# ─────────────────────────────────────────
#
# 写一个抽奖程序：
#
#   · 一等奖 1 名、二等奖 2 名、三等奖 3 名
#   · 不能重复中奖
#   · 用 random.sample 或 shuffle
#   · 输出获奖名单
#   · 用 seed 固定结果，方便核对
#
# 要求：
#   · 至少 20 个参与者
#   · 用 Counter 统计「每人中奖次数」，验证没有重复
#   · 再写一个「多次抽奖，统计每个人的中奖概率」的模拟（1000 次）
#
# 你的代码：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    from datetime import datetime, date, timedelta

    星期们 = ["星期一", "星期二", "星期三", "星期四",
              "星期五", "星期六", "星期日"]


    def 中文日期(日期对象):
        """返回「2026年3月9日 星期一」。"""
        return (f"{日期对象.year}年{日期对象.month}月{日期对象.day}日 "
                f"{星期们[日期对象.weekday()]}")


    def 解析日期(字符串):
        """解析 YYYY-MM-DD，失败返回 None。"""
        try:
            return datetime.strptime(字符串, "%Y-%m-%d").date()
        except ValueError:
            return None


    def 几天后(日期字符串, n):
        """返回 n 天后的日期字符串。"""
        日期 = 解析日期(日期字符串)
        if 日期 is None:
            return None
        return (日期 + timedelta(days=n)).strftime("%Y-%m-%d")


    def 相差几天(日期1, 日期2):
        """返回相差的天数（日期2 - 日期1）。"""
        d1 = 解析日期(日期1)
        d2 = 解析日期(日期2)
        if d1 is None or d2 is None:
            return None
        return (d2 - d1).days


    def 是周末(日期字符串):
        日期 = 解析日期(日期字符串)
        if 日期 is None:
            return None
        return 日期.weekday() >= 5


    def 本月的天数(年, 月):
        """返回那个月的天数。"""
        if 月 == 12:
            下月 = date(年 + 1, 1, 1)
        else:
            下月 = date(年, 月 + 1, 1)
        本月 = date(年, 月, 1)
        return (下月 - 本月).days


    测试：

        print(中文日期(date(2026, 3, 9)))        → 2026年3月9日 星期一
        print(几天后("2026-03-09", 10))          → 2026-03-19
        print(几天后("2026-12-25", 10))          → 2027-01-04  ← 跨年
        print(相差几天("2026-03-01", "2026-03-09"))  → 8
        print(是周末("2026-03-14"))              → True（周六）
        print(是周末("2026-03-09"))              → False（周一）
        print(本月的天数(2026, 2))               → 28
        print(本月的天数(2024, 2))               → 29  ← 闰年

    —— 几个关键点：

       ① `本月的天数` 用「下个月第一天 - 这个月第一天」
          优雅地避开了「闰年 2 月是 28 还是 29」的判断。

          这是 datetime 的典型用法：
          **让库处理复杂规则，你只管减法。**

       ② `星期们[日期.weekday()]`
          weekday() 周一=0，所以列表第一个是「星期一」。

       ③ `解析日期` 返回 None 而不是抛异常
          让调用方判断。也可以让它抛，看需求。

       ④ 跨年的情况 `2026-12-25 + 10 天 = 2027-01-04`
          datetime 自动处理了月份和年份的进位 —— 不需要你写 if。

    —— 如果用 `strftime("%A")` 输出星期：
       会得到 "Monday"（英文），因为中文依赖系统的 locale。

       自己映射更可靠。

题 2
    import random
    from collections import Counter

    参与者 = [f"选手{i:02d}" for i in range(1, 21)]

    print("参与者：", 参与者)

    # 打乱之后按顺序取
    副本 = 参与者.copy()
    random.shuffle(副本)

    一等奖 = 副本[0:1]
    二等奖 = 副本[1:3]
    三等奖 = 副本[3:6]

    print("\n获奖名单：")
    print("  一等奖：", 一等奖)
    print("  二等奖：", 二等奖)
    print("  三等奖：", 三等奖)

    # 验证没有重复
    全部中奖 = 一等奖 + 二等奖 + 三等奖
    print(f"\n共 {len(全部中奖)} 人获奖")
    print("有重复吗：", len(全部中奖) != len(set(全部中奖)))

    统计 = Counter(全部中奖)
    print("每人中奖次数：", dict(统计))

    —— 为什么用 shuffle 而不是多次 sample：

       `random.sample(参与者, 6)` 也能抽 6 个不重复的，
       然后按顺序分成 1、2、3。

       但「打乱后切片」更直观：

           一等奖 = 打乱后的前 1 个
           二等奖 = 接下来的 2 个
           ...

       —— 两种都对，选你能看懂的。

    —— 多次抽奖模拟：

        def 一次抽奖():
            副本 = 参与者.copy()
            random.shuffle(副本)
            return 副本[:6]          # 6 个人中奖

        中奖次数 = Counter()
        for _ in range(1000):
            获奖者 = 一次抽奖()
            中奖次数.update(获奖者)

        print("1000 次抽奖后，各人的中奖次数：")
        for 人, 次 in 中奖次数.most_common(5):
            print(f"  {人}：{次} 次  ({次 / 1000 * 100:.1f}%)")

    —— 输出大概是这样：

          选手01：320 次  (32.0%)
          选手07：310 次  (31.0%)
          ...

       每次抽 6 人 / 20 人 = 30%，所以每个人的中奖率应该接近 30%。

       实际跑出来会在 25%~35% 之间波动（随机性）。

       —— 跑 10000 次会更接近 30%。

       **这就是「用模拟验证概率」的思路。**

    —— `Counter.update(列表)`
       会把这个列表里的每个元素都计一次数。

       比循环 `中奖次数[人] += 1` 短。

    —— 一个概率上的细节：

       如果「一等奖、二等奖、三等奖」的抽取是**依次**进行的：

           第 1 次：从 20 人里抽 1 个
           第 2 次：从剩下的 19 人里抽 2 个
           ...

       那每个人的「获得一等奖」的概率是不同的（取决于顺序）。

       而「一次性抽 6 个再分配」，每个人的概率完全相同。

       **游戏规则要写清楚，否则玩家会觉得不公平。**
'''
