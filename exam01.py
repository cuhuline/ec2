#client -> server : request
#server -> client : response

#python server
#1) flask : 마이크로 웹 프레임워크 (12000 line)
#2) Django: 모든 기능이 포함!! (flask보다 10~20배 무겁다)

import flask

from flask import Flask,render_template,request
from flask import redirect
from flask import make_response #페이지 이동시 정보유지
from aws import detect_labels_local_file # aws.py안에 detect ~ 함수만 쓰고싶어요
from werkzeug.utils import secure_filename  #파일 이름 보안처리
from aws import compare_faces as cf

import os
#static 폴더가 없다면 만들어라
if not os.path.exists("static"):
    os.mkdir("static")
    
app = Flask(__name__)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/compare",methods=["POST"])
def compare_faces():
    if request.method == "POST":
        file1 = request.files["file1"]
        file2 = request.files["file2"]

        file1_filename = secure_filename(file1.filename)
        file2_filename = secure_filename(file2.filename)

        file1.save("static/" + file1_filename)
        file2.save("static/" + file2_filename)

        r = cf("static/" + file1_filename, "static/" + file2_filename)
        return r
    
@app.route("/detect",methods=["POST"])
def detect_label():
    #flask에서 보안 규칙상
    #file이름을 secure처리해야한다
    if request.method == "POST":
        file = request.files["file"]
        #file을 static 폴더에 저장하고
        #해당경로를 detect_lo~ 함수에 전달
        file_name = secure_filename(file.filename)
        file.save("static/" + file_name)
        r = detect_labels_local_file("static/"+ file_name)
    return r

@app.route("/login",methods=["GET"])
def login():
    if request.method == "GET":
        #페이지 이동: redirect

        #페이지가 이동하더라도
        #정보를 남겨 사용!!
        login_id = request.args["login_id"]
        login_pw = request.args["login_pw"]
        if login_id == "leejaejun" and login_pw == "8021":
            #로그인 성공
            response = make_response(redirect("/login/success"))
            #response를 정보를 담을 수 있는 순간!!
            response.set_cookie("user", login_id)
            return response
        else:
            #로그인 실패
            return redirect("/")
    return "로그인 성공"

@app.route("/secret",methods=["POST"])
def box():
    try:
        if request.method == "POST":
        #get -> args[key], post -> form[key]
            hidden = request.form["hidden"]
            return f"비밀정보 : {hidden}"
    except:
        return "데이터 전송 실패"
    
@app.route("/login/success",methods=["GET"])
def login_success():    
    login_id = request.cookies.get("user")
    return f"{login_id}님 환영합니다"

if __name__ == "__main__":
    app.run(host="0.0.0.0")