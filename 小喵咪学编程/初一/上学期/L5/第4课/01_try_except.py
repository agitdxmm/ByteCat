r'''
════════════════════════════════════════════════════════
  L5 · 第 4 课 · 用法 1        try / except
════════════════════════════════════════════════════════

前四级写代码时，遇到错误就让它报错停下。

真实的程序不能这样 —— 用户输错一个字符就崩溃，没法用。

这一节讲：**怎么让程序「出错也不死」。**

────────────────────────────────────────────────────────
【先看没有异常处理的后果】
════════════════════════════════════════════════════════

        数字 = int(input("输入一个数："))
        结果 = 100 / 数字
        print("结果是", 结果)

    如果用户输入 "abc"：

        ValueError: invalid literal for int() with base 10: 'abc'
        程序直接退出。

    如果用户输入 "0"：

        ZeroDivisionError: division by zero
        程序直接退出。

    ── 用户不知道发生了什么 ──

        屏幕上只有一堆红字，程序就没了。

        他只会觉得「这软件坏了」。

────────────────────────────────────────────────────────
【try / except 的形状】
════════════════════════════════════════════════════════

        try:
            可能出错的代码
        except 某个异常:
            出错时怎么办

    ── 例子 ──

        try:
            数字 = int("abc")
        except ValueError:
            print("这不是一个数字")

    ── 执行流程 ──

        ① 先执行 try 里的代码
        ② 如果没出错 → 跳过 except，继续往下
        ③ 如果出错 → 检查异常类型是不是 except 里写的
           匹配 → 执行 except 块，然后继续往下
           不匹配 → 程序崩溃（和没写一样）

    ── 关键：try 里出错的那一行之后的代码不执行 ──

        try:
            print("第一步")
            数字 = int("abc")      ← 这里出错
            print("第二步")        ← 不执行
        except ValueError:
            print("出错了")

        输出：第一步 / 出错了

    **「第二步」被跳过了。**

────────────────────────────────────────────────────────
【捕获特定异常】
════════════════════════════════════════════════════════

    ── 只捕获你预期的那种 ──

        try:
            f = open("data.txt")
            内容 = f.read()
            f.close()
        except FileNotFoundError:
            print("文件不存在")

    ── 为什么「只捕特定的」──

        因为如果捕获了所有异常，真正的 bug 会被藏起来：

            try:
                结果 = 复杂计算()
            except:
                print("出错了")

        「出错了」这三个字什么信息都没有。

        是除零？是类型错？是拼写错？
        你根本不知道，而且程序还在继续跑，
        带着错误的状态往下走 —— 可能造成更严重的问题。

    **宁可崩溃，也不要「假装没事」。**

    ── 忘记关文件的问题 ──

        上面那个例子里，如果 `f.read()` 出错，
        `f.close()` 就不会执行。

        所以文件操作要用 `with`：

            try:
                with open("data.txt", encoding="utf-8") as f:
                    内容 = f.read()
            except FileNotFoundError:
                print("文件不存在")

        `with` 保证出错也会关闭。

────────────────────────────────────────────────────────
【多个 except】
════════════════════════════════════════════════════════

        try:
            数字 = int(输入)
            结果 = 100 / 数字
        except ValueError:
            print("输入的不是数字")
        except ZeroDivisionError:
            print("不能除以 0")

    ── 按顺序匹配，命中就停 ──

        和 if/elif 一样，第一个匹配的 except 执行完就跳过其余。

        **所以「更具体的异常」要写在前面。**

    ── 一个 except 处理多种异常 ──

        except (ValueError, TypeError):
            print("输入有问题")

        用元组把多个类型括起来。

    ── 异常类型有继承关系 ──

        `FileNotFoundError` 是 `OSError` 的子类。

        所以：

            except OSError:         会捕获 FileNotFoundError
            except FileNotFoundError:  只捕获具体的那个

        顺序很重要：

            ✅ except FileNotFoundError: ...   先具体
               except OSError: ...

            ❌ except OSError: ...             先笼统
               except FileNotFoundError: ...  永远执行不到

────────────────────────────────────────────────────────
【拿到错误信息：as e】
════════════════════════════════════════════════════════

        try:
            int("abc")
        except ValueError as e:
            print("错误信息：", e)

    ── 输出 ──

        错误信息： invalid literal for int() with base 10: 'abc'

    ── e 是什么 ──

        一个异常对象。常用的：

            str(e)          错误描述
            type(e).__name__  异常类型名

        例：

            except Exception as e:
                print(f"[{type(e).__name__}] {e}")

            → [ValueError] invalid literal for int()...

    ── 这个信息很有用 ──

        写日志时记录它，方便事后排查：

            except Exception as e:
                with open("error.log", "a", encoding="utf-8") as f:
                    f.write(f"{时间} [{type(e).__name__}] {e}\n")

────────────────────────────────────────────────────────
【常见异常类型速查】
════════════════════════════════════════════════════════

    ┌──────────────────────┬────────────────────────────┐
    │ ValueError           │ 类型对，值不对             │
    │                      │ int("abc")                 │
    ├──────────────────────┼────────────────────────────┤
    │ TypeError            │ 类型不对                   │
    │                      │ "a" + 1                    │
    ├──────────────────────┼────────────────────────────┤
    │ ZeroDivisionError    │ 除以 0                     │
    ├──────────────────────┼────────────────────────────┤
    │ IndexError           │ 列表下标越界               │
    ├──────────────────────┼────────────────────────────┤
    │ KeyError             │ 字典键不存在               │
    ├──────────────────────┼────────────────────────────┤
    │ FileNotFoundError    │ 文件不存在                 │
    ├──────────────────────┼────────────────────────────┤
    │ PermissionError      │ 没权限                     │
    ├──────────────────────┼────────────────────────────┤
    │ AttributeError       │ 对象没这个属性/方法        │
    ├──────────────────────┼────────────────────────────┤
    │ NameError            │ 名字没定义                 │
    ├──────────────────────┼────────────────────────────┤
    │ RecursionError       │ 递归太深                   │
    └──────────────────────┴────────────────────────────┘

    ── 注意 ValueError 和 TypeError 的区别 ──

        `int("abc")`     ValueError（"abc" 是字符串，类型没错，但内容转不了）
        `int(None)`      TypeError（None 不是能转的类型）

        **「类型错」是 TypeError，「值错」是 ValueError。**

────────────────────────────────────────────────────────
【什么时候该用 try/except】
════════════════════════════════════════════════════════

    ── 适合 ──

        ① 处理外部输入（用户输入、文件、网络）
           你无法控制它是否合法

        ② 处理「可能失败但不致命」的操作
           读配置文件失败 → 用默认配置

        ③ 把底层异常翻译成你能处理的
           库抛了复杂异常，你转成自己的

    ── 不适合 ──

        ❌ 用来掩盖 bug

               try:
                   结果 = 我的函数()
               except:
                   pass

           这样程序「看起来正常」，但结果是错的。

        ❌ 用来做正常流程控制

               try:
                  值 = 列表[5]
               except IndexError:
                  值 = 默认值

           应该先判断 `if len(列表) > 5`。

        ❌ 包住一大段代码

               try:
                   # 100 行
               except Exception:
                   ...

           出错时你根本不知道是哪一行。

        **try 的范围越小越好。**

    ── 一个判断标准 ──

        「这个异常我能做什么？」

            能做出有意义的补救 → 用 try
            只能打印「出错了」→ 让它崩，崩了才知道要修什么
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① 没有异常处理会怎样")
print("  如果写 `int('abc')`，程序会直接崩溃：")
print("    ValueError: invalid literal for int() with base 10: 'abc'")

print("\n② 用 try/except 接住")
try:
    数字 = int("abc")
except ValueError:
    print("  这不是一个数字")

print("  程序继续往下跑了 ✓")

print("\n③ try 里出错之后的代码不执行")
try:
    print("  第一步")
    数字 = int("abc")
    print("  第二步（不会执行）")
except ValueError:
    print("  出错了")

print("\n④ 只捕获特定的异常")
try:
    结果 = 10 / 0
except ValueError:
    print("  这里不会执行，因为异常类型不匹配")
except ZeroDivisionError:
    print("  捕获到 ZeroDivisionError")

print("\n⑤ 多个 except 按顺序匹配")
测试 = ["abc", "0", "5"]


def 算一百除以(s):
    try:
        数 = int(s)
        return 100 / 数
    except ValueError:
        return "不是数字"
    except ZeroDivisionError:
        return "不能除以 0"


for s in 测试:
    print(f"  100 / {s!r:<6} → {算一百除以(s)}")

print("\n⑥ 一个 except 处理多种异常")
for 值 in ["abc", None]:
    try:
        结果 = int(值)
        print("  ", 结果)
    except (ValueError, TypeError) as e:
        print(f"  输入 {值!r} 出错了：[{type(e).__name__}] {e}")

print("\n⑦ 拿到错误信息")
try:
    int("hello")
except ValueError as e:
    print("  错误原文：", e)
    print("  异常类型：", type(e).__name__)

print("\n⑧ 捕获异常后继续执行")


def 安全转数字(s, 默认=0):
    """转不了就返回默认值。"""
    try:
        return int(s)
    except (ValueError, TypeError):
        return 默认


测试数据 = ["123", "abc", "", None, " 42 ", "3.14"]
for 值 in 测试数据:
    print(f"  安全转数字({值!r}) = {安全转数字(值)}")

print("\n⑨ 文件操作的异常处理")
import os


def 安全读文件(路径):
    """读文件，失败时返回 None。"""
    try:
        with open(路径, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  文件不存在：{路径}")
        return None
    except PermissionError:
        print(f"  没有权限：{路径}")
        return None
    except UnicodeDecodeError:
        print(f"  编码不对：{路径}")
        return None


print("  读一个不存在的文件：")
安全读文件("不存在.txt")

print("  读一个目录：")
安全读文件(".")

print("\n⑩ 列表和字典的异常")


def 安全取列表(列表, 索引, 默认=None):
    try:
        return 列表[索引]
    except IndexError:
        return 默认


def 安全取字典(字典, 键, 默认=None):
    try:
        return 字典[键]
    except KeyError:
        return 默认


数据 = [10, 20, 30]
字典 = {"a": 1}

print("  安全取列表([10,20,30], 1) =", 安全取列表(数据, 1))
print("  安全取列表([10,20,30], 9) =", 安全取列表(数据, 9))
print("  安全取字典({'a':1}, 'a')  =", 安全取字典(字典, "a"))
print("  安全取字典({'a':1}, 'z')  =", 安全取字典(字典, "z"))

print("  （其实有更简单的：列表用 len 判断，字典用 .get()）")
print("  列表：", 数据[1] if len(数据) > 1 else None)
print("  字典：", 字典.get("z"))

print("\n⑪ 异常顺序的重要性")
print("  FileNotFoundError 是 OSError 的子类")
print()

try:
    open("不存在.txt")
except FileNotFoundError:
    print("  ✅ 先捕具体的 FileNotFoundError")
except OSError:
    print("  不会走到这里")

try:
    open("不存在.txt")
except OSError:
    print("  ⚠ 先捕笼统的 OSError —— 也能捕获，但丢失了具体信息")
except FileNotFoundError:
    print("  永远不会执行")

print("\n⑫ 一段完整的健壮代码")


def 读数字文件(路径):
    """读一个每行一个数字的文件，返回数字列表。"""
    结果 = []
    try:
        with open(路径, "r", encoding="utf-8") as f:
            for i, 行 in enumerate(f, 1):
                行 = 行.strip()
                if not 行:
                    continue
                try:
                    结果.append(int(行))
                except ValueError:
                    print(f"  ⚠ 第 {i} 行不是数字，跳过：{行!r}")
    except FileNotFoundError:
        print(f"  ⚠ 文件不存在：{路径}")
    return 结果


测试文件 = "数字测试.txt"
with open(测试文件, "w", encoding="utf-8") as f:
    f.write("10\n20\nabc\n30\n\n40\n")

数字们 = 读数字文件(测试文件)
print("  读到的数字：", 数字们)
print("  总和：", sum(数字们))

os.remove(测试文件)
print("\n  读不存在的文件：")
print("  ", 读数字文件("根本没有.txt"))


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  安全的输入函数
# ─────────────────────────────────────────
#
# 写这几个函数，都不许让程序崩溃：
#
#   A. def 读整数(提示, 默认=None)
#        一直问，直到用户输入合法整数；输入空行返回默认值
#        （测试时用参数传入输入内容，不用真的 input）
#
#   B. def 读浮点(提示, 默认=0.0)
#
#   C. def 读选择(提示, 选项)
#        只接受 选项 列表里的值，其他重新问
#
#   D. def 读范围(提示, 最小, 最大)
#        只接受范围内的数
#
# 要求：
#   · 用 try/except 处理转换失败
#   · 参数里带一个「模拟输入列表」，方便测试
#   · 测试各种非法输入
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  异常类型判断
# ─────────────────────────────────────────
#
# 下面 10 个表达式，分别会抛什么异常？
# （跑一下验证，但先自己判断）
#
#   A.  int("abc")
#   B.  int(None)
#   C.  10 / 0
#   D.  [1, 2][5]
#   E.  {"a": 1}["b"]
#   F.  "abc" + 1
#   G.  open("不存在的文件.txt")
#   H.  1 + "2"
#   I.  int("3.14")
#   J.  "abc"[10]
#
# 你的答案：


# ─────────────────────────────────────────
#  题 3  ──  预测输出
# ═════════════════════════════════════════
#
#   A.
#       try:
#           print("A")
#           x = 1 / 0
#           print("B")
#       except ZeroDivisionError:
#           print("C")
#       print("D")
#
#   B.
#       try:
#           x = int("abc")
#       except ValueError:
#           print("V")
#       except ZeroDivisionError:
#           print("Z")
#
#   C.
#       try:
#           print("try")
#       except ValueError:
#           print("except")
#       print("after")
#
#   D.
#       try:
#           raise ValueError("自己抛的")
#       except ValueError as e:
#           print("捕获：", e)
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 读整数(提示, 默认=None, 模拟输入=None):
        """读整数。模拟输入是一个列表，用来测试。"""
        输入源 = 模拟输入 if 模拟输入 is not None else None
        次数 = 0

        while True:
            if 输入源 is not None:
                if 次数 >= len(输入源):
                    print("  （模拟输入用完了）")
                    return 默认
                原始 = 输入源[次数]
                次数 += 1
                print(f"  {提示}{原始}")
            else:
                原始 = input(提示)

            原始 = 原始.strip()

            if 原始 == "":
                return 默认

            try:
                return int(原始)
            except ValueError:
                print(f"     ⚠ 「{原始}」不是整数，请重新输入")


    测试：

        print(读整数("请输入：", 模拟输入=["abc", "3.5", "42"]))
        → 提示三次，最后返回 42

        print(读整数("请输入：", 默认=0, 模拟输入=["", "xx"]))
        → 第一次空行就返回 0

    —— 几个点：

       ① `try: return int(原始)` —— return 在 try 里
          转换成功就直接返回了，不会走 except。

       ② 循环 + try 的组合
          「一直问到合法为止」，这是交互程序的标准写法。

       ③ `模拟输入` 参数
          真实程序用 `input()`，测试用列表。
          这样既能真的运行，又能自动测试。

          —— 这个技巧叫「依赖注入」的简化版。

       ④ `原始.strip()` 处理 " 42 " 这种

       ⑤ 空行返回默认值
          让用户「直接回车跳过」。

    —— 完整的其他三个：

        def 读浮点(提示, 默认=0.0, 模拟输入=None):
            次数 = 0
            while True:
                if 模拟输入 is not None:
                    if 次数 >= len(模拟输入):
                        return 默认
                    原始 = 模拟输入[次数]
                    次数 += 1
                    print(f"  {提示}{原始}")
                else:
                    原始 = input(提示)

                原始 = 原始.strip()
                if 原始 == "":
                    return 默认
                try:
                    return float(原始)
                except ValueError:
                    print(f"     ⚠ 「{原始}」不是小数")


        def 读选择(提示, 选项, 模拟输入=None):
            次数 = 0
            while True:
                if 模拟输入 is not None:
                    if 次数 >= len(模拟输入):
                        return 选项[0]
                    原始 = 模拟输入[次数]
                    次数 += 1
                    print(f"  {提示}（{'/'.join(选项)}）{原始}")
                else:
                    原始 = input(f"{提示}（{'/'.join(选项)}）")

                原始 = 原始.strip().lower()
                for 项 in 选项:
                    if 项.lower() == 原始:
                        return 项

                print(f"     ⚠ 只能选：{'/'.join(选项)}")


        def 读范围(提示, 最小, 最大, 模拟输入=None):
            次数 = 0
            while True:
                if 模拟输入 is not None:
                    if 次数 >= len(模拟输入):
                        return 最小
                    原始 = 模拟输入[次数]
                    次数 += 1
                    print(f"  {提示}{原始}")
                else:
                    原始 = input(提示)

                try:
                    值 = int(原始.strip())
                except ValueError:
                    print("     ⚠ 请输入整数")
                    continue

                if 最小 <= 值 <= 最大:
                    return 值
                print(f"     ⚠ 请输入 {最小} 到 {最大} 之间的数")

    —— 一个设计上的观察：

       四个函数有 80% 的代码是一样的（循环、取输入、strip、判断空）。

       可以抽一个「通用读入器」：

           def 读(提示, 校验函数, 默认, 模拟输入):
               while True:
                   原始 = 取输入()
                   try:
                       值 = 校验函数(原始)
                       return 值
                   except ValueError as e:
                       print(f"⚠ {e}")

       然后每个具体函数只写「校验函数」。

       —— 这就是 L3 讲的「函数作为参数」的实际应用。

       但对初学者来说，重复写几遍更容易看懂。
       熟练之后再重构。

题 2
    A.  int("abc")      → ValueError
        类型对（字符串），内容不是数字。

    B.  int(None)       → TypeError
        None 不是能转成整数的类型。

    C.  10 / 0          → ZeroDivisionError

    D.  [1, 2][5]       → IndexError

    E.  {"a": 1}["b"]   → KeyError

    F.  "abc" + 1       → TypeError
        字符串不能加数字。

    G.  open("不存在.txt")  → FileNotFoundError

    H.  1 + "2"         → TypeError

    I.  int("3.14")     → ValueError
        字符串带小数点，不能直接转整数。

        （要先 float("3.14") 再 int()，或者用 int(float(...))）

    J.  "abc"[10]       → IndexError
        字符串索引越界。

    —— 汇总：

           A  ValueError
           B  TypeError
           C  ZeroDivisionError
           D  IndexError
           E  KeyError
           F  TypeError
           G  FileNotFoundError
           H  TypeError
           I  ValueError
           J  IndexError

    —— 最容易混的：A、B、I

        A `int("abc")`  → ValueError（是字符串，类型没错）
        B `int(None)`   → TypeError（None 不是数字类型）
        I `int("3.14")` → ValueError（是字符串，但内容转不了）

        **记法：「类型对不对」看 TypeError，
                「值能不能用」看 ValueError。**

    —— F 和 H 都是 TypeError，但方向不同：
        F 是「字符串 + 数字」
        H 是「数字 + 字符串」

        结果一样报错，因为两种操作都不支持。

题 3
    A.
        try:
            print("A")
            x = 1 / 0
            print("B")
        except ZeroDivisionError:
            print("C")
        print("D")

        输出：
            A
            C
            D

        分析：
            print("A") 正常
            1/0 出错，print("B") 跳过
            捕获，print("C")
            try 块结束，继续 print("D")

    B.
        try:
            x = int("abc")
        except ValueError:
            print("V")
        except ZeroDivisionError:
            print("Z")

        输出：V

        int("abc") 抛 ValueError，第一个 except 匹配。

    C.
        try:
            print("try")
        except ValueError:
            print("except")
        print("after")

        输出：
            try
            after

        try 里没出错，except 不执行。

    D.
        try:
            raise ValueError("自己抛的")
        except ValueError as e:
            print("捕获：", e)

        输出：捕获： 自己抛的

        `raise` 是「主动抛出异常」（下一节讲）。

    —— 汇总：

           A  A / C / D
           B  V
           C  try / after
           D  捕获： 自己抛的

    —— 最容易错的：

       ① A：以为出错之后 try 里剩下的都执行
          实际是「出错那一行之后，try 块内全部跳过」。

       ② C：以为 try 没出错就不会继续往下
          实际是「没出错就跳过 except，正常往下走」。

       ③ B：以为两个 except 都会执行
          实际只有第一个匹配的执行。
'''
