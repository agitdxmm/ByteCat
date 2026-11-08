r'''
════════════════════════════════════════════════════════
  L5 · 第 4 课 · 用法 2        else / finally / raise
════════════════════════════════════════════════════════

try/except 还有三个配套的东西，加上「主动抛异常」。

────────────────────────────────────────────────────────
【else：没出错才执行】
════════════════════════════════════════════════════════

        try:
            数字 = int("42")
        except ValueError:
            print("转换失败")
        else:
            print("转换成功，结果是", 数字)

    ── else 什么时候执行 ──

        try 里**没出任何异常** → 执行 else
        出了异常（被捕获）    → 跳过 else

    ── 为什么不直接写在 try 里 ──

        这样写也能跑：

            try:
                数字 = int("42")
                print("转换成功，结果是", 数字)
            except ValueError:
                print("转换失败")

        区别：**`print` 如果自己出错了，也会被 except 捕获。**

            try:
                数字 = int(输入)
                print(数字 * 2)      ← 如果这里出错，也会说「转换失败」
            except ValueError:
                print("转换失败")

        报错说「转换失败」，其实是 print 里的问题 —— 误导。

        **else 里的代码不会被 except 捕获，语义更精确。**

    ── 什么时候用 ──

        try 里只放「可能出错的」，else 里放「成功之后要做的」。

────────────────────────────────────────────────────────
【finally：无论如何都执行】
════════════════════════════════════════════════════════

        try:
            print("开始")
            x = 1 / 0
        except ZeroDivisionError:
            print("除零了")
        finally:
            print("无论如何都执行")

    输出：

        开始
        除零了
        无论如何都执行

    ── finally 一定会执行 ──

        · try 正常结束 → 执行
        · 出了异常被捕获 → 执行
        · 出了异常没被捕获（要崩溃）→ **也执行**
        · try 里有 return → **也执行**

    ── 最后一个是最反直觉的 ──

        def f():
            try:
                return "try 里的 return"
            finally:
                print("finally 执行了")

        print(f())

        输出：
            finally 执行了
            try 里的 return

        **return 会「等着」，先跑完 finally 再返回。**

    ── finally 用来做什么 ──

        清理资源：

            f = open("data.txt")
            try:
                内容 = f.read()
            finally:
                f.close()          ← 无论如何都关

        这就是 `with` 语句的原理：

            with open(...) as f:
                ...

        等价于 try/finally + close。

        **所以我们平时用 with 就够了，很少手写 finally。**

    ── finally 里不要写 return ──

        def f():
            try:
                return 1
            finally:
                return 2

        print(f())      → 2

        **finally 的 return 会覆盖 try 的 return。**

        这是 bug 的温床，永远不要这么写。

────────────────────────────────────────────────────────
【raise：主动抛异常】
════════════════════════════════════════════════════════

    到目前为止，异常都是「Python 自己抛的」。

    你也可以自己抛：

        raise ValueError("年龄不能是负数")

    ── 什么时候主动抛 ──

        ① 参数不合法

               def 算年龄(出生年):
                   if 出生年 > 2026:
                       raise ValueError(f"出生年不能是未来：{出生年}")
                   return 2026 - 出生年

        ② 数据不满足前提

               def 求平均(列表):
                   if len(列表) == 0:
                       raise ValueError("空列表没有平均值")
                   return sum(列表) / len(列表)

        ③ 功能还没实现

               def 待实现():
                   raise NotImplementedError("这个功能还没写")

    ── raise 和 return 的区别 ──

        `return 错误码`   调用方**可能忘记检查**
        `raise`           调用方**必须处理**，否则崩溃

        **重要的错误用 raise，让问题立刻暴露。**

    ── 重新抛出（在 except 里）──

        try:
            危险操作()
        except Exception as e:
            记日志(e)
            raise          # 记完日志再抛出去

        这样「既记录了，又没吞掉错误」。

    ── 抛出一个具体的异常 ──

        可以复用内置的：

            ValueError      值不对
            TypeError       类型不对
            KeyError        键不存在
            RuntimeError    运行时错误（通用的）

        也可以自定义（下一节）。

────────────────────────────────────────────────────────
【一个完整的例子：带校验的函数】
════════════════════════════════════════════════════════

        def 算BMI(体重公斤, 身高米):
            """算 BMI。参数不合法时抛 ValueError。"""
            if not isinstance(体重公斤, (int, float)):
                raise TypeError(f"体重应该是数字，收到 {type(体重公斤).__name__}")
            if not isinstance(身高米, (int, float)):
                raise TypeError(f"身高应该是数字，收到 {type(身高米).__name__}")
            if 体重公斤 <= 0:
                raise ValueError(f"体重必须大于 0，收到 {体重公斤}")
            if 身高米 <= 0:
                raise ValueError(f"身高必须大于 0，收到 {身高米}")

            return 体重公斤 / (身高米 * 身高米)

    ── 调用方 ──

        try:
            bmi = 算BMI(60, 1.75)
            print(f"BMI = {bmi:.1f}")
        except (TypeError, ValueError) as e:
            print(f"参数有问题：{e}")

    ── 这个设计的好处 ──

        · 函数内部不用 print（保持「纯」）
        · 错误信息带上了「实际收到什么」
        · 调用方决定怎么显示

        **这是「库函数」的标准写法。**

────────────────────────────────────────────────────────
【总结：完整的 try 结构】
════════════════════════════════════════════════════════

        try:
            可能出错的代码
        except 异常类型1 as e:
            处理方式1
        except (异常类型2, 异常类型3):
            处理方式2
        else:
            没出错时执行
        finally:
            无论如何都执行

    ── 有几种写不全也没关系 ──

        最小可用：`try` + 至少一个 `except`
        `else` 和 `finally` 都是可选的

        但顺序固定：except → else → finally
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

print("① else：没出错才执行")
for 输入 in ["42", "abc"]:
    try:
        数字 = int(输入)
    except ValueError:
        print(f"  {输入!r}：转换失败")
    else:
        print(f"  {输入!r}：转换成功，结果是 {数字}")

print("\n② else 的价值：避免误捕")


def 演示():
    try:
        值 = int("42")
        # 如果这里出错，会被下面的 except 误判为「转换失败」
        return 值 * "a" * 0
    except ValueError:
        print("  转换失败（但其实不是转换的问题）")


演示()


def 正确版():
    try:
        值 = int("42")
    except ValueError:
        print("  转换失败")
        return None
    else:
        # 这里的错误不会被 except 捕获
        return 值 * 2


print("  正确版结果：", 正确版())

print("\n③ finally：无论如何都执行")


def 演示finally(除零):
    try:
        print("    try 开始")
        if 除零:
            x = 1 / 0
        print("    try 结束")
    except ZeroDivisionError:
        print("    捕获到除零")
    finally:
        print("    finally 执行")


print("  不除零：")
演示finally(False)
print("  除零：")
演示finally(True)

print("\n④ finally 和 return")
def f1():
    try:
        return "try 的值"
    finally:
        print("  finally 先执行")


print("  返回值：", f1())

print("\n⑤ finally 里的 return 会覆盖")
def f2():
    try:
        return 1
    finally:
        return 2


print("  f2() =", f2(), " ← try 的 return 1 被覆盖了")

print("\n⑥ finally 保证资源释放")


def 手动释放(路径):
    f = None
    try:
        f = open(路径, "r", encoding="utf-8")
        return f.read()
    except FileNotFoundError:
        return None
    finally:
        if f:
            f.close()
            print("  文件已关闭")


import os
测试文件 = "finally测试.txt"
with open(测试文件, "w", encoding="utf-8") as f:
    f.write("内容\n")

print("  读存在的文件：")
print("  内容：", repr(手动释放(测试文件)))
print("  读不存在的文件：")
手动释放("不存在.txt")
os.remove(测试文件)

print("\n  其实用 with 就行：")
print("  with open(...) 内部就是 try/finally + close")

print("\n⑦ raise：主动抛异常")


def 算年龄(出生年):
    if 出生年 > 2026:
        raise ValueError(f"出生年不能是未来：{出生年}")
    if 出生年 < 1900:
        raise ValueError(f"出生年太早了：{出生年}")
    return 2026 - 出生年


for 年 in [2000, 2030, 1800]:
    try:
        print(f"  {年} 年出生，今年 {算年龄(年)} 岁")
    except ValueError as e:
        print(f"  ❌ {e}")

print("\n⑧ 重新抛出")


def 危险操作(x):
    return 100 / x


def 带日志的操作(x):
    try:
        return 危险操作(x)
    except ZeroDivisionError as e:
        print(f"  [日志] 发生错误：{e}")
        raise          # 记完日志再抛出去


try:
    带日志的操作(0)
except ZeroDivisionError:
    print("  调用方也捕获到了（日志已经记过了）")

print("\n⑨ 完整的校验函数")


def 算BMI(体重, 身高):
    """算 BMI，参数不合法时抛异常。"""
    if not isinstance(体重, (int, float)):
        raise TypeError(f"体重应该是数字，收到 {type(体重).__name__}")
    if not isinstance(身高, (int, float)):
        raise TypeError(f"身高应该是数字，收到 {type(身高).__name__}")
    if 体重 <= 0:
        raise ValueError(f"体重必须大于 0，收到 {体重}")
    if 身高 <= 0:
        raise ValueError(f"身高必须大于 0，收到 {身高}")
    return 体重 / (身高 * 身高)


测试 = [(60, 1.75), (60, 0), ("六十", 1.75), (-60, 1.75)]
for 体重, 身高 in 测试:
    try:
        bmi = 算BMI(体重, 身高)
        print(f"  体重 {体重}，身高 {身高} → BMI {bmi:.1f}")
    except (TypeError, ValueError) as e:
        print(f"  体重 {体重}，身高 {身高} → [{type(e).__name__}] {e}")

print("\n⑩ 断言 vs 异常")
print("  assert 条件      → 条件不成立时抛 AssertionError")
print("  raise 异常       → 主动抛出指定异常")
print()
print("  assert 适合「检查我的假设」（开发时）")
print("  raise  适合「检查调用方的输入」（运行时）")
print()
print("  ⚠ python -O 运行时 assert 会被跳过，所以不要用它做参数校验")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  给函数加校验
# ─────────────────────────────────────────
#
# 给下面这些函数加上参数校验（用 raise）：
#
#   A. def 求平均(列表)          空列表抛 ValueError
#   B. def 除法(a, b)            b 为 0 抛 ZeroDivisionError（自己抛）
#   C. def 取第几个(列表, n)      n 越界抛 IndexError（自己抛）
#   D. def 转整数(s)             转不了抛 ValueError（带原始输入）
#
# 要求：
#   · 每个函数都要有清晰的错误信息
#   · 调用方用 try/except 测试，验证错误信息是否正确
#   · 说明：什么时候该让函数抛异常，什么时候该返回 None
#
# 你的代码：


# ═════════════════════════════════════════
#  题 2  ──  else 和 finally 的行为
# ═════════════════════════════════════════
#
# 写出下面每个函数打印什么（按顺序）：
#
#   A.
#       def f():
#           try:
#               print("1")
#               return "A"
#           finally:
#               print("2")
#       print(f())
#
#   B.
#       def g():
#           try:
#               print("1")
#               x = 1 / 0
#           except ZeroDivisionError:
#               print("2")
#               return "B"
#           finally:
#               print("3")
#       print(g())
#
#   C.
#       def h():
#           try:
#               print("1")
#           except ValueError:
#               print("2")
#           else:
#               print("3")
#           finally:
#               print("4")
#       h()
#
#   D.
#       def k():
#           try:
#               print("1")
#               x = 1 / 0
#           except ValueError:
#               print("2")
#           finally:
#               print("3")
#       try:
#           k()
#       except ZeroDivisionError:
#           print("4")
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 求平均(列表):
        """返回平均值。空列表抛 ValueError。"""
        if len(列表) == 0:
            raise ValueError("空列表没有平均值")
        return sum(列表) / len(列表)


    def 除法(a, b):
        """返回 a / b。b 为 0 时抛 ZeroDivisionError。"""
        if b == 0:
            raise ZeroDivisionError(f"除数不能为 0（被除数是 {a}）")
        return a / b


    def 取第几个(列表, n):
        """返回第 n 个（从 0 开始）。越界抛 IndexError。"""
        if n < 0 or n >= len(列表):
            raise IndexError(
                f"索引 {n} 超出范围（列表长度 {len(列表)}）")
        return 列表[n]


    def 转整数(s):
        """转成整数。失败时抛 ValueError。"""
        try:
            return int(s)
        except (ValueError, TypeError):
            raise ValueError(f"无法把「{s}」转成整数") from None


    —— 测试：

        try:
            求平均([])
        except ValueError as e:
            print("A:", e)          → A: 空列表没有平均值

        try:
            除法(10, 0)
        except ZeroDivisionError as e:
            print("B:", e)          → B: 除数不能为 0（被除数是 10）

        try:
            取第几个([1, 2, 3], 5)
        except IndexError as e:
            print("C:", e)          → C: 索引 5 超出范围（列表长度 3）

        try:
            转整数("abc")
        except ValueError as e:
            print("D:", e)          → D: 无法把「abc」转成整数

    —— 几个关键点：

       ① `raise ... from None` 的用处
          原来 `int("abc")` 会抛一个 ValueError，
          我们在 except 里又抛一个新的。

          Python 会显示「处理这个异常时又发生了另一个异常」，
          `from None` 表示「不用显示原始的那个」。

          这样错误信息更干净。

       ② `取第几个` 自己抛 IndexError
          其实 `列表[n]` 本来就会抛 IndexError，
          但错误信息是 `list index out of range`，不告诉你「长度多少」。

          自己抛能带上更多信息。

          —— 但这也意味着多做了一次判断。
             性能敏感的地方直接用 `列表[n]` 更好。

       ③ `除法` 抛 ZeroDivisionError
          Python 自己也会抛，但我们的信息更详细。

    —— 「什么时候抛异常，什么时候返回 None」：

       **抛异常**：
           · 这是「错误」，不是「正常情况」
           · 调用方必须知道，否则会出错
           · 比如：参数不合法、前提不满足

       **返回 None**：
           · 这是「正常但没有结果」
           · 调用方通常会检查
           · 比如：查找没找到、可选操作用户跳过

       例子对比：

           求平均([])           → 抛异常（空列表求平均是错误用法）
           查字典.get("不存在的") → 返回 None（查不到是正常的）

       一句判断：
       **「这是程序员的错，还是数据的常态？」**
           程序员的错 → 抛异常（让他知道）
           数据的常态 → 返回 None（让调用方处理）

题 2
    A.
        def f():
            try:
                print("1")
                return "A"
            finally:
                print("2")
        print(f())

        输出：
            1
            2
            A

        分析：print("1") 先执行，然后遇到 return，
        但 return 要等 finally 跑完，所以先 print("2")，再返回 "A"。

    B.
        def g():
            try:
                print("1")
                x = 1 / 0
            except ZeroDivisionError:
                print("2")
                return "B"
            finally:
                print("3")
        print(g())

        输出：
            1
            2
            3
            B

        分析：1 → 除零 → 捕获，2 → return "B"（等 finally）→ 3 → 返回。

    C.
        def h():
            try:
                print("1")
            except ValueError:
                print("2")
            else:
                print("3")
            finally:
                print("4")
        h()

        输出：
            1
            3
            4

        分析：try 没出错 → 跳过 except → 执行 else（3）→ finally（4）。

    D.
        def k():
            try:
                print("1")
                x = 1 / 0
            except ValueError:
                print("2")
            finally:
                print("3")
        try:
            k()
        except ZeroDivisionError:
            print("4")

        输出：
            1
            3
            4

        分析：
            print("1")
            除零 → 找 except，但 ValueError 不匹配 → 异常「悬着」
            执行 finally（3）
            finally 结束后，异常继续往外抛
            外层 try 捕获 ZeroDivisionError → print("4")

        ⚠ 注意「2」没打印，因为 except 类型不匹配。

    —— 汇总：

           A  1 2 A
           B  1 2 3 B
           C  1 3 4
           D  1 3 4

    —— 最容易错的：

       ① A：以为 return 立刻返回值
          实际「finally 优先」，return 要排队。

       ② D：以为 except 不匹配就不执行 finally
          实际 finally 一定会执行，然后异常继续往上抛。

          **finally 的执行和「有没有异常」「异常有没有被捕获」都无关。**
'''
