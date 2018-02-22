#-*- coding:utf-8 -*-
import json

# 读取控制台输入并打印
def readConsole():
    param = raw_input("请输入：")
    print param
    
# 读取数据文件，并打印
def readDataFile():
    file = open("data.txt", 'r')
    while True:
        line = file.readline().strip()
        if line:
            print line
            splitStr(line)
            pass
        else:
            break;
        
# 依据‘=’分隔字符串
def splitStr(str):
    strs = str.split('=', 1)
    print strs
    
# 生成速算扣除数
def genQuickDeduction():
    file = open('rule.txt', 'r')
    result = '# 应纳税所得额对应的速算扣除数：\n# s(单位：元)，速算扣除数：q(单位：元)\n';
    # 上一级应税所得额
    preTaxValue = 0.0
    # 上一级应税税率
    preTaxLevel = 0.0
    # 上一级速算扣除数
    preQuickValue = 0.0
    while True:
        line = file.readline().strip()
        if line:
            # 检是否注释标识开头
            if line.startswith('#'):
                # print line
                continue
            strs = line.split(',')
            if len(strs) > 1:
                ss = strs[0].strip().split('=')
                ps = strs[1].strip().split('=')
                preQuickValue = preTaxValue * (float(ps[1]) - preTaxLevel) * 0.01 + preQuickValue
                # print ss[1] + "的速算扣除数为：%.2f" % preQuickValue
                result += "s=%s, q=%.2f, p=%s\n" % (ss[1], preQuickValue, ps[1])
                preTaxValue = float(ss[1])
                preTaxLevel = float(ps[1])
                pass
            else:
                ps = strs[0].strip().split('=')
                preQuickValue = preTaxValue * (float(ps[1]) - preTaxLevel) * 0.01 + preQuickValue
                # print "最高段位的速算扣除数为：%.2f" % preQuickValue
                result += "q=%.2f, p=%s\n" % (preQuickValue, ps[1])
                pass
            pass
        else:
            break;
        pass
    print result
    writeFile('quickDeduction.txt', result)
    
# 将数据写入指定文件
def writeFile(fileName, data):
    f = open(fileName, "w")
    f.write(data)
    f.close()
    
# 根据应纳税所得额计算税额
def tax(taxValue):
    print "应纳税所得额：%.2f" % taxValue
    file = open('quickDeduction.txt', 'r')
    result = 0.0
    while True:
        line = file.readline().strip()
        if line:
            if line.startswith('#'):
                continue
            strs = line.split(',')
            if len(strs) > 2:
                ss = strs[0].strip().split('=')
                if taxValue > float(ss[1]):
                    continue
                qs = strs[1].strip().split('=')
                ps = strs[2].strip().split('=')
                result = taxValue * float(ps[1]) * 0.01 - float(qs[1])
                print "适用税率%s%%，应纳税额%.2f" % (ps[1], result)
                break
            else:
                qs = strs[0].strip().split('=')
                ps = strs[1].strip().split('=')
                result = taxValue * float(ps[1]) * 0.01 - float(qs[1])
                print "适用税率%s%%，应纳税额%.2f" % (ps[1], result)
                break
            pass
        else:
            break
    return result
    
# 根据汇缴基数计算社保公积金
def insurance(value):
    # 个人需要缴纳的总额
    result = 0.0
    file = open('socialSecurity.txt', 'r')
    flag = False
    while True:
        line = file.readline().strip()
        if line:
            if line.startswith('#'):
                # print line
                continue
            strs = line.strip().split('=')
            rates = strs[1].strip().split(',')
            if len(rates) > 1:
                v = value * float(rates[1].strip('%')) * 0.01
                result += v
                print "[%s]单位汇缴%.2f，个人汇缴%.2f" % (strs[0].strip(), value * float(rates[0].strip('%')) * 0.01, v)
                print str(rates)
            else:
                print "[%s]单位汇缴%.2f" % (strs[0].strip(), value * float(rates[0].strip('%')) * 0.01)
                print str(rates)
        else:
            break
        pass
    print "计费基数：%.2f" % value
    print "个人汇缴总额：%.2f" % result
    return result
    
if __name__ == '__main__':
    # readConsole()
    # readDataFile()
    # genQuickDeduction()
    j = 0.0
    while True:
        j = input("请输入社保公积金计费基数：")
        break
    insu = insurance(j)
    print "\n"
    
    while True:
        inputData = input("请输入工资:")
        if inputData < 0:
            print "输入负数，退出计算"
            break
        y = inputData - insu
        print "税前工资：%.2f, 税前扣除基数：3500" % y
        t = tax(y - 3500)
        print "到手金额：%.2f" % (inputData - t)
        print '\n'
        pass
