r'''
════════════════════════════════════════════════════════
  L5 · 第 3 课 · 用法 3        CSV 与 JSON
════════════════════════════════════════════════════════

自己拼字符串写数据文件，会遇到一堆转义问题。

标准库提供了两个模块，专门解决这个。

────────────────────────────────────────────────────────
【CSV：表格数据】
════════════════════════════════════════════════════════

    CSV = Comma-Separated Values，逗号分隔值。

    用记事本打开长这样：

        姓名,语文,数学
        张三,92,88
        李四,78,90

    用 Excel 打开就是一张表。

    ── 用 csv 模块写 ──

        import csv

        with open("成绩.csv", "w", encoding="utf-8", newline="") as f:
            写 = csv.writer(f)
            写.writerow(["姓名", "语文", "数学"])
            写.writerow(["张三", 92, 88])
            写.writerow(["李四", 78, 90])

    ⚠ 必须加 `newline=""`

        否则 Windows 上每行之间会多一个空行。

        因为 csv 模块自己写 `\r\n`，而文本模式又会把 `\n` 转成 `\r\n`，
        两边都转就变成了 `\r\r\n`。

    ── 用 csv 模块读 ──

        with open("成绩.csv", "r", encoding="utf-8", newline="") as f:
            读 = csv.reader(f)
            for 行 in 读:
                print(行)

        每行是一个**字符串列表**：`['张三', '92', '88']`

        ⚠ 读出来的都是字符串，数字要自己转。

    ── 用字典形式（更方便）──

        with open("成绩.csv", "w", encoding="utf-8", newline="") as f:
            写 = csv.DictWriter(f, fieldnames=["姓名", "语文", "数学"])
            写.writeheader()
            写.writerow({"姓名": "张三", "语文": 92, "数学": 88})

        读：

        with open("成绩.csv", "r", encoding="utf-8", newline="") as f:
            读 = csv.DictReader(f)
            for 行 in 读:
                print(行)        → {'姓名': '张三', '语文': '92', ...}

    ── DictReader/Writer 好在哪 ──

        · 不用记「第几列是什么」
        · 加一列不用改代码
        · 读出来的直接是字典

    ── 为什么不用 split(",") ──

        CSV 有转义规则：

            字段里有逗号     → 用引号包起来   "张,三",92
            字段里有引号     → 引号翻倍       "他说""你好""",92
            字段里有换行     → 用引号包起来

        `split(",")` 处理不了这些。

        **csv 模块已经处理好所有边界情况。**

────────────────────────────────────────────────────────
【JSON：嵌套数据】
════════════════════════════════════════════════════════

    JSON 是「JavaScript 对象表示法」，现在是通用的数据交换格式。

    长这样：

        {
          "姓名": "张三",
          "成绩": {"语文": 92, "数学": 88},
          "爱好": ["读书", "编程"]
        }

    ── 和 Python 的对应 ──

        JSON 对象 {}     ↔  Python 字典
        JSON 数组 []     ↔  Python 列表
        JSON 字符串 ""   ↔  Python 字符串
        JSON 数字        ↔  Python int / float
        JSON true/false  ↔  Python True / False
        JSON null        ↔  Python None

    ── 四个函数 ──

        json.dumps(对象)        转成 JSON 字符串（dump**s** = dump string）
        json.dump(对象, 文件)   写进文件

        json.loads(字符串)      从字符串解析
        json.load(文件)         从文件读

    ── 写文件 ──

        import json

        数据 = {"姓名": "张三", "成绩": [92, 88]}

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(数据, f, ensure_ascii=False, indent=2)

    ⚠ 两个参数必加：

        `ensure_ascii=False`  否则中文会变成 `\u5f20\u4e09`
        `indent=2`            美化缩进，给人看

    ── 读文件 ──

        with open("data.json", "r", encoding="utf-8") as f:
            数据 = json.load(f)

        直接得到 Python 对象（字典/列表），不用自己解析。

    ── 打印 JSON 字符串 ──

        print(json.dumps(数据, ensure_ascii=False, indent=2))

    ── JSON 的严格规则 ──

        · 字符串必须用**双引号**（不能用单引号）
        · 最后一个元素后面不能有逗号
        · 不能有注释
        · 不能有 NaN / Infinity（标准 JSON）

        Python 的 `json` 模块比较宽容（能接受一些变体），
        但别的语言可能更严格。

        **写 JSON 时用标准格式。**

────────────────────────────────────────────────────────
【CSV vs JSON：什么时候用哪个】
════════════════════════════════════════════════════════

    ┌────────────┬──────────────────┬──────────────────┐
    │            │ CSV              │ JSON             │
    ├────────────┼──────────────────┼──────────────────┤
    │ 结构       │ 平的表格         │ 任意嵌套         │
    │ 人类可读   │ 很好（Excel 能开）│ 还行             │
    │ 体积       │ 小               │ 大一些           │
    │ 类型       │ 全是字符串       │ 保留类型         │
    │ 嵌套       │ 不支持           │ 支持             │
    │ 适合       │ 表格、导出 Excel │ 配置、API、嵌套  │
    └────────────┴──────────────────┴──────────────────┘

    ── 判断 ──

        数据能放进「一张表」→ CSV
        数据有嵌套（字典里套列表）→ JSON

    ── 一个反例 ──

        学生成绩：

            [{"名字": "张三", "语文": 92, "数学": 88}, ...]

        这个是平的（每行都是同样的字段），CSV 就行：

            名字,语文,数学
            张三,92,88

        但如果每个学生有「多门课外班」：

            [{"名字": "张三", "课外班": ["钢琴", "围棋"]}, ...]

        CSV 就难表达了（一个格子塞多个值，要自己约定分隔符）。

        JSON 天然支持。

────────────────────────────────────────────────────────
【读旧编码的 CSV】
════════════════════════════════════════════════════════

    从 Excel 导出的 CSV，往往是 GBK 编码（中文 Windows 默认）。

    直接读会报 UnicodeDecodeError。

    ── 两个办法 ──

        ✅ 用 Excel「另存为」时选 UTF-8
        ✅ 代码里写 encoding="gbk"

            with open("旧文件.csv", encoding="gbk") as f:
                ...

    ── 判断编码的笨办法 ──

        试着用 utf-8 读，报错就换 gbk：

            for 编码 in ["utf-8-sig", "gbk", "utf-8"]:
                try:
                    with open(路径, encoding=编码) as f:
                        内容 = f.read()
                    break
                except UnicodeDecodeError:
                    continue

        （`utf-8-sig` 会顺便处理 Excel 加的 BOM。）
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

import csv
import json
import os

CSV文件 = "演示成绩.csv"
JSON文件 = "演示数据.json"

print("① 写 CSV")
with open(CSV文件, "w", encoding="utf-8", newline="") as f:
    写 = csv.writer(f)
    写.writerow(["姓名", "语文", "数学", "英语"])
    写.writerow(["张三", 92, 88, 95])
    写.writerow(["李四", 78, 90, 85])
    写.writerow(["王五", 55, 48, 62])

with open(CSV文件, "r", encoding="utf-8") as f:
    print("  文件内容：")
    for 行 in f:
        print("    " + 行.rstrip())

print("\n② 读 CSV")
with open(CSV文件, "r", encoding="utf-8", newline="") as f:
    读 = csv.reader(f)
    for 行 in 读:
        print("  ", 行)

print("  ↑ 每行是字符串列表，数字要自己转")

print("\n③ 用 DictWriter 写")
CSV2 = "演示成绩2.csv"
with open(CSV2, "w", encoding="utf-8", newline="") as f:
    写 = csv.DictWriter(f, fieldnames=["姓名", "总分"])
    写.writeheader()
    写.writerow({"姓名": "张三", "总分": 275})
    写.writerow({"姓名": "李四", "总分": 253})

with open(CSV2, "r", encoding="utf-8", newline="") as f:
    print("  ", f.read().replace("\n", " | "))

print("\n④ 用 DictReader 读")
with open(CSV2, "r", encoding="utf-8", newline="") as f:
    读 = csv.DictReader(f)
    for 行 in 读:
        print("  ", 行)

print("\n⑤ CSV 的转义：字段里有逗号")
CSV3 = "演示转义.csv"
with open(CSV3, "w", encoding="utf-8", newline="") as f:
    写 = csv.writer(f)
    写.writerow(["名字", "备注"])
    写.writerow(["张三", "喜欢读书, 编程"])
    写.writerow(["李四", '他说"你好"'])

with open(CSV3, "r", encoding="utf-8") as f:
    print("  文件内容：")
    for 行 in f:
        print("    " + 行.rstrip())

with open(CSV3, "r", encoding="utf-8", newline="") as f:
    print("  读回来：")
    for 行 in csv.reader(f):
        print("  ", 行)
print("  ↑ 逗号被正确处理了，split(',') 做不到")

print("\n⑥ 写 JSON")
数据 = {
    "班级": "初一(3)班",
    "学生": [
        {"名字": "张三", "成绩": {"语文": 92, "数学": 88}, "爱好": ["读书", "编程"]},
        {"名字": "李四", "成绩": {"语文": 78, "数学": 90}, "爱好": ["篮球"]},
    ],
    "人数": 2,
    "已毕业": False,
    "备注": None,
}

with open(JSON文件, "w", encoding="utf-8") as f:
    json.dump(数据, f, ensure_ascii=False, indent=2)

print("  文件内容：")
with open(JSON文件, "r", encoding="utf-8") as f:
    for 行 in f:
        print("    " + 行.rstrip())

print("\n⑦ 读 JSON")
with open(JSON文件, "r", encoding="utf-8") as f:
    读回 = json.load(f)

print("  类型：", type(读回).__name__)
print("  班级：", 读回["班级"])
print("  第一个学生：", 读回["学生"][0])
print("  张三的语文：", 读回["学生"][0]["成绩"]["语文"])
print("  张三的爱好：", 读回["学生"][0]["爱好"])
print("  已毕业：", 读回["已毕业"], " 类型：", type(读回["已毕业"]).__name__)
print("  备注：", 读回["备注"])

print("\n⑧ ensure_ascii 的区别")
小数据 = {"名字": "张三"}
print("  ensure_ascii=True ：", json.dumps(小数据))
print("  ensure_ascii=False：", json.dumps(小数据, ensure_ascii=False))

print("\n⑨ 类型对照")
样本 = {
    "字符串": "abc",
    "整数": 42,
    "浮点": 3.14,
    "布尔": True,
    "空": None,
    "列表": [1, 2],
    "字典": {"k": "v"},
}
转成 = json.dumps(样本, ensure_ascii=False)
print("  ", 转成)

读回 = json.loads(转成)
print("  读回后各值类型：")
for 键, 值 in 读回.items():
    print(f"    {键:<8}{type(值).__name__}")

print("\n⑩ 读写往返：数据不变")
往返 = json.loads(json.dumps(数据, ensure_ascii=False))
print("  原数据和往返后相等：", 往返 == 数据)

print("\n⑪ JSON 能表达的嵌套（CSV 不行）")
嵌套 = [
    {"名字": "张三", "课外班": ["钢琴", "围棋"]},
    {"名字": "李四", "课外班": ["篮球"]},
]
print("  ", json.dumps(嵌套, ensure_ascii=False))
print("  ↑ 一个字段的值是个列表，CSV 很难表达")

print("\n⑫ 清理演示文件")
for 文件 in [CSV文件, CSV2, CSV3, JSON文件]:
    if os.path.exists(文件):
        os.remove(文件)
        print(f"  已删除 {文件}")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  成绩表 CSV 读写
# ─────────────────────────────────────────
#
# 要求：
#   · 用 csv.DictWriter 写一个 "成绩表.csv"：
#         字段：姓名、语文、数学、英语、总分、平均
#         数据：三个学生（自编）
#   · 用 csv.DictReader 读回来
#   · 算出班级平均分
#   · 找出总分最高的学生
#   · 注意读出来的是字符串，要转成数字
#   · 最后删除文件
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  JSON 配置管理
# ─────────────────────────────────────────
#
# 做一个「配置管理」小工具：
#
#   A. def 读配置(路径)      文件不存在时返回默认配置并创建文件
#   B. def 写配置(路径, 配置)
#   C. def 改配置(路径, 键, 值)
#   D. def 合并配置(路径, 新配置)   新配置覆盖旧的
#
# 默认配置：
#
#     {
#         "主题": "浅色",
#         "字号": 14,
#         "自动保存": True,
#         "最近打开": []
#     }
#
# 要求：
#   · 全部用 json 模块
#   · 要处理「文件损坏（不是合法 JSON）」的情况
#   · 测试：读默认 → 改字号 → 加最近打开 → 读回验证
#
# 你的代码：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.  json.dumps({"a": 1})
#   B.  json.dumps({"名": "张三"})
#   C.  json.dumps({"名": "张三"}, ensure_ascii=False)
#   D.  json.loads('{"a": 1}')["a"]
#   E.  json.loads('[1, 2, 3]')
#   F.  json.loads('{"ok": true}')["ok"]
#   G.  json.loads('{"x": null}')["x"]
#   H.  csv.writer 写一行 ["a", "b,c"] 结果是什么
#   I.  json.dumps([1, "a", None])
#   J.  json.loads('{"a": 1,}')     ← 末尾多逗号
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    import csv
    import os

    路径 = "成绩表.csv"
    数据 = [
        {"姓名": "张三", "语文": 92, "数学": 88, "英语": 95},
        {"姓名": "李四", "语文": 78, "数学": 90, "英语": 85},
        {"姓名": "王五", "语文": 55, "数学": 48, "英语": 62},
    ]

    # 加上总分和平均
    for 人 in 数据:
        总 = 人["语文"] + 人["数学"] + 人["英语"]
        人["总分"] = 总
        人["平均"] = round(总 / 3, 1)

    字段 = ["姓名", "语文", "数学", "英语", "总分", "平均"]

    with open(路径, "w", encoding="utf-8", newline="") as f:
        写 = csv.DictWriter(f, fieldnames=字段)
        写.writeheader()
        写.writerows(数据)

    # 读回来
    with open(路径, "r", encoding="utf-8", newline="") as f:
        读 = list(csv.DictReader(f))

    print("读回来：")
    for 行 in 读:
        print("  ", 行)

    # 注意：读出来全是字符串
    print("\n类型检查：")
    print("  姓名的类型：", type(读[0]["姓名"]).__name__)
    print("  语文的类型：", type(读[0]["语文"]).__name__)

    # 转数字
    for 行 in 读:
        行["语文"] = int(行["语文"])
        行["总分"] = int(行["总分"])
        行["平均"] = float(行["平均"])

    班级平均 = sum(行["总分"] for 行 in 读) / len(读)
    print(f"\n班级平均总分：{班级平均:.1f}")

    最高 = 读[0]
    for 行 in 读:
        if 行["总分"] > 最高["总分"]:
            最高 = 行
    print(f"总分最高：{最高['姓名']}（{最高['总分']}）")

    os.remove(路径)

    —— 几个关键点：

       ① `写.writerows(数据)` 是「一次写多行」
          等价于循环 `writerow`。

       ② **读出来的全是字符串**
          即使原来写的是数字 92，读回来是 "92"。

          这是 CSV 的本质：它没有类型，只有文本。

          —— 这和 JSON 不同，JSON 保留类型。

       ③ `round(总 / 3, 1)` 写了浮点，读回来是 "91.7"

       ④ 最后删除文件（练习用）

    —— 如果直接用 `split(",")` 会怎样：

       字段里的逗号会切错。而且引号转义完全不管。

       数据简单时可能「碰巧对」，但一旦有逗号就崩。

题 2
    import json
    import os

    默认配置 = {
        "主题": "浅色",
        "字号": 14,
        "自动保存": True,
        "最近打开": [],
    }


    def 读配置(路径):
        """读配置，不存在或损坏时返回默认配置。"""
        if not os.path.isfile(路径):
            写配置(路径, 默认配置.copy())
            return 默认配置.copy()

        try:
            with open(路径, "r", encoding="utf-8") as f:
                配置 = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError):
            print(f"  ⚠ 配置文件损坏，已重置：{路径}")
            写配置(路径, 默认配置.copy())
            return 默认配置.copy()

        # 补齐缺失的键（兼容旧版本配置文件）
        补齐 = 默认配置.copy()
        补齐.update(配置)
        return 补齐


    def 写配置(路径, 配置):
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(配置, f, ensure_ascii=False, indent=2)


    def 改配置(路径, 键, 值):
        """改一个配置项。"""
        配置 = 读配置(路径)
        配置[键] = 值
        写配置(路径, 配置)
        return 配置


    def 合并配置(路径, 新配置):
        """新配置覆盖旧的。"""
        配置 = 读配置(路径)
        配置.update(新配置)
        写配置(路径, 配置)
        return 配置


    —— 测试：

        路径 = "配置.json"

        print(读配置(路径))
        → {'主题': '浅色', '字号': 14, '自动保存': True, '最近打开': []}

        print(改配置(路径, "字号", 18))
        → {'主题': '浅色', '字号': 18, ...}

        print(合并配置(路径, {"主题": "深色", "最近打开": ["a.txt"]}))
        → {'主题': '深色', '字号': 18, '自动保存': True, '最近打开': ['a.txt']}

        print(读配置(路径))
        → 同上（验证持久化成功）

        os.remove(路径)

    —— 几个设计点：

       ① `默认配置.copy()` 每次都复制
          否则返回同一个字典，调用方改了会影响「默认值」。

          （L3 讲的「可变默认值」的同一个坑。）

       ② `补齐` 的逻辑很重要

              补齐 = 默认配置.copy()
              补齐.update(配置)

          这样「配置文件里有的用值，没有的用默认值」。

          用途：程序升级后新增了配置项，旧配置文件不会缺键。

       ③ 捕获 `json.JSONDecodeError`
          文件被手工改坏时的报错。

          捕获 `UnicodeDecodeError`
          编码不对时的报错。

       ④ `改配置` 是「读-改-写」三步
          每次都重写整个文件。

          缺点：配置大了会慢；并发时可能冲突。
          优点：简单，不会出现「文件只写了一半」。

    —— 真实项目的配置管理通常会：
       · 加文件锁（防并发）
       · 加备份（防写坏）
       · 用专门的库（如 `pydantic-settings`）

题 3
    A.  json.dumps({"a": 1})
        → '{"a": 1}'

    B.  json.dumps({"名": "张三"})
        → '{"\\u540d": "\\u5f20\\u4e09"}'
        默认 ensure_ascii=True，中文变成转义序列。

    C.  json.dumps({"名": "张三"}, ensure_ascii=False)
        → '{"名": "张三"}'

    D.  json.loads('{"a": 1}')["a"]
        → 1（整数，不是字符串）

        —— 这和 CSV 不一样：JSON 保留类型。

    E.  json.loads('[1, 2, 3]')
        → [1, 2, 3]（Python 列表）

    F.  json.loads('{"ok": true}')["ok"]
        → True（Python 的布尔值，注意 JSON 里是小写 true）

    G.  json.loads('{"x": null}')["x"]
        → None（JSON 的 null 对应 Python 的 None）

    H.  csv.writer 写 ["a", "b,c"]
        → 文件里是：a,"b,c"

        因为第二个字段有逗号，被引号包起来了。

    I.  json.dumps([1, "a", None])
        → '[1, "a", null]'

    J.  json.loads('{"a": 1,}')
        → json.JSONDecodeError

        **标准 JSON 不允许末尾逗号。**

        （Python 的字典字面量允许 `{"a": 1,}`，但 JSON 不允许。
          这是两者最容易混的地方。）

    —— 汇总：

           A  '{"a": 1}'
           B  '{"\\u540d": "\\u5f20\\u4e09"}'
           C  '{"名": "张三"}'
           D  1
           E  [1, 2, 3]
           F  True
           G  None
           H  a,"b,c"
           I  '[1, "a", null]'
           J  JSONDecodeError

    —— 最容易错的：

       ① J：把 Python 字面量的习惯带到 JSON
          Python 允许末尾逗号，JSON 不允许。

       ② B：忘了 ensure_ascii=False 时中文会变成转义序列
          虽然能正确解析回来，但文件不「人类可读」。

       ③ D 和 CSV 的对比：JSON 保留类型，CSV 全是字符串
          这是选择格式时的重要区别。
'''
