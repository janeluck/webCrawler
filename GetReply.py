import re
import csv
with open('source.htm', 'r', encoding='UTF-8') as f:
    source = f.read()

#获取所有的回复生成一个list
replies = re.findall('j_l_post(.*?)class="l_post', source, re.S)

#去除广告贴
def getPure(replies):
    return [elem for elem in replies if 'label_text">广告' not in elem]


result = []

#从每一个回复中提取姓名,内容和发帖时间
for each in getPure(replies):
    result.append({
        'username': re.findall('>(.*)', re.findall('p_author_name(.*?)</a>', each, re.S)[0], re.S)[0].strip(),
        'content': re.findall('>(.*)', re.findall('j_d_post_content(.*?)</div>', each, re.S)[0], re.S)[0].strip(),
        'reply_time':re.findall('>(20\d\d-\d\d-.*?)</span', re.findall('post-tail-wrap(.*?)p_props_tail', each, re.S)[0], re.S)[0].strip(),
    })

#生成csv文件
with open('result.csv', 'w', encoding='UTF-8') as f:
    writer = csv.DictWriter(f, fieldnames=['username', 'content', 'reply_time'])
    writer.writeheader()
    writer.writerows(result)


