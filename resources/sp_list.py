# -*- coding: utf-8 -*-
import json
import os
import sys

from flask import jsonify, make_response, request, send_from_directory
from flask_restful import Resource, reqparse

from common import db
from common.models import SearchSP

paths = os.path.abspath('.')
sp_path = paths + "\\SoloPi\\"


class SearchList(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('description', type=str)
        self.parser.add_argument('path', type=str, required=True, help='path不能为空！')

    def post(self):
        response = []
        datas = request.form
        print(datas)
        list_data = SearchSP.query.filter(SearchSP.path == str(request.form['results[path]'])) \
            .filter(SearchSP.id.ilike('%' + str(request.form['results[id]']) + '%')) \
            .filter(SearchSP.name.ilike('%' + str(request.form['results[name]']) + '%')) \
            .filter(SearchSP.description.ilike('%' + str(request.form['results[description]']) + '%')) \
            .order_by(SearchSP.addtime.desc()).all()
        for v in list_data:
            _dict = {"id": v.id, "name": v.name,
                     "description": v.description, "addtime": v.addtime}
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
        self.parser.add_argument('path', type=str, required=True, help='path不能为空！')

    def get(self):
        data = self.parser.parse_args()
        # 删除存储路径下的文件
        del_file = str(paths + "\\" + data.get('path') + "\\" + data.get('name')).replace("\\", '/')
        if os.path.exists(del_file):
            del_id = data.get('id')
            search_data = SearchSP.query.get_or_404(del_id)
            db.session.delete(search_data)
            db.session.commit()
            os.remove(del_file)
            return jsonify({'msg': "删除成功！"})
        else:
            return jsonify({'msg': "本地不存在该文件！"})


class ViewDetail(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str, required=True, help='name不能为空!')
        self.parser.add_argument('path', type=str, required=True, help='path不能为空！')

    def post(self):
        data = self.parser.parse_args()
        view_file = str(paths + "\\" + data.get('path') + "\\" + data.get('name')).replace("\\", '/')
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
        self.parser.add_argument('path', type=str, required=True, help='path不能为空！')

    def get(self):
        data = self.parser.parse_args()
        view_file = str(paths + "\\" + data.get('path') + "\\" + data.get('name') +
                        ".json").replace("\\", '/')
        load_path = str(paths + "\\" + data.get('path') + "\\").replace("\\", '/')
        if os.path.exists(view_file):
            response = make_response(send_from_directory(
                load_path, data.get('name') + ".json", as_attachment=True))
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                data.get('name').encode().decode('latin-1'))
            return response
        else:
            return jsonify({'msg': "本地不存在该文件！"})


class addDirSP(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('path', type=str, required=True, help='path不能为空!')

    def post(self):
        data = self.parser.parse_args()
        view_dir = str(paths + "\\" + data.get('path')).replace("\\", '/')
        if os.path.exists(view_dir):
            return jsonify({'code': 1, 'msg': "路径已存在该目录！"})
        else:
            try:
                os.mkdir(view_dir)
            except FileNotFoundError as e:
                return jsonify({'code': 1, 'msg': "找不到指定路径！无法新增", 'error': str(e)})
            return jsonify({'code': 0, 'msg': "新增目录成功！"})


class delDirSP(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('path', type=str, required=True, help='path不能为空!')

    def post(self):
        data = self.parser.parse_args()
        view_dir = str(paths + "\\" + data.get('path')).replace("\\", '/')
        if os.path.exists(view_dir):
            # 判断路径下是否存在文件
            print(os.listdir(view_dir))
            if os.listdir(view_dir):
                return jsonify({'code': 1, 'msg': "该目录存在子文件删除失败！"})
            os.rmdir(view_dir)
            return jsonify({'code': 0, 'msg': "删除目录成功！"})
        return jsonify({'code': 1, 'msg': "该路径不存在！无需删除。"})


class getDirSP(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'path', type=str, required=True, help='path不能为空!')
        self.file_list = []

    def post(self):
        data = self.parser.parse_args()
        view_dir = str(paths + "\\" + data.get('path')).replace("\\", '/')
        for file in os.listdir(view_dir):
            if ".json" in file:
                file_dict = {"title": file, "key": data.get(
                    'path') + "/" + file, "isLeaf": True}
            else:
                file_dict = {"title": file,
                             "key": data.get('path') + "/" + file}
            self.file_list.append(file_dict)
        return jsonify({'filelist': self.file_list})


if __name__ == '__main__':
    pass
    # import os
    # paths = os.path.abspath('..')
    # sp_path = str(paths + "\\SoloPi\\").replace("\\", '/')
    # for file in os.listdir(sp_path):
    #     print(file)
    # view_file = str(sp_path + "测试4-1567737729706.json").replace("\\", '/')
    # if os.path.exists(view_file):
    #     with open(view_file, 'r', encoding='utf-8') as f:
    #         load_dict = json.load(f)
    #         print(load_dict)
    # paths1 = os.path.abspath('..')
    # sp_path1 = paths1 + "\\SoloPiDir\\"
    # print(sp_path1)
