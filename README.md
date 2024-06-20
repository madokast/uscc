# uscc 统一社会信用代码

统一社会信用代码信息提取，获取如下信息，返回一个长度为 6 的元组。

- 登记管理部门
- 主体类型
- 登记管理机关行政区划码
- 主体标识码（组织机构代码）
- 校验码
- 合法性校验

使用示例

```
import uscc
print(uscc.resolve('12440300MB2C92173E')) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'E', '有效')
print(uscc.resolve('12440300MB2C92173A')) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'A', '无效')

print(uscc.resolve('12440300MB2C92173'))   # ('', '', '', '', '', '长度过短')
print(uscc.resolve('12440300MB2C92173AA')) # ('', '', '', '', '', '长度过长')
print(uscc.resolve('12440300MB2C92173O'))  # ('', '', '', '', '', '无效字符')
print(uscc.resolve('C2440300MB2C92173A'))  # ('', '', '', '', '', '无效编码')
```

合法性校验结果可以自己适配，从 resolve 第二个参数传入。例如

```
check_result_info = {'valid':'1', 'invalid':'0', 'too long':'-1', 'too short':'-1'}

print(resolve('12440300MB2C92173E', check_result_info)) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'E', '1')
print(resolve('12440300MB2C92173A', check_result_info)) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'A', '0')

print(resolve('12440300MB2C92173', check_result_info))   # ('', '', '', '', '', '-1')
print(resolve('12440300MB2C92173AA', check_result_info)) # ('', '', '', '', '', '-1')
print(resolve('12440300MB2C92173O', check_result_info))  # ('', '', '', '', '', '0')
print(resolve('C2440300MB2C92173A', check_result_info))  # ('', '', '', '', '', '0')
```

