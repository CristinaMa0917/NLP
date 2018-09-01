import json
import jieba
import fool
from collections import Counter

path1 = '/home/xubinchen/rc_tf-master/data/results/test_predicted_bidaf.json'
path2 = '/home/xubinchen/rc_tf-master/data/results/test_predicted_mlstm.json'
path = '/home/xubinchen/data_test_raw.txt'
jieba.load_userdict('/home/xubinchen/data_test/dict.txt')

jieba.add_word('不含')
jieba.add_word('不到位')
fool.load_userdict('/home/xubinchen/data_test/dict.txt')

jieba.add_word('不含')
jieba.add_word('不到位')


def ori_data(path):
    ori = []
    with open(path) as fin:
        for lidx, line in enumerate(fin):
            sample = json.loads(line.strip())
            question = sample['question']
            quest_id = sample['question_id']
            paragraphs = sample['documents'][0]['paragraphs']
            question_type = sample['question_type']

            data = [quest_id, question, question_type, paragraphs]
            ori.append(data)
    return ori


# [问题id，问题，问题类型，文本段落]
def get_ans(path):
    ans = []
    with open(path) as fin:
        for lidx, line in enumerate(fin):
            sample = json.loads(line.strip())
            answers = sample['answers']
            ans.append(answers)
    return ans


def who_answer(s, flag):
    words, ners = fool.analysis(s)
    ansml = ''
    for ner in ners[0]:
        if flag == 1:
            if 'person' in ner[2]:
                return ner[3]
        else:
            if 'person' in ner[2]:
                ansml = ansml + ner[3]
            if 'org' in ner[2]:
                ansml = ansml + ner[3]
            if 'company' in ner[2]:
                ansml = ansml + ner[3]
    return ansml


def how_much_answer(s):
    ans = ''
    ans_temp = ''
    parts = fool.pos_cut(s)
    try:
        for i, part in enumerate(parts[0]):
            if part[1] == 'm':
                ans_temp = ans_temp + part[0]
                if parts[0][i + 1][1] == 'q':
                    ans = ans + part[0]
                elif parts[0][i + 1][1] == 'm':
                    ans = ans + part[0]
            elif part[1] == 'q':
                if parts[0][i - 1][1] == 'm':
                    ans = ans + part[0]
    except:
        pass
    if ans == '':
        return ans_temp
    return ans


def n_answer(s):
    ans = ''
    parts = fool.pos_cut(s)
    for part in parts[0]:
        if part[1] == 'n':
            ans = ans + part[0]
    return ans


def comma_ans(para):
    ans = ''
    for sub_start in sub_start_anchors:
        if sub_start in para:
            para = para.split(sub_start)[1]
            for sub_end in sub_end_anchors:
                if sub_end in para:
                    index = para.index(sub_end)
                    ans_temp, para = para[:index], para[index:]
                    ans = ans + sub_start + ans_temp + sub_end
                    break
    return ans


oridata = ori_data(path)
answers1 = get_ans(path1)
answers2 = get_ans(path2)

no_anchor = ['否', '不', '没', '未曾', '莫', '非', '不得']
time_anchor = ['时间', '时候', '哪一年', '多久', '哪一天', '那一天', '那一年', '何时']
org_anchor = ['哪个部门', '哪家', '哪个机构', '哪个银行', '哪家公司', '哪个公司', '哪个组织', '哪个辖区', '单位有哪些']
much_anchor = ['多少', '那几', '哪几', '几', '哪次', '哪回', '那次', '哪些', '那些', '多大']
who_anchor = ['哪些人', '哪个人', '谁', '哪位', '什么名字', '叫什么']
loc_anchor = ['在哪', '何处', '去哪', '什么位置', '什么地方', '哪里', '地点？', '哪儿']

ans_anchors = ['：']
# sub_start_anchors = ['一','二','三','四','五','六','七','八','1、','2、','3、','4、']
sub_start_anchors = ['（一）', '（二）', '（三）', '（四）', '（五）', '（六）', '一是', '二是', '三是', '四是', '1、', '2、', '3、', '4、']
sub_end_anchors = ['。', '；']

else_anchor = ['编号是', '']


def describle_refine(oridata, ans1, ans2):
    for i, j, k in zip(oridata, ans1, ans2):
        if i[2] == 'DESCRIPTION':
            ans_flag = 0
            ans = ''

            for ans_anchor in ans_anchors:
                para = i[3][0]
                # print(para)
                if ans_anchor in para:
                    ans_flag = 1
                    index = para.index(ans_anchor)
                    para = para[index:]
                    j[0] = comma_ans(para)
                    if j[0] == '':
                        j[0] = i[3][0].split(ans_anchor)[1]
                    break

            if '章主要' in i[1]:
                if '章' in i[3][0]:
                    result = i[3][0].split('章')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '范围是' in i[1]:
                if '范围' in i[3][0]:
                    result = i[3][0].split('范围')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '什么意义' in i[1]:
                if '意义是' in i[3][0]:
                    result = i[3][0].split('意义是')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '指的' or '指的是' in i[1]:
                if '指' in i[3][0]:
                    result = i[3][0].split('指')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '什么意义' in i[1]:
                if '意义是' in i[3][0]:
                    result = i[3][0].split('意义是')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '适用范围' in i[1]:
                if '范围' in i[3][0]:
                    result = i[3][0].split('范围')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '有什么特点' in i[1]:
                if '特点' in i[3][0]:
                    result = i[3][0].split('特点')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '遵循' in i[1]:
                if '遵循' in i[3][0]:
                    result = i[3][0].split('遵循')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]
            elif '如果' in i[1]:
                if '应' in i[3][0]:
                    result = i[3][0].split('应')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]

#             print('Question_type(%s)'%(i[2]))
#             print('%s:%s'%(i[0],i[1]))
#             print('paragraphs:',i[3][0])
#             print('Answers1:',j[0])
#             print('Answers2:',k[0])
#             print('\n')

def yesno_refine(oridata, ans1, ans2):
    for i, j, k in zip(oridata, ans1, ans2):
        if i[2] == 'yes_no':
            s = i[1]

            s = s.replace('是否', '')
            s = s.replace('？', '')
            s = s.replace('了', '')
            s = s.replace('还', '')
            s = s.replace(' ', '')

            ans = j[0]
            ans = ans.replace('。', '')
            ans = ans.replace('了', '')
            ans = ans.replace('还', '')

            if (s.find('不') >= 0) and (ans.find('不') < 0):
                j[0] = ["no", "不是"]
            else:
                if s == ans:
                    j[0] = ["yes", "是"]
                else:
                    if ans.find(s) >= 0:
                        j[0] = ["yes", "是"]
                    else:
                        if (ans.find('不') >= 0) or (ans.find('不能') >= 0) or (ans.find('只能') >= 0):
                            j[0] = ["no", "不是"]
                        else:
                            j[0] = ["yes", "是"]


def entity_refine(oridata, ans1, ans2):
    null_count = 0
    for i, j, k in zip(oridata, ans1, ans2):

        who_flag, time_flag, org_flag, much_flag, who_flag, loc_flag = 0, 0, 0, 0, 0, 0,

        if i[2] == 'entity':
            for time in time_anchor:
                if time in i[1]:
                    time_flag = 1
                    break

            for org in org_anchor:
                if org in i[1]:
                    org_flag = 1
                    break

            for much in much_anchor:
                if much in i[1]:
                    much_flag = 1
                    break

            for who in who_anchor:
                if who in i[1]:
                    who_flag = 1
                    break

            for loc in loc_anchor:
                if loc in i[1]:
                    loc_flag = 1
                    break

            if time_flag == 1:
                ans = ''
                _, ners = fool.analysis(i[3][0])  # para
                for m in ners[0]:
                    if 'time' in m:
                        ans = ans + m[3]
                j[0] = ans

            elif org_flag == 1:
                ans = ''
                _, ners = fool.analysis(i[3][0], ignore=False)  # para
                for ner in ners[0]:
                    if ner[2] == 'org':
                        ans = ans + ner[3]
                    if ner[2] == 'company':
                        ans = ans + ner[3]
                j[0] = ans

            elif much_flag == 1:
                j[0] = how_much_answer(i[3][0])

            elif who_flag == 1:
                _, ner = fool.analysis(i[1])  # question
                for m in ner[0]:
                    if 'job' in m[2]:
                        who_flag = 1
                j[0] = who_answer(i[3][0], who_flag)

            elif loc_anchor == 1:
                ans = ''
                _, ners = fool.analysis(i[3][0])
                for ner in ers[0]:
                    if ner[2] == 'location':
                        ans = ans + ner[3]
                j[0] = ans

            elif '什么' in i[1]:
                j[0] = n_answer(i[3][0])

            if j[0] == '':
                j[0] = n_answer(i[3][0])


yesno_refine(oridata,answers1,answers2)
entity_refine(oridata,answers1,answers2)
describle_refine(oridata,answers1,answers2)

filename = 'result11.csv'
with open(filename,'w') as f:
    for i,j in zip(oridata,answers1):
        f.write(i[0]+'\t'+str(j[0])+str('\n'))
f.close()


