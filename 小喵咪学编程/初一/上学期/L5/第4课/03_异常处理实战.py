r'''
════════════════════════════════════════════════════════
  L5 · 第 4 课 · 用法 3        异常处理实战
════════════════════════════════════════════════════════

语法学会了，这一节讲「什么时候该怎么用」。

真实程序里的异常处理，主要是这四种模式。

────────────────────────────────────────────────────────
【模式一：重试】
════════════════════════════════════════════════════════

    有些操作「失败一次不代表永远失败」：网络请求、文件锁、临时冲突。

    ── 简单重试 ──

        def 重试(操作, 次数=3):
            """尝试最多 次数 次，全失败则抛出最后的异常。"""
            最后错误 = None
            for i in range(次数):
                try:
                    return 操作()
                except Exception as e:
                    最后错误 = e
                    print(f"  第 {i + 1} 次失败：{e}")
            raise 最后错误

    ── 带退避的重试（更真实）──

        失败之后等一会儿再试，而且越等越久：

            import time

            def 重试_退避(操作, 次数=3):
                等待 = 0.1
                for i in range(次数):
                    try:
                        return 操作()
                    except Exception as e:
                        if i == 次数 - 1:
                            raise
                        print(f"  {等待:.1f} 秒后重试")
                        time.sleep(等待)
                        等待 *= 2

        （真实项目里，网络请求的重试间隔通常是 1s、2s、4s……）

    ── 什么时候不该重试 ──

        ❌ 参数错误（ValueError）—— 重试一百次也一样错
        ❌ 文件不存在（FileNotFoundError）—— 不会自己冒出来
        ❌ 权限不够（PermissionError）—— 不会自己变有

        **只对「可能是暂时性的错误」重试。**

        所以重试的 except 应该捕获**具体的**异常，不是 `Exception`：

            except (ConnectionError, TimeoutError):
                重试

────────────────────────────────────────────────────────
【模式二：降级】
════════════════════════════════════════════════════════

    「主要方案失败了，用备选方案」。

    ── 例子：读配置 ──

        def 读配置():
            try:
                with open("config.json", encoding="utf-8") as f:
                    return json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                print("  配置文件有问题，使用默认配置")
                return 默认配置

    ── 例子：多个数据源 ──

        def 取数据():
            try:
                return 从网络取()
            except Exception:
                print("  网络失败，改用本地缓存")
                try:
                    return 从缓存取()
                except Exception:
                    print("  缓存也没有，用空数据")
                    return {}

    ── 降级的核心 ──

        **「失败也要给调用方一个能用的结果」，而不是崩溃。**

    ── 但要小心 ──

        降级会掩盖问题。

        如果配置文件一直是坏的，程序一直用默认值，
        用户可能永远不知道自己的配置没生效。

        **降级时要「让用户知道」。**

            ① 打印警告
            ② 记录日志
            ③ 在界面上显示「当前使用默认配置」

────────────────────────────────────────────────────────
【模式三：部分失败】
════════════════════════════════════════════════════════

    批量处理时，一条失败不该让整批都停。

    ── 错误示范 ──

        def 处理全部(数据们):
            结果 = []
            for 条 in 数据们:
                结果.append(处理(条))      ← 一条报错，整个函数崩
            return 结果

    ── 正确做法：记录失败，继续处理 ──

        def 处理全部(数据们):
            成功 = []
            失败 = []

            for i, 条 in enumerate(数据们):
                try:
                    成功.append(处理(条))
                except Exception as e:
                    失败.append({
                        "序号": i,
                        "数据": 条,
                        "错误": f"[{type(e).__name__}] {e}",
                    })

            return 成功, 失败

    ── 调用方 ──

        成功, 失败 = 处理全部(数据)
        print(f"成功 {len(成功)} 条，失败 {len(失败)} 条")
        for 项 in 失败:
            print(f"  第 {项['序号']} 条失败：{项['错误']}")

    ── 这个模式的重要性 ──

        处理 1000 条数据，第 3 条有问题：

            ❌ 全部停 → 剩 997 条没处理
            ✅ 记录失败 → 处理了 999 条，告诉你哪条有问题

        **「尽量做完，然后报告问题」比「一有问题就全停」有用得多。**

    ── 一个注意点 ──

        `except Exception` 在这里是合理的 ——
        因为你要「任何错误都不能中断整批」。

        但要用 `type(e).__name__` 记录具体类型，
        否则事后不知道是什么错。

────────────────────────────────────────────────────────
【模式四：把错误转成更清楚的说法】
════════════════════════════════════════════════════════

    底层库抛的异常往往很技术化，用户看不懂。

    ── 例子 ──

        try:
            with open("数据.csv", encoding="utf-8") as f:
                数据 = list(csv.reader(f))
        except FileNotFoundError:
            raise RuntimeError("数据文件不见了，请确认它还在原来的位置") from None
        except UnicodeDecodeError:
            raise RuntimeError("数据文件编码不对，请用 UTF-8 保存") from None

    ── 好处 ──

        · 用户看得懂
        · 带上了「怎么办」

    ── 但不要丢掉原始信息 ──

        ❌ 只写「出错了」，不说是哪个错
        ✅ 用 `from e` 保留原始异常（Python 会显示两者）

            except FileNotFoundError as e:
                raise RuntimeError("数据文件不见了") from e

        这样 traceback 里既有你的话，也有原始的错。

────────────────────────────────────────────────────────
【四种模式速查】
════════════════════════════════════════════════════════

    ┌──────────┬────────────────────────────────────┐
    │ 重试     │ 暂时性错误，等一会儿可能就好了      │
    │ 降级     │ 有备选方案，失败也要能用            │
    │ 部分失败 │ 批量处理，一条失败不影响其他        │
    │ 转译     │ 把技术错误变成用户能懂的话          │
    └──────────┴────────────────────────────────────┘

────────────────────────────────────────────────────────
【反模式：不要这么写】
════════════════════════════════════════════════════════

    ❌ 一：吞掉所有异常

        try:
            ...
        except:
            pass

        程序「正常」跑完，但结果是错的，而且你完全不知道。

    ❌ 二：捕获了不做处理

        try:
            ...
        except Exception:
            print("出错了")

        至少打印一下异常内容：`print("出错了", e)`。

    ❌ 三：用异常控制流程

        try:
            值 = 字典[键]
        except KeyError:
            值 = None

        应该是：`值 = 字典.get(键)`。

    ❌ 四：try 包太大

        try:
            # 200 行代码
        except Exception as e:
            print(e)

        出错时你不知道是哪一行。

    ❌ 五：捕获后不重新抛

        def 关键操作():
            try:
                真正的工作()
            except Exception:
                print("失败了")
                # 然后呢？调用方以为成功了！

        如果调用方需要知道失败，必须 `raise`。
'''

# ═══════════════════════════════════════
#  示例
# ═══════════════════════════════════════

import time
import json
import os

print("① 模式一：重试")
尝试次数 = [0]


def 会失败三次():
    尝试次数[0] += 1
    if 尝试次数[0] < 3:
        raise ConnectionError(f"网络超时（第 {尝试次数[0]} 次）")
    return "成功拿到数据"


def 重试(操作, 次数=5):
    最后错误 = None
    for i in range(次数):
        try:
            return 操作()
        except (ConnectionError, TimeoutError) as e:
            最后错误 = e
            print(f"  第 {i + 1} 次失败：{e}")
    raise 最后错误


try:
    结果 = 重试(会失败三次)
    print("  最终结果：", 结果)
except ConnectionError as e:
    print("  彻底失败：", e)

print("\n② 重试不该用于「参数错误」")


def 转换(s):
    return int(s)


try:
    重试(lambda: 转换("abc"), 次数=3)
except ValueError as e:
    print(f"  参数错误直接抛出来：{e}")
    print("  （重试了 3 次，但每次都是同样的错，白费）")

print("\n③ 模式二：降级")
默认配置 = {"主题": "浅色", "字号": 14}


def 读配置(路径):
    try:
        with open(路径, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"  ⚠ 配置文件不存在，使用默认配置")
        return 默认配置
    except json.JSONDecodeError as e:
        print(f"  ⚠ 配置文件格式错误（{e}），使用默认配置")
        return 默认配置


print("  读不存在的配置：")
print("  ", 读配置("没有这个配置.json"))

坏配置 = "坏配置.json"
with open(坏配置, "w", encoding="utf-8") as f:
    f.write("{不是合法JSON")
print("  读坏掉的配置：")
print("  ", 读配置(坏配置))

好配置 = "好配置.json"
with open(好配置, "w", encoding="utf-8") as f:
    json.dump({"主题": "深色", "字号": 18}, f, ensure_ascii=False)
print("  读正常的配置：")
print("  ", 读配置(好配置))

os.remove(坏配置)
os.remove(好配置)

print("\n④ 模式三：部分失败")


def 处理一条(数据):
    if 数据 < 0:
        raise ValueError(f"不能处理负数：{数据}")
    if 数据 == 0:
        raise ZeroDivisionError("不能处理 0")
    return 100 / 数据


def 处理全部(数据们):
    成功 = []
    失败 = []
    for i, 条 in enumerate(数据们):
        try:
            成功.append((条, 处理一条(条)))
        except Exception as e:
            失败.append({
                "序号": i,
                "数据": 条,
                "错误": f"[{type(e).__name__}] {e}",
            })
    return 成功, 失败


数据 = [10, 20, -5, 0, 50, -1, 100]
成功, 失败 = 处理全部(数据)

print(f"  总数 {len(数据)}，成功 {len(成功)}，失败 {len(失败)}")
print("  成功的：")
for 原始, 结果 in 成功:
    print(f"    {原始} → {结果}")
print("  失败的：")
for 项 in 失败:
    print(f"    第 {项['序号']} 条（{项['数据']}）：{项['错误']}")

print("\n⑤ 对比：不隔离错误会怎样")


def 处理全部_不隔离(数据们):
    结果 = []
    for 条 in 数据们:
        结果.append(处理一条(条))
    return 结果


try:
    处理全部_不隔离(数据)
except Exception as e:
    print(f"  ❌ 第一条错误就中断了：{e}")
    print("     后面的数据一条都没处理")

print("\n⑥ 模式四：转译错误")


def 读数据文件(路径):
    try:
        with open(路径, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"数据文件找不到：{路径}，请确认它还在") from e
    except UnicodeDecodeError as e:
        raise RuntimeError(f"文件编码不是 UTF-8：{路径}") from e


try:
    读数据文件("不存在的.csv")
except RuntimeError as e:
    print("  用户看到的：", e)
    print("  （原始异常被 from e 保留，调试时能看到根因）")

print("\n⑦ 带退避的重试")


def 重试_退避(操作, 次数=3, 初始等待=0.05):
    等待 = 初始等待
    for i in range(次数):
        try:
            return 操作()
        except ConnectionError as e:
            if i == 次数 - 1:
                raise
            print(f"    失败，{等待:.2f} 秒后重试")
            time.sleep(等待)
            等待 *= 2


计数 = [0]


def 第二次成功():
    计数[0] += 1
    if 计数[0] < 2:
        raise ConnectionError("模拟失败")
    return "成功"


print("  开始重试：")
print("  结果：", 重试_退避(第二次成功))

print("\n⑧ 反模式演示：吞掉异常")


def 吞掉异常():
    try:
        return int("abc")
    except:
        pass          # 什么都不做


print("  吞掉异常后返回：", 吞掉异常())
print("  ↑ 返回 None，调用方以为「转换成功但没有结果」")
print("    实际是「转换失败了」，但没人知道")

print("\n⑨ 正确做法：让调用方知道")


def 正确做法():
    try:
        return int("abc"), None
    except ValueError as e:
        return None, f"转换失败：{e}"


值, 错误 = 正确做法()
print("  值：", 值)
print("  错误：", 错误)
print("  ↑ 调用方能区分「没结果」和「出错了」")


# ═════════════════════════════════════════
#  练习：3 道综合题
# ═════════════════════════════════════════

# ─────────────────────────────────────────
#  题 1  ──  健壮的数据处理管道
# ─────────────────────────────────────────
#
# 写一个 `def 处理数据(原始数据们, 处理函数, 最大重试=2)`：
#
#   · 对每条数据调用 处理函数
#   · 失败时重试最多 最大重试 次
#   · 全部失败则记录到失败列表
#   · 返回 (成功列表, 失败列表, 统计信息)
#
# 统计信息包括：总数、成功数、失败数、重试次数合计
#
# 要求：
#   · 处理函数自己写（比如「转成整数」「算平方根」）
#   · 造一批好坏混合的数据测试
#   · 打印一份处理报告
#
# 你的代码：


# ─────────────────────────────────────────
#  题 2  ──  分析异常处理代码
# ═════════════════════════════════════════
#
# 下面 5 段代码，哪些写法有问题？为什么？怎么改？
#
#   A.
#       try:
#           结果 = 复杂计算()
#       except:
#           pass
#
#   B.
#       try:
#           数字 = int(输入)
#       except ValueError:
#           print("请输入数字")
#           数字 = 0
#
#   C.
#       def 保存(数据):
#           try:
#               with open("a.txt", "w") as f:
#                   f.write(数据)
#           except Exception:
#               print("保存失败")
#
#   D.
#       try:
#           列表[10]
#       except IndexError:
#           值 = None
#
#   E.
#       try:
#           f = open("a.txt")
#           内容 = f.read()
#       except FileNotFoundError:
#           内容 = ""
#
# 你的答案：


# ═════════════════════════════════════════
#  答案  ——  先自己写完再看
# ═════════════════════════════════════════
r'''
题 1
    def 处理数据(原始数据们, 处理函数, 最大重试=2):
        """返回 (成功, 失败, 统计)。"""
        成功 = []
        失败 = []
        重试总次数 = 0

        for i, 数据 in enumerate(原始数据们):
            最后错误 = None

            for 尝试 in range(最大重试 + 1):
                try:
                    结果 = 处理函数(数据)
                    成功.append({"序号": i, "数据": 数据, "结果": 结果})
                    最后错误 = None
                    break
                except Exception as e:
                    最后错误 = e
                    if 尝试 < 最大重试:
                        重试总次数 += 1

            if 最后错误 is not None:
                失败.append({
                    "序号": i,
                    "数据": 数据,
                    "错误": f"[{type(最后错误).__name__}] {最后错误}",
                    "尝试次数": 最大重试 + 1,
                })

        统计 = {
            "总数": len(原始数据们),
            "成功": len(成功),
            "失败": len(失败),
            "重试次数": 重试总次数,
        }
        return 成功, 失败, 统计


    —— 测试：

        def 开方(x):
            if x < 0:
                raise ValueError(f"负数不能开方：{x}")
            return x ** 0.5

        数据 = [4, 9, -1, 16, "abc", 25]
        成功, 失败, 统计 = 处理数据(数据, 开方)

        print(f"总数 {统计['总数']}，成功 {统计['成功']}，"
              f"失败 {统计['失败']}，重试了 {统计['重试次数']} 次")

        for 项 in 成功:
            print(f"  ✓ {项['数据']} → {项['结果']}")
        for 项 in 失败:
            print(f"  ✗ 第 {项['序号']} 条（{项['数据']}）：{项['错误']}")

    输出：
        总数 6，成功 4，失败 2，重试了 4 次
          ✓ 4 → 2.0
          ✓ 9 → 3.0
          ✓ 16 → 4.0
          ✓ 25 → 5.0
          ✗ 第 2 条（-1）：[ValueError] 负数不能开方：-1
          ✗ 第 4 条（abc）：[TypeError] unsupported operand...

    —— 几个关键点：

       ① `最后错误 = None` 的双重作用
          · 每轮开始重置
          · 成功后设为 None
          · 循环结束后判断「还是 None 说明成功了」

          这个「哨兵」写法比 `成功 = False` 简洁。

       ② `range(最大重试 + 1)`
          因为「第一次尝试」不算重试。
          最大重试 2 次 = 总共尝试 3 次。

       ③ 重试次数统计
          只在 `尝试 < 最大重试` 时计数，避免把「最后一次失败」算成重试。

       ④ **这个设计对「参数错误」是浪费的**
          `-1` 开方永远失败，重试 3 次也一样。

          更聪明的做法：区分「可重试的异常」和「不可重试的异常」：

              class 不可重试(Exception): pass

          或者按类型判断：

              except (ValueError, TypeError):
                  break          # 参数错误，不重试
              except Exception:
                  continue       # 其他错误，重试

          —— 真实项目里通常会这么区分。

    —— 这题的实用价值：

       批量导入、批量转换、批量爬取 ——
       任何「处理一堆数据」的场景都需要这个模式。

题 2
    A. 有问题（最严重）

        `except:` 捕获所有异常，包括 KeyboardInterrupt（Ctrl+C）、
        SystemExit，而且 `pass` 什么都不做。

        问题：
           ① 真正的 bug 被藏起来了
           ② 程序带着错误状态继续跑
           ③ 连 Ctrl+C 都失效

        改法：

            try:
                结果 = 复杂计算()
            except ValueError as e:
                print(f"计算出错：{e}")
                结果 = None

        至少要：捕获具体的异常 + 记录错误。

    B. 基本可以，但有小问题

        优点：捕获了具体异常（ValueError），给了默认值。

        问题：`数字 = 0` 之后继续往下跑，
        调用方不知道「用户输入错了」。

        如果后面用这个 0 做除法，会出别的问题。

        改进：明确告诉用户后续会发生什么。

            try:
                数字 = int(输入)
            except ValueError:
                print("请输入数字，已按 0 处理")
                数字 = 0

        或者在循环里重问（更好的用户体验）。

    C. 有问题

        三个问题：
           ① `except Exception` 太宽（虽然这里还能接受）
           ② 只打印「保存失败」，没有说为什么
           ③ **最严重：函数没有把失败告诉调用方**

        调用方以为「函数返回了 = 保存成功了」，
        实际可能失败了。

        改法：

            def 保存(数据):
                try:
                    with open("a.txt", "w", encoding="utf-8") as f:
                        f.write(数据)
                    return True, None
                except OSError as e:
                    return False, f"保存失败：{e}"

        或者让异常抛出去，让调用方自己决定。

    D. 有问题（用异常控制流程）

        `列表[10]` 越界本来是可以用 `len()` 判断的：

            if len(列表) > 10:
                值 = 列表[10]
            else:
                值 = None

        用 try/except 也能跑，但：
           ① 异常机制比 if 慢（有栈展开的开销）
           ② 语义上「越界」不是「异常情况」，是「可预期的情况」

        **能用 if 判断的，别用 try。**

        例外：如果数组很长，判断长度反而慢（虽然实际上不会）。

    E. 基本可以，但漏了文件关闭

        `f = open("a.txt")` 之后如果 `f.read()` 出错，
        文件不会被关闭。

        改法：

            try:
                with open("a.txt", encoding="utf-8") as f:
                    内容 = f.read()
            except FileNotFoundError:
                内容 = ""

        用 `with` 保证关闭。

    —— 汇总：

           A  严重（吞掉一切）      改为捕获具体异常+记录
           B  小问题（没提示）      加一句说明
           C  有问题（不告诉调用方）返回状态或抛出去
           D  有问题（用异常控流程）改用 if 判断
           E  小问题（没用 with）   改用 with

    —— 这题的核心：

       **「能跑」和「写法正确」是两回事。**

       A、C、D 都能跑，但都是坏代码。
       区别在于：它们会在未来的某一天，以你完全想不到的方式出问题。
'''
