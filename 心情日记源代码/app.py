from flask import Flask,render_template,request,redirect #网站框架的搭建
import datetime #调取系统当前时间
import functions as func #自定义函数库
from flask_bootstrap import Bootstrap #前端开发框架
import luyin #自定义的语音输入识别模块
import random #随机调取推荐文章
#app主要运行程序py

app = Flask(__name__)#实例化一个Flask对象
bootstrap = Bootstrap(app)#实例化，创建具有基本页面结构的基模板
app.secret_key='asda1231g/.ad045mbgf;s$#%'#生成密钥


@app.route('/')#页面最初的路由
def coming():
    return redirect('login')#页面最初重定向为登录页面

#登录页面
@app.route('/login',methods=['get','post'])#登录页面路由，路由访问方法可为get，post
def come():
    if request.method == 'post':
           return render_template('login.html')
    return render_template('login.html')#渲染登录页面html

#注册页面
@app.route('/zhuce',methods=['get','post'])#注册页面路由，路由访问方法可为get，post
def zhuce():
    return render_template('zhuce.html')#渲染注册页面html


@app.route('shouye', methods=['get', 'post'])#首页页面路由，路由访问方法可为get，post
def shouye():
    if request.method == 'post':
        return render_template('shouye.html', username="小明")#渲染首页页面html
    return render_template('shouye.html')

#用户登录验证，但本网站是本地网站，则不用验证登录
# @app.route('shouye1', methods=['get', 'post'])
# def shouye1():
#     if request.method == 'post':
#         username=request.form.get('username') 获取用户名
#         password=request.form.get('password') 获取用户密码
#         is_login = func.check_password(username, password) 验证登录名和密码是否正确
#         if is_login==1:
#             return render_template('shouye.html')  # redirect(url_for('shouye.html'))
#         elif is_login==0:
#             return  redirect(url_for('templates',filename='login.html'))
#     return render_template('shouye.html')

@app.route('/zhongxin', methods=['get','post'])#个人中心页面路由，路由访问方法可为get，post
def zhongxin():
        return render_template('zhongxin.html')#渲染个人中心页面html

@app.route('/fenxi2',methods=['get','post'])#无文本分析时的页面路由，路由访问方法可为get，post
def fenxi2():
    return render_template('fenxi.html',sentiment_index="（请在首页进行输入文本分析）")#渲染无文本分析时的页面html，并会显示提示内容

@app.route('/fenxi',methods=['get','post'])#文本分析时的页面路由，路由访问方法可为get，post
def fenxi():
    store = request.form.get('store')#获取html表单上交的日记内容，store为首页的html中textarea输入标签名
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')#获取当前时间，并转化为固定格式
    store_judge=func.check_contain_chinese(store)#调用自定义函数，中英文文本检测
    if store_judge==True:
        sentiment_index=func.Chinese_fenxi(store, now_time)#中文文本分析
    else:
        sentiment_index=func.English_fenxi(store, now_time)#英文文本分析
    print(store_judge)#输出为中英文检测结果，便于后台调试
    print(sentiment_index)#输出分析的情绪值，便于后台调试
    if sentiment_index>=0 and sentiment_index <0.5:
        with open( "1.txt", 'r', encoding='UTF-8') as sentiment1: #打开消极情绪的文章推荐文本
            sentiment_tuijian1=list(sentiment1.readlines()) #读取所有行，并转化为列表存储
            sentiment_tuijian1_names=[]
            for a in range(len(sentiment_tuijian1)): #循环列表，将列表中的网址名字添加到新的列表
                sentiment_tuijian1_names.append(sentiment_tuijian1[a])
                a+=2
            sentiment_tuijian_name=random.choice(sentiment_tuijian1_names)#随机选择一篇推荐文章
            for a in range(len(sentiment_tuijian1)):
                if sentiment_tuijian1[a]==sentiment_tuijian_name:#选择网址名字对应的网址链接
                    sentiment_tuijian_store = sentiment_tuijian1[a+1]
                    if not u'\u4e00' <= sentiment_tuijian_store <= u'\u9fff':#防止文件格式错误所导致的赋值错误
                        sentiment_tuijian_store=sentiment_tuijian1[a]  #赋予正确的网址名和网址
                        sentiment_tuijian_name=sentiment_tuijian1[a-1]
                    break
                else:
                    a+=2  # 循环
       #渲染分析结果为消极的页面html
        return render_template('fenxi1.html', sentiment_index=sentiment_index, sentiment_tuijian_name1=sentiment_tuijian_name, sentiment_tuijian_store=sentiment_tuijian_store)
    elif sentiment_index>=0.5 and sentiment_index<0.6:
        with open( "2.txt", 'r', encoding='UTF-8') as sentiment2:#打开中性情绪的文章推荐文本
            sentiment_tuijian2=list(sentiment2.readlines())
            sentiment_tuijian1_names=[]
            for a in range(len(sentiment_tuijian2)):
                sentiment_tuijian1_names.append(sentiment_tuijian2[a])
                a+=2
            sentiment_tuijian_name=random.choice(sentiment_tuijian1_names)
            for a in range(len(sentiment_tuijian2)):
                if sentiment_tuijian2[a]==sentiment_tuijian_name:
                    sentiment_tuijian_store = sentiment_tuijian2[a+1]
                    if not u'\u4e00' <= sentiment_tuijian_store <= u'\u9fff':
                        sentiment_tuijian_store=sentiment_tuijian2[a]
                        sentiment_tuijian_name=sentiment_tuijian2[a-1]
                    break
                else:
                    a+=2
        #渲染分析结果为中中性页面html
        return render_template('fenxi2.html', sentiment_index=sentiment_index, sentiment_tuijian_name1=sentiment_tuijian_name, sentiment_tuijian_store=sentiment_tuijian_store)
    else:
        with open( "3.txt", 'r', encoding='UTF-8') as sentiment3:#打开积极情绪的文章推荐文本
            sentiment_tuijian3=list(sentiment3.readlines())
            sentiment_tuijian3_names=[]
            for a in range(len(sentiment_tuijian3)):
                sentiment_tuijian3_names.append(sentiment_tuijian3[a])
                a+=2
            sentiment_tuijian_name=random.choice(sentiment_tuijian3_names)
            for a in range(len(sentiment_tuijian3)):
                if sentiment_tuijian3[a]==sentiment_tuijian_name:
                    sentiment_tuijian_store = sentiment_tuijian3[a+1]
                    if not u'\u4e00' <= sentiment_tuijian_store <= u'\u9fff':
                        sentiment_tuijian_store=sentiment_tuijian3[a]
                        sentiment_tuijian_name=sentiment_tuijian3[a-1]
                    break
                else:
                    a+=2
        #渲染分析结果为积极的页面html
        return render_template('fenxi3.html', sentiment_index=sentiment_index, sentiment_tuijian_name1=sentiment_tuijian_name, sentiment_tuijian_store=sentiment_tuijian_store)


@app.route('/fenxi1',methods=['get','post'])#分析结果页面路由，路由访问方法可为get，post
def fenxi1():
    store1 = luyin.luyin()#调取语音输入识别模块的语音输入识别函数
    return render_template('shouye2.html', store1=store1)#渲染首页页面html，将语音识别后的文本传到首页

if __name__ == '__main__':
    app.run(debug=True,port=5000) #运行主程序,参数为用来调试和端口设置