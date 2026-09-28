#Flask:创建应用实例.render_template:渲染HTML模板.request:获取网站上用户提交的实时表单数据。redirect:提交完跳回首页
from flask import Flask, render_template,request,redirect
import sqlite3
import os
#timedelta:用来做日期加减，时间差。
from datetime import datetime,timedelta
import pandas as pd
import matplotlib
# 使用非交互式后端，专门用于生成图片:Agg 是一个“无界面”的后端，专门用于只保存图片，不弹窗显示。这样就不会在多线程环境下出问题。
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def table():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("select date,hours from stu",conn)
    conn.close()
    if df.empty:
        return
    day1 = df.groupby("date")["hours"].sum()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(8,5))
    plt.bar(day1.index,day1.values,color="skyblue")
    plt.title("每日学习时长")
    plt.xlabel("日期")
    plt.ylabel("小时")
    plt.xticks(rotation=45)
    plt.tight_layout()
    # 创建一个叫static 文件夹，exist_ok=True：如果没有就跳过
    os.makedirs("static",exist_ok=True)
    #把当前画布保存成为图片文件。static/chart.png：保存的路径和文件名
    plt.savefig("static/chart.png")
    #关闭画布释放内存，在每次使用完之后保持关闭，不占用过多内存。
    plt.close()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
print("=" * 40)
print("app.py 所在目录：", BASE_DIR)
print("模板目录应该是：", TEMPLATE_DIR)
print("这个目录存在吗：", os.path.exists(TEMPLATE_DIR))
print("index.html 存在吗：", os.path.exists(os.path.join(TEMPLATE_DIR, "index.html")))
print("=" * 40)
BASE = r"C:\Users\Administrator\PycharmProjects\PythonProject\学习追踪"

print("=" * 50)
print("BASE 路径：", BASE)
print("BASE 存在吗：", os.path.exists(BASE))
print("BASE 下有什么：", os.listdir(BASE) if os.path.exists(BASE) else "（不存在）")
print("-" * 50)

TEMP = os.path.join(BASE, "templates")
print("TEMPLATE 路径：", TEMP)
print("TEMPLATE 存在吗：", os.path.exists(TEMP))
print("TEMPLATE 下有什么：", os.listdir(TEMP) if os.path.exists(TEMP) else "（不存在）")
print("=" * 50)
app = Flask(__name__, template_folder=r"C:\Users\Administrator\PycharmProjects\PythonProject\学习追踪\templates")
DB = "stu.db"
def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""create table if not exists stu(
                      id integer primary key autoincrement,
                      date text not null,
                      content text not null,
                      hours real not null,
                      mood text)""")
    conn.commit()
    conn.close()
@app.route("/")
def home():
    table()
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("select * from stu order by date desc")
    stus = cursor.fetchall()
    conn.close()
    #拿到今天的日期
    day = datetime.today()
    #day.weekday():返回今天是星期几，timedelta(days=):是指周一到括号里的时间是几天,如果括号里是周一，则是0，如果是周五，则是5，以此来计算今天是周几。
    # day - timedelta(days=):用上面得到的周几数字减去timedelta得到的时间差数的商就是本周1的日期。这是用来计算本周有几天的代码
    monday = day-timedelta(days=day.weekday())
    #将刚刚的到的日期转化为字符串，与数据库保持相同
    monday_str = monday.strftime("%Y-%m-%d")
    #创建一个变量week，初始为0
    week = 0
    #查找数据库的所有记录
    for s in stus:
        # s[1]=数据库第二列，date日期。再判断日期是否大于等于本周一，如果大于等于则本条记录属于本周。
        if s[1] >= monday_str:
            #如果属于本周就把他的s[3]=时间（hours）累加在一起
            week += s[3]

    return render_template("index.html",stus=stus, week=week)
#当浏览器向 /add 这个地址发送 POST 请求时，执行下面的 add() 函数
@app.route("/add",methods = ["post"])
def about():
    #request.form("date")取出表单里 name="date" 那个输入框的数据
    date = request.form.get("date")
    content = request.form.get("content")
    #因为表单传过来的都是字符串，所以需要float转为浮点数，才能存入数据库
    hours = float(request.form["hours"])
    #“mood”,"":表示如果没有填入则返回空字符，不影响代码运行
    mood = request.form.get("mood","")
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("insert into stu (date,content,hours,mood) values (?,?,?,?)",(date,content,hours,mood))
    conn.commit()
    conn.close()
    return redirect("/")
@app.route("/delete/<int:id>")
def delete(id):
    conn =sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("delete from stu where id = ?",(id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
