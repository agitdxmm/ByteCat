r'''
════════════════════════════════════════════════════════
  YCL4 · 冲刺 · 第 4 讲        第三方库：jieba 与 wordcloud
════════════════════════════════════════════════════════

考纲：

    「掌握模块及常用标准库的功能与用法……
      理解 jieba、wordcloud 等第三方库的获取与使用方法。」

「获取」两个字是关键 —— 意思是：**你得知道怎么把它装上来。**

这一讲就讲三件事：

    ① pip 是什么，怎么装
    ② jieba 怎么分词（中文的分词是个真问题）
    ③ wordcloud 怎么出图

────────────────────────────────────────────────────────
【先分清：标准库 vs 第三方库】
────────────────────────────────────────────────────────

    ┌─ 标准库（装 Python 就有，直接 import）
    │     math、random、time、datetime、os、json、csv、bisect、collections
    │
    └─ 第三方库（要额外装，装完才能 import）
          jieba、wordcloud、requests、numpy、pandas、matplotlib

    ── 判断方法 ──

        `import math` 能用 → 标准库
        `import jieba` 报 ModuleNotFoundError → 要么没装，要么装错了环境

    ── 那个报错长这样 ──

        ModuleNotFoundError: No module named 'jieba'

        看到这句，第一反应就是「没装」。
        但还有一种情况：装到了另一个 Python 上（见下面「常见坑」）。

────────────────────────────────────────────────────────
【pip：Python 的「应用商店」】
────────────────────────────────────────────────────────

    pip install jieba                  装
    pip uninstall jieba                卸
    pip list                           看装了什么
    pip show jieba                     看某个包的详情
    pip install jieba==0.42.1          装指定版本

    ── 国内的网速问题 ──

        直接 pip install 会连 pypi.org，国内经常龟速或超时。

        换镜像源（清华的）：

            pip install jieba -i https://pypi.tuna.tsinghua.edu.cn/simple

        或者一次设好，以后都走镜像：

            pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

    ── 版本号怎么写 ──

        jieba           最新版
        jieba==0.42.1   就这个版本
        jieba>=0.42     这个版本以上
        jieba<1.0       这个版本以下

        考卷不会问这个，但 `pip install 包名` 这一条要知道。

────────────────────────────────────────────────────────
【jieba：中文为什么要单独分词】
────────────────────────────────────────────────────────

英文分词超简单 —— 空格就是分隔符：

    "I love Python".split()     → ['I', 'love', 'Python']

中文不行，句子是连着的：

    "我喜欢编程".split()        → ['我喜欢编程']      一个词都没分开

所以需要一个「知道中文词边界」的工具。jieba 就是干这个的。

    ── 三种模式 ──

        jieba.cut(文本)               精确模式（默认，最常用）
        jieba.cut(文本, cut_all=True) 全模式（把所有可能的词都切出来）
        jieba.cut_for_search(文本)    搜索引擎模式（长词再切细一遍）

        实测一句话你就明白了：

            原文：小猫咪在玩我的世界

            精确模式： 小猫咪 / 在 / 玩 / 我 / 的 / 世界
            全模式：   小猫 / 小猫咪 / 猫咪 / 在 / 玩 / 我 / 的 / 世界
            搜索模式： 小猫 / 猫咪 / 小猫咪 / 在 / 玩 / 我 / 的 / 世界

        **精确模式**：最贴近人的理解，做词频统计用它
        **全模式**：宁可错切也不漏，会有重叠的废话词
        **搜索模式**：精确模式的基础上，把长词再切出短词

    ── cut() 返回的是什么 ──

        一个「生成器」，不是列表。

            jieba.cut(文)          → <generator object ...>
            list(jieba.cut(文))    → ['小猫咪', '在', '玩', ...]
            "/".join(jieba.cut(文)) → '小猫咪/在/玩/...'

        要当下标访问、要 len()，必须先 list() 一下。

        这一点和上一讲的 filter / map 是同一回事 ——
        Python 里凡是「生成器」，都得转成列表才能当列表用。

    ── 自定义词典：解决切错的问题 ──

        jieba 的词典是通用的，遇到专业词、人名、游戏术语容易切错。

        实测：「小明用红石做了一台刷怪塔」

            默认切法：小明用 / 红石 / 做 / 了 / 一台 / 刷怪 / 塔

            两处不对：
                「小明用」粘成一个词了（应该是 小明 + 用）
                「刷怪 / 塔」被拆开（应该是 刷怪塔）

        修法：把这几个词加进词典。

            jieba.add_word("小明")
            jieba.add_word("红石")
            jieba.add_word("刷怪塔")

            再切：小明 / 用 / 红石 / 做 / 了 / 一台 / 刷怪塔     全对

        批量加就用词典文件，一行一个词：

            jieba.load_userdict("我的词典.txt")

        词典文件格式（UTF-8，纯文本）：

            小明
            红石
            刷怪塔
            活塞门

        ⚠ 加词必须加全。

          只加「小明」不加「红石」，结果会变成：

              小明 / 用红石 / 做 / 了 / 一台 / 刷怪塔

          「用红石」又粘一起了。jieba 会用自己的规则去补空档，
          补出来的不一定是你想要的那个。

        ── 顺带：HMM 开关 ──

            jieba.cut(文本)               默认 HMM=True，会「发现新词」
            jieba.cut(文本, HMM=False)    只用词典，不猜新词

            实测对比「他最喜欢挖钻石和造红石机器」：

                HMM=True ：他/最/喜欢/挖/钻石/和造/红石/机器
                HMM=False：他/最/喜欢/挖/钻石/和/造/红石/机器

            HMM 把「和造」当成一个词了 —— 这是个真不存在的词。

            所以：**词典够全的时候，加 HMM=False 结果更稳。**

        这招在比赛和项目里很常用 —— 通用词典永远不够用。

    ── 顺带：词性标注 ──

        import jieba.posseg as pseg

        for 词, 词性 in pseg.cut("小猫咪在挖钻石"):
            print(词, 词性)

        → 小猫咪 n      （名词）
          在   p        （介词）
          挖   v        （动词）
          钻石 n

        考纲没要求，知道有这么个东西就行。

────────────────────────────────────────────────────────
【wordcloud：把词频画成图】
────────────────────────────────────────────────────────

它吃一段文本（或一个词频字典），吐一张图：
出现次数越多的词，字越大。

    ── 三个必知参数 ──

        WordCloud(
            font_path="C:/Windows/Fonts/msyh.ttc",   ← 中文必须指定
            width=800,
            height=400,
            background_color="white",
            max_words=100,
        )

    ── 为什么非要 font_path ──

        wordcloud 默认用的字体不含中文字形。
        不指定的话，图上全是「□□□」这种方框。

        Windows 常见中文字体路径：

            C:/Windows/Fonts/msyh.ttc      微软雅黑（推荐）
            C:/Windows/Fonts/simhei.ttf    黑体
            C:/Windows/Fonts/simsun.ttc    宋体

        这是初学者第一大坑 —— 图出来了，一看全是方块。

    ── 两种生成方式 ──

        ① 从一段文本生成（内部自己分词，但中文分词效果差）：

               wc.generate("Python 编程 函数 递归")

           注意：它按**空格**切词。中文连在一起会当成一个词。

        ② 从词频字典生成（推荐，配合 jieba 用）：

               wc.generate_from_frequencies({"Python": 50, "函数": 30})

           这个方式最可控 —— 你用什么分词、去什么停用词，自己说了算。

    ── 保存 ──

        wc.to_file("词云.png")

    ── 依赖 ──

        wordcloud 依赖 numpy（数值计算）和 pillow（图片处理）。
        pip install wordcloud 时会自动把它们一起装上。

        如果装的时候报「Microsoft Visual C++ 14.0 required」，
        说明它要现场编译。两种解法：

            ① 换成 64 位 Python（大概率有现成的 wheel 包）
            ② 先装 numpy，再装 wordcloud

────────────────────────────────────────────────────────
【装不上怎么办：try / except ImportError】
────────────────────────────────────────────────────────

这一条很重要，因为**考试机上不一定装了 jieba**。

代码要能优雅地降级，而不是直接崩：

    try:
        import jieba
        有jieba = True
    except ImportError:
        有jieba = False
        print("没装 jieba，改用简单切分")

    def 分词(文本):
        if 有jieba:
            return list(jieba.cut(文本))
        return 文本.split()          # 退化方案

    ── 这为什么重要 ──

        编程题如果因为「环境里没这个库」而崩掉，
        整题 0 分。加个 try 兜底，至少能跑起来拿部分分。

        这也是真实工程里的标准做法：
        **可选依赖要能优雅降级，不能硬崩。**

    ── ImportError 和 ModuleNotFoundError 的关系 ──

        ModuleNotFoundError 是 ImportError 的**子类**。
        写 `except ImportError` 能同时抓住两个。

        所以兜底统一写 ImportError 就行。
'''


# ═══════════════════════════════════════════════════════════
#  示例
# ═══════════════════════════════════════════════════════════

import sys
import os

print("① 先确认这些库在不在")
for 包名 in ["jieba", "wordcloud", "numpy"]:
    try:
        __import__(包名)
        print(f"   {包名:12s} ✓ 已安装")
    except ImportError:
        print(f"   {包名:12s} ✗ 没装（pip install {包名}）")

print(f"\n   Python 版本：{sys.version.split()[0]}")
print(f"   Python 路径：{sys.executable}")


print("\n② jieba 三种模式对比")
import jieba
jieba.setLogLevel(20)          # 关掉「Building prefix dict」那些提示

一句话 = "小猫咪在玩我的世界，他最喜欢挖钻石"
print("   原文：", 一句话)
print("   精确模式：", "/".join(jieba.cut(一句话)))
print("   全模式  ：", "/".join(jieba.cut(一句话, cut_all=True)))
print("   搜索模式：", "/".join(jieba.cut_for_search(一句话)))


print("\n③ cut() 返回的是生成器，不是列表")
结果 = jieba.cut(一句话)
print("   直接打印：", 结果)
print("   类型：", type(结果).__name__)
print("   转成列表：", list(jieba.cut(一句话))[:6], "...")


print("\n④ 切错了怎么办：自定义词典")
难句 = "小明用红石做了一台刷怪塔"
print("   原文：", 难句)
print("   默认切法：", "/".join(jieba.cut(难句)))
print("   ↑ 「小明用」粘在一起，「刷怪 / 塔」被拆开")

jieba.add_word("小明")
jieba.add_word("红石")
jieba.add_word("刷怪塔")
print("   加词之后：", "/".join(jieba.cut(难句)))
print("   ↑ 小明 / 用 / 红石 …… 刷怪塔，都对上了")

print("\n   对比 HMM 开关（另一句话）：")
对比句 = "他最喜欢挖钻石和造红石机器"
print("   HMM=True ：", "/".join(jieba.cut(对比句)))
print("   HMM=False：", "/".join(jieba.cut(对比句, HMM=False)))
print("   ↑ HMM 自己造了个「和造」，关掉就正常了")


print("\n⑤ 词频统计：分词 + 计数")


def 词频统计(文本, 停用词=()):
    计数 = {}
    for 词 in jieba.cut(文本):
        词 = 词.strip()
        if len(词) < 2:            # 单字丢掉
            continue
        if 词 in 停用词:
            continue
        计数[词] = 计数.get(词, 0) + 1
    return 计数


样本文本 = (
    "函数是组织代码的基本单位。函数可以接收参数，也可以返回结果。"
    "学会函数之后，代码可以复用。递归也是一种函数调用自己的方式。"
    "递归要写基线条件，不然会无限递归。二分查找也用到递归思想。"
    "二分查找要求数据有序，这是它的前提。分治是把问题拆成小问题。"
)
统计 = 词频统计(样本文本, 停用词={"可以", "也是", "一种", "自己", "要求"})
排好 = sorted(统计.items(), key=lambda x: -x[1])
print("   前 8 个高频词：")
for 词, 次 in 排好[:8]:
    print(f"      {词:8s} {次}")


print("\n⑥ wordcloud：生成一张词云")
try:
    from wordcloud import WordCloud

    字体 = None
    for 候选 in [r"C:\Windows\Fonts\msyh.ttc",
                 r"C:\Windows\Fonts\simhei.ttf",
                 r"C:\Windows\Fonts\simsun.ttc"]:
        if os.path.exists(候选):
            字体 = 候选
            break

    if 字体 is None:
        print("   找不到中文字体，跳过")
    else:
        print("   用字体：", 字体)
        词频 = {词: 次 * 100 for 词, 次 in 统计.items()}

        wc = WordCloud(
            font_path=字体,
            width=800,
            height=400,
            background_color="white",
            max_words=60,
        )
        wc.generate_from_frequencies(词频)
        输出路径 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "词云_输出.png")
        wc.to_file(输出路径)
        print("   已生成：", 输出路径)
        print("   大小：", os.path.getsize(输出路径), "字节")
        print("   ↑ 用看图软件打开看看，字越大表示出现越多")
except ImportError:
    print("   没装 wordcloud，跳过这一步")


print("\n⑦ try / except ImportError：装不上也不崩")


def 分词_可降级(文本):
    """有 jieba 用 jieba，没有就按空格切。"""
    try:
        import jieba
        # 注意：jieba.cut 会把空格也当成一个 token 吐出来，要滤掉
        return [词 for 词 in jieba.cut(文本) if 词.strip()]
    except ImportError:
        return 文本.split()


print("   直接 list(jieba.cut('函数 递归'))：", list(jieba.cut("函数 递归")))
print("   ↑ 空格单独成了一个元素，这是 jieba 的行为，不是 bug")
print("   分词_可降级('函数 递归 二分')：", 分词_可降级("函数 递归 二分"))
print("   ↑ 滤掉空白之后，两种环境下的结果形状才一致")


print("\n⑧ generate vs generate_from_frequencies")


def 演示两种生成():
    from wordcloud import WordCloud
    字体 = r"C:\Windows\Fonts\msyh.ttc"
    if not os.path.exists(字体):
        return "（没字体，跳过）"

    # 方式一：直接喂文本 —— 内部按空格切
    wc1 = WordCloud(font_path=字体, width=400, height=200, background_color="white")
    wc1.generate("python python python 函数 函数 递归")
    print("   方式一 generate(文本)：", dict(list(wc1.words_.items())[:5]))

    # 方式二：喂词频字典 —— 自己控制分词结果
    wc2 = WordCloud(font_path=字体, width=400, height=200, background_color="white")
    wc2.generate_from_frequencies({"python": 100, "函数": 60, "递归": 30})
    print("   方式二 generate_from_frequencies：", wc2.words_)
    return ""


print(演示两种生成())
print("   ↑ 方式一按空格切，中文连写的词会被当成一个整体")
print("     方式二你说了算，配合 jieba 用最稳")


# ═══════════════════════════════════════════════════════════
#  练习：3 道综合题
# ═══════════════════════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  真正的词频统计器
# ─────────────────────────────────────────
#
# 写一个函数：
#
#     def 分析文本(文本, 停用词, 前N=10):
#         """返回 (总词数, 不同词数, 前 N 个高频词列表)"""
#
# 要求：
#   · 用 jieba 精确模式分词
#   · 去掉：长度 < 2 的词、纯标点、停用词表里的词
#   · 高频词列表格式：[(词, 次数), ...]，按次数降序
#   · 次数相同按词的字母序（保证结果稳定）
#
# 用这段文本测试：
#
#     文本 = (
#         "学习编程最重要的是理解概念。概念清楚了，语法只是工具。"
#         "函数是一种工具，列表也是一种工具，字典也是工具。"
#         "但工具本身不会思考，思考的是人。所以要先想清楚再写代码。"
#         "写代码之前先想清楚，这比敲键盘重要得多。"
#     )
#     停用词 = {"一种", "也是", "只是", "不会", "所以", "之前"}
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  自定义词典
# ─────────────────────────────────────────
#
# 下面这段文本，jieba 默认会切错：
#
#     文本 = "他骑着末影龙飞到附魔台旁边，用下界合金修了把剑。"
#
# 实测默认切法：
#     他 / 骑 / 着 / 末影 / 龙飞 / 到 / 附魔台 / 旁边 / ，/ 用 / 下界 / 合金 / ……
#
# 两处错：
#     「末影 / 龙飞」→ 应该是 末影龙 + 飞
#     「下界 / 合金」→ 应该是 下界合金
#
# 要求：
#   ① 先输出默认切法，确认错在哪
#   ② 把切错的词加成自定义词（末影龙、下界合金）
#   ③ 再输出一次，对比
#   ④ 用 load_userdict 的方式也做一遍（写一个临时词典文件）
#
# 提示：
#   · add_word 是「当场加」
#   · load_userdict 是「从文件批量加」
#   · 临时词典文件记得在结束时删掉（os.remove）
#   · ⚠ 这题要新开一个 Python 窗口跑。
#     因为前面示例 ④ 已经 add_word 过几个词，
#     那些词在同一个进程里会一直生效，干扰对照。
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  生成一张真正的词云
# ─────────────────────────────────────────
#
# 综合前两题：读一段文本 → jieba 分词 → 去停用词 → 词频统计
# → 生成词云 PNG。
#
# 要求：
#   · 用 generate_from_frequencies（不要用 generate）
#   · font_path 自动找系统中文字体，找不到就打印提示并跳过
#   · 输出文件叫「我的词云.png」
#   · 打印：总词数、不同词数、前 5 个高频词、图片大小
#
# 文本自己写一段，至少 100 个字（写你学 Python 的感受就行）。
#
# 你的代码：


# ═══════════════════════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═══════════════════════════════════════════════════════════
r'''
题 1

    import jieba
    jieba.setLogLevel(20)


    def 分析文本(文本, 停用词, 前N=10):
        所有词 = []
        for 词 in jieba.cut(文本):
            词 = 词.strip()
            if len(词) < 2:
                continue
            if 词 in 停用词:
                continue
            if all(not c.isalnum() for c in 词):
                continue
            所有词.append(词)

        计数 = {}
        for 词 in 所有词:
            计数[词] = 计数.get(词, 0) + 1

        排好 = sorted(计数.items(), key=lambda x: (-x[1], x[0]))
        return len(所有词), len(计数), 排好[:前N]


    文本 = (
        "学习编程最重要的是理解概念。概念清楚了，语法只是工具。"
        "函数是一种工具，列表也是一种工具，字典也是工具。"
        "但工具本身不会思考，思考的是人。所以要先想清楚再写代码。"
        "写代码之前先想清楚，这比敲键盘重要得多。"
    )
    停用词 = {"一种", "也是", "只是", "不会", "所以", "之前"}

    总数, 不同数, 前N = 分析文本(文本, 停用词)
    print(f"总词数 {总数}，不同词 {不同数}")
    for 词, 次 in 前N:
        print(f"  {词:8s} {次}")

    —— 实测输出：
           总词数 28，不同词 17
             工具       5
             清楚       3
             代码       2
             先想       2
             思考       2
             概念       2
             重要       2
             函数       1
             列表       1
             字典       1

    —— 「工具」出现 5 次，是全文最高的：

           函数是一种工具
           列表也是一种工具
           字典也是工具
           语法只是工具
           但工具本身不会思考

        —— 数一下确实是 5 次。
           （「一种工具」里的「工具」也算，因为分词把「一种」和「工具」
             拆成了两个词，「一种」被停用词表过滤掉了。）

    —— `all(not c.isalnum() for c in 词)` 在干什么：

        isalnum() = 这个字符是字母或数字吗？
        not c.isalnum() = 既不是字母也不是数字（那就只能是标点）
        all(...) = **所有**字符都满足？

        整句读作：「这个词全是标点吗？」

        为什么要它：
        `len(词) < 2` 能滤掉单个标点，但滤不掉「。。」这种
        两个标点连在一起的（len 是 2）。

    —— 排序键 `(-x[1], x[0])`：

        次数降序，次数相同时按词的字符串升序。

        "代码" 的 Unicode 比 "工具" 小，但这里次数不一样（2 vs 5），
        所以按次数排就行。同分的情况看前面几个 2 分的：
        代码、先想、思考、概念、重要 —— 确实是按字符串排的。

    —— 关于「总词数 28」和「不同词 17」：

        28 是过滤后剩下的词的总个数（含重复）
        17 是去重后的个数

        相差 11，说明重复出现的有 11 次。

题 2

    import jieba
    import os

    jieba.setLogLevel(20)

    文本 = "他骑着末影龙飞到附魔台旁边，用下界合金修了把剑。"

    print("默认：", "/".join(jieba.cut(文本)))

    jieba.add_word("末影龙")
    jieba.add_word("下界合金")
    print("add_word：", "/".join(jieba.cut(文本)))

    # 第二条路：写词典文件
    词典路径 = "临时词典.txt"
    with open(词典路径, "w", encoding="utf-8") as f:
        f.write("末影龙\n")
        f.write("下界合金\n")

    jieba.load_userdict(词典路径)
    print("load_userdict：", "/".join(jieba.cut(文本)))
    os.remove(词典路径)

    —— 实测输出：

        默认：
           他/骑/着/末影/龙飞/到/附魔台/旁边/，/用/下界/合金/修/了/把/剑/。

        add_word：
           他/骑/着/末影龙/飞到/附魔台/旁边/，/用/下界合金/修/了/把/剑/。

        load_userdict：
           他/骑/着/末影龙/飞到/附魔台/旁边/，/用/下界合金/修/了/把/剑/。

    —— 默认切法错在两处：

           末影 / 龙飞      →  应该是 末影龙 + 飞
           下界 / 合金      →  应该是 下界合金

        jieba 的默认词典里没有「末影龙」「下界合金」，
        它就按规则硬切，切出了「末影」「龙飞」这种不存在的组合。

        注意「龙飞」还跨了语义边界 —— 「飞」是动词，
        被粘到了「龙」后面。这种错在词频统计里影响很大：
        本来该算给「飞」，结果算给了「龙飞」，两个词都统计错了。

    —— 加词后：

        「末影龙」「下界合金」都正确了。
        但「飞到」粘一起了 —— 这是 HMM 新词发现的副作用，
        对你这段文本不影响理解，可以不管。

        想彻底稳定：`jieba.cut(文本, HMM=False)`，
        但那要求词典足够全（上面讲过了）。

    —— add_word 和 load_userdict 结果一样吗？

        一样。两者做的事本质相同：往词典里塞词。
        区别只是「一个一个塞」和「从文件批量塞」。

        真实项目里用 load_userdict，因为：
            · 词表放文件里，改词不用改代码
            · 几百个词写几十行 add_word 太丑

    —— 一个必须知道的副作用：

        **add_word 改的是全局词典，整个进程都受影响。**

        你在示例 ④ 里加过「小明」「红石」「刷怪塔」，
        那之后这个进程里所有 jieba.cut 都会认得这些词。

        所以做「加词前后对比」的实验，一定要**新开一个进程**，
        否则对照组已经被污染了，看不出差别。

        这也是题目提示「新开窗口跑」的原因。

题 3

    import jieba
    import os
    from wordcloud import WordCloud

    jieba.setLogLevel(20)

    文本 = (
        "学Python最有意思的地方是能看到自己写的东西跑起来。"
        "刚开始学打印的时候觉得很简单，后来学循环觉得有点绕，"
        "学到函数才发现前面那些代码都能收进函数里，一下子就干净了。"
        "递归是最难的一关，汉诺塔想了很久才想明白，"
        "但想明白之后觉得特别漂亮，一个函数就把那么复杂的步骤说清楚了。"
        "现在学二分查找和分治，感觉像是在学怎么偷懒，"
        "把大问题拆成小问题，每个小问题都好解决。"
        "希望两个月后的考试能过。"
    )

    停用词 = {"的", "是", "了", "在", "和", "就", "都", "能", "把",
              "一个", "那些", "之后", "觉得", "自己", "时候", "有点"}

    计数 = {}
    总词数 = 0
    for 词 in jieba.cut(文本):
        词 = 词.strip()
        if len(词) < 2 or 词 in 停用词:
            continue
        if all(not c.isalnum() for c in 词):
            continue
        计数[词] = 计数.get(词, 0) + 1
        总词数 += 1

    排好 = sorted(计数.items(), key=lambda x: -x[1])
    print(f"总词数 {总词数}，不同词 {len(计数)}")
    for 词, 次 in 排好[:5]:
        print(f"  {词:8s} {次}")

    字体 = None
    for 候选 in [r"C://Windows//Fonts//msyh.ttc",
                 r"C://Windows//Fonts//simhei.ttf"]:
        if os.path.exists(候选):
            字体 = 候选
            break

    if 字体 is None:
        print("找不到中文字体，跳过生成")
    else:
        wc = WordCloud(font_path=字体, width=900, height=500,
                       background_color="white", max_words=80)
        wc.generate_from_frequencies(计数)
        wc.to_file("我的词云.png")
        print("已生成，", round(os.path.getsize("我的词云.png") / 1024, 1), "KB")

    —— 实测输出：
           总词数 51，不同词 46
             函数       3
             问题       3
             明白       2
             Python     1
             有意思     1

    —— 几个观察：

       ① 「函数」和「问题」都是 3 次，并列第一。
          排序时次数相同，就按字典的插入顺序（Python 3.7 起保序），
          所以和代码里谁先出现有关。

       ② 「学Python」被切开了，成了「学」+「Python」。
          「学」是单字，被 len<2 过滤掉，只剩 Python。
          这在词云里看着还行，不算问题。

       ③ 这组数字**换个 jieba 版本就会变**。
          词典每年都在更新，切分结果会有一两个词的差异。
          考试不会拿这种数字考你，我写出来只是让你能对照。

       ④ 「想明白」应该是 2 次，但前 5 里没出现 ——
          因为它和「明白」被切成了不同的词。
          「想明白」如果是整体，会单独算一次；
          这里 jieba 把它切成了「想」「明白」，所以「明白」2 次。

          **这就是分词质量直接影响统计结果的例子。**
          想让「想明白」算一个词：`jieba.add_word("想明白")`。

    —— 这题真正的考点不是词云，是这条流水线：

           原始文本
             ↓ jieba.cut
           词列表
             ↓ 过滤（长度 / 停用词 / 标点）
           干净词列表
             ↓ 计数
           词频字典
             ↓ generate_from_frequencies
           图片文件

        每一环都能单独出题：
        · 只考分词 → 给一句话，问切成什么
        · 只考过滤 → 给词列表，问剩下哪些
        · 只考统计 → 给文本，问哪个词最多
        · 考全流程 → 就是这道题

        考试时如果只问其中一环，别把整个流程都写上去，浪费时间。

    —— 最后：那个「我的词云.png」是跑出来的产物，
       看一眼就行，不用提交到 git。
'''
