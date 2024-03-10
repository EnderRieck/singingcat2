def calcu_distance(note1: str, note0: str):
    notelist = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    updistance = 0
    downdistance = 0
    change_pitch_up = 0
    change_pitch_down = 0
    # 上行搜索
    # 获取音的索引值
    i1 = notelist.index(note1)
    uplist = notelist * 2
    uplist = uplist[i1:]
    for i, note in enumerate(uplist):
        if note == "C" and note1 != "C":
            change_pitch_up += 1
        if note == note0:
            updistance = i
            break

    # 下行搜索
    downlist = notelist
    downlist.reverse()
    i1 = downlist.index(note1)
    downlist *= 2
    downlist = downlist[i1:]
    cc = 0
    for i, note in enumerate(downlist):
        if note == "C" and note0 != "C":
            change_pitch_down -= 1
        if note == note0:
            downdistance = -i
            break

    # 比较两个距离的大小
    if abs(updistance) > abs(downdistance):
        return [downdistance, change_pitch_down]
    else:
        return [updistance, change_pitch_up]

def recommend(note, raw):
    pitch = (note[-1], raw[-1])
    note = (note[ :-1], raw[ :-1])
    opt_list = ["C", "D", "E", "G", "A"]
    dist_dict = {name: calcu_distance(note[0], name) for name in opt_list}
    print(dist_dict)
    for name in opt_list:
        dist_dict[name][1] = calcu_distance(note[1], name)[1]

    print(dist_dict)

    recom_list = []
    pitch_list = []

    for _ in range(len(opt_list)):
        # 将字典中的值按绝对值进行排序，取出最小的，如果绝对值相等，优先取正值（对负值进行+0.1的惩罚）
        min_key = min(dist_dict, key=lambda k: dist_dict[k][0] if dist_dict[k][0]>=0 else -dist_dict[k][0]+0.1)
        recom_list.append(min_key)
        pitch_list.append(dist_dict[min_key][1] + int(pitch[1]))
        del dist_dict[min_key]


    return recom_list, pitch_list

# rec = recommend("C6")
# print(rec)