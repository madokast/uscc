import regex
import math

_CharSet = '0123456789ABCDEFGHJKLMNPQRTUWXY'

_Pattern = regex.compile(f'^[{_CharSet}]{{18}}$')

_CharValue = dict(zip(_CharSet, range(len(_CharSet)))) # 字符的值

_RegistrationDeptAndIdTypeMap = dict() # code -> (登记管理部门 registrationDept, 主体类型 idType)

_CheckResultInfo = {
    'valid':'有效', 
    'invalid':'无效', 
    'too long':'长度过长', 
    'too short':'长度过短', 
    'invalid character':'无效字符', 
    'invalid code':'无效编码'
}

def resolve(uscc_code, check_result_info = _CheckResultInfo):
    '''
    返回长度 6 的元组
    - 登记管理部门
    - 主体类型
    - 登记管理机关行政区划码
    - 主体标识码（组织机构代码）
    - 校验码
    - 合法性校验
    '''
    def invalid(reason):
        return ('', '', '', '', '', check_result_info.get(reason, check_result_info['invalid']))
    def check(uscc_code):
        sum = 0
        for i in range(17):
            value = _CharValue[uscc_code[i]]
            weight = int(math.pow(3, i)) % 31
            sum += value * weight
        mod = sum % 31
        sign = 31 - mod
        if sign == 31:
            sign = 0
        return _CharSet[sign] == uscc_code[17]


    if len(uscc_code) > 18:
        return invalid('too long')
    if len(uscc_code) < 18:
        return invalid('too short')
    if not _Pattern.match(uscc_code):
        return invalid('invalid character')
    registration_dept_and_id_type = uscc_code[:2]
    registration_dept_area_code = uscc_code[2:2+6]
    id_code = uscc_code[2+6:2+6+9]
    check_code = uscc_code[2+6+9:]

    regis_info = _RegistrationDeptAndIdTypeMap.get(registration_dept_and_id_type)
    if regis_info is None:
        return invalid('invalid code')
    if check(uscc_code):
        return (regis_info[0], regis_info[1], registration_dept_area_code, id_code, check_code, check_result_info['valid'])
    else:
        return (regis_info[0], regis_info[1], registration_dept_area_code, id_code, check_code, check_result_info['invalid'])

    

    

def _init_RegistrationDeptAndIdTypeMap():
    raw = '''
        机构编制	机关	11
            事业单位	12
            编办直接管理机构编制的群众团体	13
            其他	19
        外交	外国常驻新闻机构	21
            其他	29
        司法行政	律师执业机构	31
            公证处	32
            基层法律服务所	33
            司法鉴定机构	34
            仲裁委员会	35
            其他	39
        文化	外国在华文化中心	41
            其他	49
        民政	社会团体	51
            民办非企业单位	52
            基金会	53
            其他	59
        旅游	外国旅游部门常驻代表机构	61
            港澳台地区旅游部门常驻内地（大陆）代表机构	62
            其他	69
        宗教	宗教活动场所	71
            宗教院校	72
            其他	79
        工会	基层工会	81
            其他	89
        工商	企业	91
            个体工商户	92
            农民专业合作社	93
        中央军委改革和编制办公室	军队事业单位	A1
            其他	A9
        农业	组级集体经济组织	N1
            村级集体经济组织	N2
            乡镇级集体经济组织	N3
            其他	N9
        其他	—	Y1
    '''
    print('init Registration And Type')
    registrationDept = None
    for item in raw.splitlines():
        item = item.rstrip().split()
        if len(item) == 2:
            _RegistrationDeptAndIdTypeMap[item[1]] = (registrationDept, item[0])
        elif len(item) ==3:
            registrationDept = item[0]
            _RegistrationDeptAndIdTypeMap[item[2]] = (registrationDept, item[1])


_init_RegistrationDeptAndIdTypeMap()

if __name__ == '__main__':
    print(len(_CharSet))
    print(_Pattern)
    print(_CharValue)
    print(_RegistrationDeptAndIdTypeMap)

    print(resolve('12440300MB2C92173E')) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'E', '有效')
    print(resolve('12440300MB2C92173A')) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'A', '无效')

    print(resolve('12440300MB2C92173'))   # ('', '', '', '', '', '长度过短')
    print(resolve('12440300MB2C92173AA')) # ('', '', '', '', '', '长度过长')
    print(resolve('12440300MB2C92173O'))  # ('', '', '', '', '', '无效字符')
    print(resolve('C2440300MB2C92173A'))  # ('', '', '', '', '', '无效编码')


    check_result_info = {'valid':'1', 'invalid':'0', 'too long':'-1', 'too short':'-1'}

    print(resolve('12440300MB2C92173E', check_result_info)) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'E', '1')
    print(resolve('12440300MB2C92173A', check_result_info)) # ('机构编制', '事业单位', '440300', 'MB2C92173', 'A', '0')

    print(resolve('12440300MB2C92173', check_result_info))   # ('', '', '', '', '', '-1')
    print(resolve('12440300MB2C92173AA', check_result_info)) # ('', '', '', '', '', '-1')
    print(resolve('12440300MB2C92173O', check_result_info))  # ('', '', '', '', '', '0')
    print(resolve('C2440300MB2C92173A', check_result_info))  # ('', '', '', '', '', '0')
    