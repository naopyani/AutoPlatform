# -*- coding: utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqlconnector://root:123456@localhost:3306/AutoPlatForm"
# 数据改变后自动提交
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "cbb88e54b0ff4f03a2666a45818ffaa4"
app.debug = True
db = SQLAlchemy(app)
