ans_anchor = '：'
# sub_start_anchors = ['一','二','三','四','五','六','七','八','1、','2、','3、','4、']
sub_start_anchors = ['一是', '二是', '三是', '四是', '五是', '六是', '七是', '八是', '九是',
                     '（一）', '（二）', '（三）', '（四）', '（五）', '（六）', '（七）', '（八）',
                     '1、', '2、', '3、', '4、', '5、', '6、', '7、', '8、']
sub_end_anchors = ['。', '；']


def describle_refine(oridata, ans1, ans2):
    for i, j, k in zip(oridata, ans1, ans2):
        if i[2] == 'DESCRIPTION':

            comma_flag = 0
            num_flag = 0
            much_flag = 0
            who_flag = 0
            loc_flag = 0

            ## flag built
            if ans_anchor in i[3][0]:
                comma_flag = 1

            for sub_start in sub_start_anchors:
                if sub_start in i[3][0]:
                    num_flag = 1

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

            for org in org_anchor:
                if org in i[1]:
                    org_flag = 1
                    break

                    ## action
            para = i[3][0]
            if comma_flag == 1:
                index = para.index(ans_anchor)
                para = para[(index + 1):]
                j[0] = comma_ans(para)

                if j[0] == '':
                    j[0] = para
                    continue
                else:
                    continue

            if num_flag == 1:
                j[0] = comma_ans(para)

            elif '章主要' in i[1]:
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
            elif '目标是什么' in i[1]:
                if '目标是' in i[3][0]:
                    result = i[3][0].split('目标是')[1:]
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

            elif much_flag == 1:
                j[0] = how_much_answer(i[3][0])

            elif org_flag == 1:
                ans = ''
                _, ners = fool.analysis(i[3][0], ignore=False)  # para
                for ner in ners[0]:
                    if ner[2] == 'org':
                        ans = ans + ner[3]
                    if ner[2] == 'company':
                        ans = ans + ner[3]
                j[0] = ans

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

            elif '分为' in i[1]:
                if '分为' in i[3][0]:
                    result = i[3][0].split('分为')[1:]
                    s = ''
                    for tok in result:
                        s += tok
                    j[0] = s
                else:
                    j[0] = i[3][0]