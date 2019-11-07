# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request, jsonify, send_from_directory,make_response
from common.models import SearchSP
from common import db
import os
import json

paths = os.path.abspath('.')
sp_path = paths + "\\SoloPiDir\\"


class SPList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('results', type=int, required=True, help='results不能为空。')

    def get(self):
        response = []
        data = self.parser.parse_args()
        per_page = data.get('results')
        if per_page is None:
            per_page = 10
        search_data = SearchSP.query.order_by(SearchSP.addtime.desc()).paginate(page=1, per_page=per_page)
        for v in search_data.items:
            _dict = {"id": v.id, "name": v.name, "description": v.description, "addtime": v.addtime}
            response.append(_dict)
        print(response)
        pr = jsonify(response)
        print(pr)
        return pr


class SearchList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('description', type=str)

    def post(self):
        response = []
        datas = request.form
        print(datas)
        list_data = SearchSP.query.filter(SearchSP.id.ilike('%' + str(request.form['results[id]']) + '%')) \
            .filter(SearchSP.name.ilike('%' + str(request.form['results[name]']) + '%')) \
            .filter(SearchSP.description.ilike('%' + str(request.form['results[description]']) + '%')) \
            .order_by(SearchSP.addtime.desc()).all()
        for v in list_data:
            _dict = {"id": v.id, "name": v.name, "description": v.description, "addtime": v.addtime}
            response.append(_dict)
        print(response)
        pr = jsonify(response)
        print(pr)
        return pr


class DelList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str, required=True, help='id不能为空!')
        self.parser.add_argument('name', type=str, required=True, help='name不能为空!')

    def get(self):
        data = self.parser.parse_args()
        del_id = data.get('id')
        search_data = SearchSP.query.get_or_404(del_id)
        db.session.delete(search_data)
        db.session.commit()
        # 删除存储路径下的文件
        del_file = str(sp_path + data.get('name')).replace("\\", '/')
        if os.path.exists(del_file):
            os.remove(del_file)
            return jsonify({'msg': "删除成功！"})
        else:
            return jsonify({'msg': "数据库删除成功！但本地不存在该文件！"})


class ViewDetail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='name不能为空!')

    def post(self):
        data = self.parser.parse_args()
        view_file = str(sp_path + data.get('name')).replace("\\", '/')
        if os.path.exists(view_file):
            with open(view_file, 'r', encoding='utf-8') as f:
                load_dict = json.load(f)
                print(load_dict)
                return jsonify(load_dict)
        else:
            return jsonify({})


class DownLoadSP(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='name不能为空!')

    def get(self):
        data = self.parser.parse_args()
        view_file = str(sp_path + data.get('name') + ".json").replace("\\", '/')
        if os.path.exists(view_file):
            response = make_response(send_from_directory(sp_path, data.get('name') + ".json", as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                data.get('name').encode().decode('latin-1'))
            return response
        else:
            return jsonify({'msg': "本地不存在该文件！"})


if __name__ == '__main__':
    pass
    # paths = os.path.abspath('..')
    # sp_path = paths + "\\SoloPiDir\\"
    # view_file = str(sp_path + "测试4-1567737729706.json").replace("\\", '/')
    # if os.path.exists(view_file):
    #     with open(view_file, 'r', encoding='utf-8') as f:
    #         load_dict = json.load(f)
    #         print(load_dict)
    # paths1 = os.path.abspath('..')
    # sp_path1 = paths1 + "\\SoloPiDir\\"
    # print(sp_path1)
