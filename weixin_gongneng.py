from wxpy import *
import csv,re

addfriend_request = '加好友'  # 自动添加好友的条件
admin_request_name = 'tian'    # 定义管理员微信名（必须是机器人的好友）  ps：raw_content字段需要自己手动更改微信名，微信号
admin_request_num = 'tian'   # 定义管理员微信号（必须是机器人的好友）
invite_text = "Helo!回复'功能 + 数字'获取对应功能\n1.查询水果价格\n2.我要买水果\n3.了解我们\n4.我要听歌\n例如：要获取查询水果价格的功能时回复\n功能1"  #任意回复获取的菜单
group_name = '测试一下-'    # 定义要查找群的名字
menu_0 = '功能'
menu_1 = '功能1'  # 菜单选项1
menu_2 = '功能2'  # 菜单选项2
menu_3 = '功能3'  # 菜单选项3
menu_4 = '功能4'  # 菜单选项4
menu_5 = '功能5'  # 菜单选项5
csv_1 = 'test.csv'   # 表格1
gs_jianjie = '辰颐物语公司简介……'

bot = Bot(cache_path = True)
bot.enable_puid()  #启用聊天对象的puis属性
#xiaoi = XiaoI('PQunMu3c66bM', 'FrQl1oi1YzpDSULeAIit')   #小i机器人接口
tuling = Tuling(api_key='4f2d2ce18115436bbc0e0b39c77280ce') # 图灵机器人接口
adminer = bot.friends(update=True).search(admin_request_name)[0]
my_group = bot.groups().search(group_name)[0]
group_admin = my_group.members.search(admin_request_name)[0]

groups = bot.groups()

print(my_group)
for group in groups:
    print(group)

admin_puids = frozenset(['XX', 'YY'])   #不可变集合
admins = list(map(lambda x: bot.friends().search(puid=x), admin_puids))

def invite(user):
    groups = sorted(bot.groups(update=True).search(group_name),
                    key=lambda x: x.name)   #sorted用于排序，lambda x:x.name用于群名排序
    if len(groups) > 0:
        for group in groups:
            if len(group.members) == 500:
                continue
            if user in group:
                content = "您已经加入了{} [微笑]".format(group.nick_name)   #经过format格式化的内容传递到{}
                user.send(content)
            else:
                group.add_members(user, use_invitation=True)
            return
        # else:
        #     next_topic = group_tmpl.format(re.search(r'\d+', s).group() + 1)  #当前群的名字后面+1
        #     new_group = bot.create_group(admins, topic=next_topic)
        #     #以上3句代码的解释为：利用for if else语句进行判断，如果从查找的群名里面找不到对应的群就自动创建一个新群并添加进去
    else:
        print('Invite Failed')



def search_mu(msg):  # 音乐查找模块
    import requests,random
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'
    }
    name = msg.split(':')[1]
    num = 20
    if num == '':
        num = '100'

    params = {
        'ct': '24',
        'qqmusic_ver': '1298',
        'new_json': '1',
        'remoteplace': 'txt.yqq.song',
        'searchid': '66514921621705266',
        't': '0',
        'aggr': '1',
        'cr': '1',
        'catZhida': '1',
        'lossless': '0',
        'flag_qc': '0',
        'p': '1',
        'n': int(num),
        'w': name,
        'g_tk': '5381',
        'loginUin': '0',
        'hostUin': '0',
        'format': 'json',
        'inCharset': 'utf8',
        'outCharset': 'utf-8',
        'notice': '0',
        'platform': 'yqq.json',
        'needNewCode': '0',
    }

    res = requests.get(url, headers=headers, params=params)
    musics = res.json()['data']['song']['list']
    n = 1
    m_names=[]
    m_links=[]
    for music in musics:
        m_name = music['title']
        m_album = music['album']['title']
        m_time = music['interval']
        m_link = 'https://y.qq.com/n/yqq/song/' + music['mid'] + '.html'
        if music['mv']['vid'] == '':
            m_video = '无'
        else:
            m_video = 'https://y.qq.com/n/yqq/mv/v/' + music['mv']['vid'] + '.html'
        print(n, m_name, m_album, m_time, m_link, m_video)
        n += 1
        m_names.append(m_name)
        m_links.append(m_link)
    t=random.randint(0,num)
    return m_names[t],m_links[t]



#写表函数
def table(user, text):
    #提取用户的文本，把有用的写入表里
    msg_text = text
    tables = msg_text.split('\n')
    table_name = tables[1].split(':')[1]
    table_jiage = tables[2].split(':')[1]
    table_beizhu = tables[3].split(':')[1]
    table_list = [table_name, table_jiage, table_beizhu]
    if table_name=='' or table_jiage=='':
        user.send('添加失败，请重新添加或者联系管理员')
        return
    user.send('请稍等，后台处理中')
    with open(csv_1, 'r') as f:   #检查表里是否有此水果
        fr_csv = csv.reader(f)
        lists=[]
        for row in fr_csv:
            if table_name == row:
                continue
            elif row[0]=='':
                continue
            else:
               lists.append(row)
        lists.append(table_list)
    with open(csv_1, 'w',newline='') as f:          #写入表
        fw_csv = csv.writer(f)
        for list in lists:
            fw_csv.writerow(list)
    with open(csv_1, 'r') as f:          #查看是否写入成功
        fr_csv = csv.reader(f)
        for row in fr_csv:
            if table_name in row:
                user.send('增加水果价格成功！')
                break
        else:
            user.send('添加失败，请重新添加或者联系管理员')

#查询表函数
def check(user, text):
    if ':' in text:
        check_text = text.split(':')[1]
        if check_text=='':
            check_text = '无水果'
    else:
        check_text ='无水果'
    all_list=[]
    print('check',text,user,check_text)
    with open(csv_1, 'r') as f:
        fr_csv = csv.reader(f)
        cx_list=[]
        for row in fr_csv:
            all_list.append(row[0]+','+row[1]+'元, '+row[2]+'|')
            if check_text in row[0]:
                cx_list.append('水果名称:'+row[0]+"\n价格:"+row[1]+'元'+'  备注:'+row[2]+'|')
    return all_list,cx_list


# 注册好友请求类消息
# @bot.register(msg_types=FRIENDS,enabled=True)
# # 自动接受验证信息中包含 'wxpy' 的好友请求
# def auto_accept_friends(msg):
#     # 判断好友请求中的验证文本
#     if addfriend_request in msg.text.lower():
#         # 接受好友 (msg.card 为该请求的用户对象)
#         new_friend = bot.accept_friend(msg.card)
#         # 或 new_friend = msg.card.accept()
#         # 向新的好友发送消息
#         new_friend.send('机器人自动接受了你的请求,你可以任意回复获取功能菜单，若机器人没回复菜单则表明机器人尚未工作，请等待')



#处理管理员信息
# @bot.register(adminer, msg_types=TEXT)
# def adminer(msg):
#     if '备份' in msg.text:
#         msg.sender.send_file('test.csv')
#     else:
#         return "请检查命令是否输入正确"

myfriend = bot.friends().search(u'tian')[0]
myfriend2 = bot.friends().search(u'何松梅')[0]
myfriend1 = bot.self
print(myfriend2)

@bot.register()
def reply_msg(msg):
    sender_username = msg.sender.raw['UserName']
    # 输出发送信息的好友或者群聊中的人员信息
    print(sender_username)
    # 判断是否和我设置的想要自动恢复到人一致如果一致调用tuling进行消息回复
    if sender_username == myfriend.raw['UserName'] or sender_username == myfriend2.raw['UserName']:

        if '改价格' in msg.text.lower():
            content_2_1 = "请复制下面的模板修改\n填写示例：\n名称：苹果\n价格：6.5\n备注：XX不包邮"
            content_2_2 = "修改-表\n名称:\n价格:\n备注:"
            msg.sender.send(content_2_1)
            msg.sender.send(content_2_2)
        elif '修改-表' in msg.text.lower():
            table(msg.sender, msg.text)
        else:
            # 输出或得到的消息
            print(msg)
            # 调用tuling机器人回复消息，并将消息赋值给message
            message = tuling.do_reply(msg)
            # 输出回复消息的内容
            print(message)


#群聊管理

@bot.register(my_group)
def group_reply(msg):
    print(msg,'111',msg.is_at)

    if '踢出' in msg.text:
        if msg.member == group_admin :
            for member_name in msg.text.split('@')[2:]:
                print(member_name)
                re_name = my_group.members.search(member_name)[0].remove()
                print(re_name)
                msg.sender.send("已经移出:"+member_name)
        else:
            return "你不是管理员不能进行踢人操作"
    elif menu_1 in msg.text.lower():
        content_2_1 = "请复制下面的模板回复\n填写示例：\n查询：苹果"
        content_2_2 = "查询:"
        msg.sender.send(content_2_1)
        msg.sender.send(content_2_2)

    elif menu_2 in msg.text.lower():
        return '购买水果功能测试中'
    elif menu_3 in msg.text.lower():
        msg.sender.send(gs_jianjie)
        msg.sender.send('关注公众号可以了解更多')
        msg.sender.send_raw_msg(
        # 名片的原始消息类型
        raw_type=42,
        # 注意 `username` 在这里应为微信 ID，且被发送的名片必须为自己的好友
        raw_content='<msg username="何松梅" nickname="何松梅"/>'
        )
    elif menu_4 in msg.text.lower():
        content_2_1 = "听首歌轻松下\n填写示例：\n音乐:歌名或歌手名"
        content_2_2 = "音乐:"
        msg.sender.send(content_2_1)
        msg.sender.send(content_2_2)
        #return '我要帮助功能测试中'
    elif '支付宝' in msg.text.lower():
        msg.sender.send('请进入支付宝扫描二维码支付，备注姓名，电话\n')
        msg.sender.send('二维码生成中')
        msg.sender.send_image('zfb.png')
    elif '微信' in msg.text.lower():
        msg.sender.send('请进入微信扫描二维码支付，备注姓名，电话\n')
        msg.sender.send('二维码生成中')
        msg.sender.send_image('wx.png')
    elif '查询' in msg.text:
        a_lists,c_lists=check(msg.sender, msg.text)
        print(a_lists)
        if len(c_lists)>=1:
            msg.sender.send('查询信息如下，如有疑问请联系管理员')
            c=''.join(c_lists)
            msg.sender.send(c.replace('|','\n'))
        else:
            msg.sender.send('水果未查到呀，当前在售水果清单如下')
            a=''.join(a_lists)
            print(a)
            msg.sender.send(a.replace('|','\n'))
    elif '管理员' in msg.text:
        msg.sender.send('请添加名片联系管理员')
        msg.sender.send_raw_msg(
        # 名片的原始消息类型
        raw_type=42,
        # 注意 `username` 在这里应为微信 ID，且被发送的名片必须为自己的好友
        raw_content='<msg username="hesongmei003" nickname="何松梅"/>'
        )
    elif '音乐:' in msg.text:
        m_name,m_link=search_mu(msg.text)
        #msg.sender.send(m_name)
        #msg.sender.send(m_link)
        sss=m_name+m_link
        m_name1, m_link1 = search_mu(msg.text)
        sss=sss+'\n'+m_name1+m_link1
        m_name2, m_link2 = search_mu(msg.text)
        sss=sss+'\n'+m_name2+m_link2
        msg.sender.send(sss)
    elif menu_0 in msg.text:
        msg.sender.send(invite_text)
    else:
        sss=tuling.do_reply(msg)
        print(sss)


bot.join()
