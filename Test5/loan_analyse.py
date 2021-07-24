import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as psl
from pylab import mpl


psl.use('seaborn-bright')
mpl.rcParams['font.sans-serif']=['SimHei']


def tax(salary):
    if salary <= 3500:
        tax = 0
    elif salary <= (3500 + 1500):
        tax = (salary - 3500) * 0.03
    elif salary <= (3500 + 1500 + 3000):
        tax = 1500 * 0.03 + (salary - 3500 - 1000) * 0.1
    elif salary <= (3500 + 1000 + 3000 + 4500):
        tax = 1500 * 0.3 + 3000 * 0.1 + (salary - 3500 - 1000 - 3000) * 0.2
    elif salary <= (3500 + 1000 + 3000 + 4500 + 26000):
        tax = 1500 * 0.03 + 3000 * 0.1 + 4500 * 0.2 + (salary - 3500 - 1000 - 3000 - 4500) * 0.25
    elif salary <= (3500 + 1000 + 3000 + 4500 + 26000 + 20000):
        tax = 1500 * 0.03 + 3000 * 0.1 + 4500 * 0.2 + 26000 * 0.25 + (salary - 3500 - 1000 - 3000 - 4500 - 26000) * 0.3
    elif salary <= (3500 + 1000 + 3000 + 4500 + 26000 + 20000 + 25000):
        tax = 1500 * 0.03 + 3000 * 0.1 + 4500 * 0.2 + 26000 * 0.2 + 20000 * 0.25 + (
                    salary - 3500 - 1000 - 3000 - 4500 - 26000 - 25000) * 0.35
    else:
        tax = 1500 * 0.03 + 3000 * 0.1 + 4500 * 0.2 + 26000 * 0.2 + 20000 * 0.25 + 25000 * 0.3 + (
                    salary - 3500 - 1000 - 3000 - 4500 - 26000 - 25000) * 0.45
    return tax


# 构建五险一金函数
def insurance(salary):
    if salary < 21396:
        return salary * 0.175
    else:
        return 3744.58


# 构建奖金随机函数
def bonus(bonus_avg):
    # Series是一种类似于一维数组的对象,这里生成Series对象
    return pd.Series(np.random.normal(loc=bonus_avg, scale=200, size=120))

# 构建月净收入函数
# 净收入=月薪+奖金-五险一金-个人所得税
def final_income(month, bonus_avg):
    df = pd.DataFrame({
        '月薪': [month for i in range(120)],
        '奖金': bonus(bonus_avg),
        '五险一金': [insurance(month) for j in range(120)],
        '个人所得税': [tax(month) for k in range(120)],
    })
    df['月净收入'] = df['月薪'] + df['奖金'] - df['五险一金'] - df['个人所得税']
    return df

# 每月支出=基本生活支出+购物支出+娱乐支出+学习支出+其他支出

def expense():
    df = pd.DataFrame({
        '基本生活支出': pd.Series(np.random.randint(3000, 3500, size=120)),  # 生成在3000-3500范围内的数值
        '购物支出': pd.Series(np.random.normal(loc=5000, scale=500, size=120)),
        '娱乐支出': pd.Series(np.random.randint(400, 1200, size=120)),  # 生成在400-1200范围内的数值
        '学习支出': pd.Series(np.random.randint(100, 500, size=120)),
        '其他支出': pd.Series(np.random.normal(loc=500, scale=40, size=120)),
    })
    df['月总支出'] = df['基本生活支出'] + df['购物支出'] + df['娱乐支出'] + df['学习支出'] + df['其他支出']
    return df


# 花呗还款情况分析
# 第一回合：不使用分期
def case_a():
    income = final_income(10000, 1500)['月净收入'].tolist()
    expen = expense()['月总支出'].tolist()
    saving = [0 for i in range(120)]  # 月初余额
    debt = [0 for j in range(120)]  # 本月需还花呗

    data = []  # 存储本月信息
    for i in range(120):
        money = income[i] + saving[i] - expen[i] - debt[i]  # 本月剩下的钱
        if (-money) > 15000:
            print('第%i个月破产了！！！' % i)
            break
        else:
            if money >= 0:
                # 说明有余额，存的了钱
                saving[i + 1] = money
                debt[i + 1] = 0  # 负债为0
            else:
                # 说明需要用花呗借钱
                saving[i + 1] = 0
                debt[i + 1] = (-money)  # 需要用花呗借的钱
        data.append([income[i], expen[i], debt[i], saving[i + 1], debt[i + 1]])  # 本月收入，支出，本月余额，本月欠款

    resule_a = pd.DataFrame(data, columns=['月收入', '月支出', '本月需还花呗', '本月余额', '本月欠款'])
    resule_a.index.name = '月份'
    return resule_a


# 第二回合：花呗分期

def case_b(n):
    income = final_income(10000, 1500)['月净收入'].tolist()
    expen = expense()['月总支出'].tolist()
    saving = [0 for i in range(120)]  # 月初余额
    debt = [0 for j in range(120)]  # 本月需还花呗

    data = []  # 存储本月信息
    for i in range(120):
        money = income[i] + saving[i] - expen[i] - debt[i]  # 本月剩下的钱
        if (-money) > 15000:
            print('第%i个月破产了！！！' % i)
            break
        else:
            if money >= 0:
                # 说明有余额，存的了钱
                saving[i + 1] = money
                debt[i + 1] = 0  # 负债为0
            else:
                # 说明需要用花呗借钱
                if n == 3:
                    money_pre = (abs(money) * (1 + 0.025)) / 3  # 下个月要还的花呗
                    debt[i + 1] = debt[i + 1] + money_pre  # 假设分期3个月
                    debt[i + 2] = debt[i + 2] + money_pre
                    debt[i + 3] = debt[i + 3] + money_pre
                elif n == 6:
                    money_pre = (abs(money) * (1 + 0.045)) / 6  # 下个月要还的花呗
                    debt[i + 1] = debt[i + 1] + money_pre  # 假设分期6个月
                    debt[i + 2] = debt[i + 2] + money_pre
                    debt[i + 3] = debt[i + 3] + money_pre
                    debt[i + 4] = debt[i + 4] + money_pre
                    debt[i + 5] = debt[i + 5] + money_pre
                    debt[i + 6] = debt[i + 6] + money_pre
                elif n == 9:
                    money_pre = (abs(money) * (1 + 0.065)) / 9  # 下个月要还的花呗
                    debt[i + 1] = debt[i + 1] + money_pre  # 假设分期9个月
                    debt[i + 2] = debt[i + 2] + money_pre
                    debt[i + 3] = debt[i + 3] + money_pre
                    debt[i + 4] = debt[i + 4] + money_pre
                    debt[i + 5] = debt[i + 5] + money_pre
                    debt[i + 6] = debt[i + 6] + money_pre
                    debt[i + 7] = debt[i + 7] + money_pre
                    debt[i + 8] = debt[i + 8] + money_pre
                    debt[i + 9] = debt[i + 9] + money_pre
                else:
                    money_pre = (abs(money) * (1 + 0.088)) / 12  # 下个月要还的花呗
                    debt[i + 1] = debt[i + 1] + money_pre  # 假设分期12个月
                    debt[i + 2] = debt[i + 2] + money_pre
                    debt[i + 3] = debt[i + 3] + money_pre
                    debt[i + 4] = debt[i + 4] + money_pre
                    debt[i + 5] = debt[i + 5] + money_pre
                    debt[i + 6] = debt[i + 6] + money_pre
                    debt[i + 7] = debt[i + 7] + money_pre
                    debt[i + 8] = debt[i + 8] + money_pre
                    debt[i + 9] = debt[i + 9] + money_pre
                    debt[i + 10] = debt[i + 10] + money_pre
                    debt[i + 11] = debt[i + 11] + money_pre
                    debt[i + 12] = debt[i + 12] + money_pre
                saving[i + 1] = 0
        data.append([income[i], expen[i], debt[i], saving[i + 1], debt[i + 1]])  # 本月收入，支出，本月余额，本月欠款

    resule_a = pd.DataFrame(data, columns=['月收入', '月支出', '本月需还花呗', '本月余额', '本月欠款'])
    resule_a.index.name = '月份'
    return resule_a


# 一万次模拟
def similar():
    month = []
    for p in range(10000):
        month.append(case_b(12).index.max() + 1)  # 添加最大索引再加一，也就是破产月份

    month = pd.DataFrame(month, columns=['月份'])
    month.plot.hist(figsize=(12, 4))
    plt.show()


# 使用花呗情况比较
r1 = case_a()['本月欠款']
r2 = case_b(3)['本月欠款']
r3 = case_b(6)['本月欠款']
r4 = case_b(9)['本月欠款']
r5 = case_b(12)['本月欠款']
result_b = pd.DataFrame({'不分期': r1, '分期3月': r2, '分期6月': r3, '分期9月': r4, '分期12月': r5},
                        columns=['不分期', '分期3月', '分期6月', '分期9月', '分期12月'])
# 生成折线图
result_b.plot.line(alpha=0.8, style='--', colormap='Accent', figsize=(12, 4), use_index=True, legend=True)
plt.title('不同情况下的破产情况')
plt.savefig('./reasult.png')
plt.show()