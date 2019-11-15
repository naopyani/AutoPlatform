# _*_ coding: utf-8 _*_
from common import db
from datetime import datetime


class SearchSP(db.Model):
    __tablename__ = 'search_sp'
    id = db.Column(db.String(500), primary_key=True, autoincrement=False)
    name = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000))
    path = db.Column(db.String(1000), nullable=False)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 注册时间


if __name__ == "__main__":
    db.create_all()
    # ssp = SearchSP(id="sp-1572248574262",
    #                name="测试3-1567737729706.json", description="用来测试", path="SoloPi")
    # db.session.add(ssp)
    # db.session.commit()
