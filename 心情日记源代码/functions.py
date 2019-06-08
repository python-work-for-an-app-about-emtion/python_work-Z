# -*- coding:utf8 -*-
# 汇总函数py
import sys
import importlib  # 模块重载，便于调试
import Chinese  # 自定义中文文本情绪分析模块
import English  # 自定义英文文本情绪分析模块

importlib.reload(sys)  # 进行模块重载

# 判断所输入文本是中文还是英文
def check_contain_chinese(check_str):
	for ch in check_str:         # check_str.encode('utf-8'):
		if u'\u4e00' <= ch <= u'\u9fff':  # 中文Unicode范围
			return True
	return False

# 中文文本情绪分析函数
def Chinese_fenxi(store,now_time_str):
	sentiment_index = Chinese.Chinese(str(store))  # 调用自定义的中文文本情绪分析模块中的分析函数
	write_fenxi(sentiment_index, now_time_str)  # 将情绪分析指数同日记提交时间存储
	return sentiment_index

# 英文文本分析函数
def English_fenxi(store,now_time_str):
	sentiment_index=English.English(store)  # 调用自定义的英文文本情绪分析模块中的分析函数
	write_fenxi(sentiment_index, now_time_str)  # 将情绪分析指数同日记提交时间存储
	return sentiment_index

def write_fenxi(sentiment_index,now_time_str):  # 将情绪分析指数同日记提交时间存储到store.txt
	data1={}
	data1[now_time_str] = sentiment_index
	with open("store.txt", 'w+') as file:
		file.writelines(data1)

def userinfoshow(username):          # 个人中心显示信息，打开userdata.txt
	with open("userdata.txt",'r+') as file:
		data = file.read()
		print("账号：" + str(username))
		sex=data[username][1]
		year=data[username][2]
		print("性别：" + str(sex))
		print("年龄："+str(year))

# 用户数据保存
def save_user(username, password, sex, year):
	with open("userdata.txt", 'r+') as file:  # 将注册时的用户信息存储到userdata.txt中
		data = file.read()
	datas=dict(data)
	datas[username] = [password, sex, year]
	write_user(datas)

def write_user(datas):
	with open("userdata.txt", 'w+') as file:  # 将注册时的用户信息存储到userdata.txt中
		file.writelines(datas)
# 登录检查
def check_password(username, password):   # 登录时验证用户信息
	data = open('userdata.txt', 'r', encoding="utf-8").read()
	datas = dict(data)
	if username in datas.keys():
		if password == datas[username][0]:
			return 1
		else:
			return 0
	else:
		return 0

