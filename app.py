from flask import Flask, render_template, Response,request
from camera import VideoCamera
from camera import emotion_list
import matplotlib.pyplot as plt
import io
import os, sys
import urllib, base64
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/num' , methods=['POST'])
def num():
    print(emotion_list)
    print("\n\nInside--NUM--Inside--NUMInside--NUM\n")
    sad = emotion_list.count('Sad')
    angry = emotion_list.count('Angry')
    disgust = emotion_list.count('Disgust')
    fear = emotion_list.count('Fear')
    happy = emotion_list.count('Happy')
    surprise = emotion_list.count('Surprise')
    # print("\nSad : ",sad)
    # print("\nangry : ",angry)
    # print("\ndisgust : ",disgust)
    # print("\nfear : ",fear)
    # print("\nhappy : ",happy)
    # print("\nsurprise : ",surprise)
    a=0
    b=0
    d=0
    bb =0
    flag=0

    val1 = int(request.form['q1'])

    if(val1==1):d+=5
    elif(val1==2):d+=10
    elif(val1==4):b+=10

    val2 = int(request.form['q2'])

    if(val2==1):a+=10
    elif(val2==2):b+=10
    elif(val2== 3):a=+1
    elif(val2==4):d+=10

    val3 = int(request.form['q3'])
    if(val3==1):d+=10
    elif(val3==2):a+=5
    elif(val3 == 3):b=+5

    val4 = int(request.form['q4'])
    if(val4==2):b+=50

    val5 = int(request.form['q5'])
    if(val5==1):d+=20
    elif(val5==2):a+=10

    val6 = int(request.form['q6'])
    if(val6 ==1):a+=20
    elif(val6 ==2):d+=10
    if(val6 == 3):a+=20
    elif(val6== 4):a+=20

    if(a>d and a>b):
        flag=2

    elif(d>b and d>a):
        flag=1

    elif(b>a and b>d):
        flag =3
    if(flag==1):
        return render_template('depression.html')
    elif(flag==2):
        return render_template('insomnia.html')
    elif(flag==3):
        return render_template('binge.html')

@app.route('/numd' , methods=['POST'])
def numd():
    print(emotion_list)
    print("\n\nInside--NUM--Inside--NUMInside--NUM\n")
    sad = emotion_list.count('Sad')
    angry = emotion_list.count('Angry')
    disgust = emotion_list.count('Disgust')
    fear = emotion_list.count('Fear')
    happy = emotion_list.count('Happy')
    surprise = emotion_list.count('Surprise')
    print("\nSad : ",sad)
    print("\nangry : ",angry)
    print("\ndisgust : ",disgust)
    print("\nfear : ",fear)
    print("\nhappy : ",happy)
    print("\nsurprise : ",surprise)
    emotion_list.clear()#very-very imp
    dd =0
    val1 = int(request.form['d1'])
    if(val1==3):dd+=5
    elif(val1==2):dd+=5
    elif(val1==4):dd+=10

    val2 = int(request.form['d2'])
    if(val2 ==1):dd+=20
    if(val2 == 3):dd+=5

    val3 = int(request.form['d3'])
    if(val3 ==1):dd+=10
    elif(val3 ==3):dd+=1
    elif(val3== 4):dd+=2

    val4 = int(request.form['d4'])
    if(val4 ==1):dd+=10

    val5 = int(request.form['d5'])
    if(val5 ==2):dd+=2
    elif(val5 == 3):dd+=2
    elif(val5== 4):dd+=10

    val6 = int(request.form['d6'])
    if(val6 ==1):dd+=10

    x = 50

    #plot for all emotions
    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [sad, angry, disgust, fear, happy , surprise]#count will come of respective emotions
    labels = ['Sad', 'Angry', 'Disgust', 'Fear', 'Happy', 'Surprise']
    colors = ['#264653' , '#2a9d8f' ,'#e9c46a', '#f4a261' ,'#e76f51' , '#e63946']
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors=colors,
            wedgeprops={'edgecolor':'black'})
    plt.title('Emotions Chart')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri1 = urllib.parse.quote(string1)

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [10, 13, 13, 19, 16 , 7, 16, 6]
    labels = ['<25 yrs', '25-30 yrs', '31-35 yrs', '36-40 yrs', '41-45 yrs', '46-50 yrs', '51-55 yrs', '56-60 yrs']
    colors = ['#c9cba3' , '#55415f' , '#646964' , '#d77355' , '#508cd7' , '#64b964' , '#e6c86e' ,'#dcf5ff' ]
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors = colors,
            wedgeprops={'edgecolor':'black'})

    plt.title('Mental Illness by Age Group')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri2 = urllib.parse.quote(string1)


    if(dd>x):
        return render_template('result.html',result = int(dd),dis='depression',data1=uri1,data2=uri2)
    elif(int(dd)>30 and int(dd)<=50):
        return render_template('result.html',result=int(dd),dis='depression',data1=uri1,data2=uri2)
    else:
        return render_template('result.html',result='1',dis='none',data1=uri1,data2=uri2)

@app.route('/numb' , methods=['POST'])
def numb():
    print(emotion_list)
    print("\n\nInside--NUM--Inside--NUMInside--NUM\n")
    sad = emotion_list.count('Sad')
    angry = emotion_list.count('Angry')
    disgust = emotion_list.count('Disgust')
    fear = emotion_list.count('Fear')
    happy = emotion_list.count('Happy')
    surprise = emotion_list.count('Surprise')
    print("\nSad : ",sad)
    print("\nangry : ",angry)
    print("\ndisgust : ",disgust)
    print("\nfear : ",fear)
    print("\nhappy : ",happy)
    print("\nsurprise : ",surprise)
    emotion_list.clear()#very-very imp
    bb = 0
    val1 = int(request.form['b1'])
    if(val1 ==2):bb+=2
    elif(val1 == 3):bb+=2
    elif(val1== 4):bb+=10

    val2 = int(request.form['b2'])
    if(val2 ==2):bb+=5

    val3 = int(request.form['b3'])
    if(val3 ==2):bb+=10

    val4= int(request.form['b4'])
    if(val4== 4):bb+=5

    val5 = int(request.form['b5'])
    if(val5 ==2):bb+=10

    val6 = int(request.form['b6'])
    if(val6 ==2):bb+=2
    elif(val6 == 1):bb+=2

    x2 = 20

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [sad, angry, disgust, fear, happy , surprise]#count will come of respective emotions
    labels = ['Sad', 'Angry', 'Disgust', 'Fear', 'Happy', 'Surprise']
    colors = ['#264653' , '#2a9d8f' ,'#e9c46a', '#f4a261' ,'#e76f51' , '#e63946']
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors=colors,
            wedgeprops={'edgecolor':'black'})
    plt.title('Emotions Chart')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string1)

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [10, 13, 13, 19, 16 , 7, 16, 6]
    labels = ['<25 yrs', '25-30 yrs', '31-35 yrs', '36-40 yrs', '41-45 yrs', '46-50 yrs', '51-55 yrs', '56-60 yrs']
    colors = ['#c9cba3' , '#55415f' , '#646964' , '#d77355' , '#508cd7' , '#64b964' , '#e6c86e' ,'#dcf5ff' ]
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors = colors,
            wedgeprops={'edgecolor':'black'})

    plt.title('Mental Illness by Age Group')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string1)


    if(bb>x2):
        return render_template('result.html',result=int(bb),dis='insomnia',data1=uri1,data2=uri2)
    else:
        return render_template('result.html',result=1,dis='none',data1=uri1,data2=uri2)

@app.route('/numi' , methods=['POST'])
def numi():
    print(emotion_list)
    print("\n\nInside--NUM--Inside--NUMInside--NUM\n")
    sad = emotion_list.count('Sad')
    angry = emotion_list.count('Angry')
    disgust = emotion_list.count('Disgust')
    fear = emotion_list.count('Fear')
    happy = emotion_list.count('Happy')
    surprise = emotion_list.count('Surprise')
    print("\nSad : ",sad)
    print("\nangry : ",angry)
    print("\ndisgust : ",disgust)
    print("\nfear : ",fear)
    print("\nhappy : ",happy)
    print("\nsurprise : ",surprise)
    emotion_list.clear()#very-very imp
    aa =0
    val1 = int(request.form['z1'])
    if(val1 ==2):aa+=2
    elif(val1 == 3):aa+=2
    elif(val1== 4):aa+=10

    val2 = int(request.form['z2'])
    if(val2 ==3):aa+=5
    elif(val2 == 4):aa+=10

    val3 = int(request.form['z3'])
    if(val3 ==2):aa+=5
    elif(val3 == 3):aa+=2

    val5 = int(request.form['z5'])
    if(val5 ==1):aa+=10
    elif(val5 == 2):aa+=5
    elif(val5== 3):aa+=4

    val6 = int(request.form['z6'])
    if(val6 ==2):aa+=5

    x3 = 25


    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [sad, angry, disgust, fear, happy , surprise]#count will come of respective emotions
    labels = ['Sad', 'Angry', 'Disgust', 'Fear', 'Happy', 'Surprise']
    colors = ['#264653' , '#2a9d8f' ,'#e9c46a', '#f4a261' ,'#e76f51' , '#e63946']
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors=colors,
            wedgeprops={'edgecolor':'black'})
    plt.title('Emotions Chart')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string1)

    plt.style.use('fivethirtyeight')
    plt.figure(figsize=(8,7))
    slices = [10, 13, 13, 19, 16 , 7, 16, 6]
    labels = ['<25 yrs', '25-30 yrs', '31-35 yrs', '36-40 yrs', '41-45 yrs', '46-50 yrs', '51-55 yrs', '56-60 yrs']
    colors = ['#c9cba3' , '#55415f' , '#646964' , '#d77355' , '#508cd7' , '#64b964' , '#e6c86e' ,'#dcf5ff' ]
    plt.pie(slices, labels=labels,shadow=True, startangle=90,
            autopct='%1.1f%%',colors = colors,
            wedgeprops={'edgecolor':'black'})

    plt.title('Mental Illness by Age Group')
    plt.tight_layout()
    fig1 = plt.gcf()
    buf = io.BytesIO()
    fig1.savefig(buf, format="png")
    buf.seek(0)
    string1 = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string1)


    if(aa>x3):
        return render_template('result.html',result = int(aa),dis= 'binge',data=uri)
    else:
        return render_template('result.html',result = 1,dis = 'none',data=uri)

@app.route('/result')
def result():
    print(emotion_list)
    sad = emotion_list.count('Sad')
    angry = emotion_list.count('Angry')
    disgust = emotion_list.count('Disgust')
    fear = emotion_list.count('Fear')
    happy = emotion_list.count('Happy')
    surprise = emotion_list.count('Surprise')
    print("\nSad : ",sad)
    print("\nangry : ",angry)
    print("\ndisgust : ",disgust)
    print("\nfear : ",fear)
    print("\nhappy : ",happy)
    print("\nsurprise : ",surprise)
    emotion_list.clear()#very-very imp
    return render_template('final_result.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
