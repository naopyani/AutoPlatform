# -*- coding: utf-8 -*-
from flask_restful import Resource, reqparse
from flask import request
from werkzeug.datastructures import FileStorage
import json
from common import db
from common.models import SearchSP
import time
import os


class Upload(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    def post(self):
        self.parser.add_argument('file', type=FileStorage, location='files')
        cur_paths = request.form.getlist('path')
        dict1 = request.files
        dicts = dict1.getlist('files')
        # 找一下path
        for i in range(len(dicts)):
            paths = os.path.abspath('.')
            sp_path = str(paths + "\\" + cur_paths[i] +"\\").replace("\\", '/')
            dicts[i].save(sp_path + dicts[i].filename)
            with open(sp_path + dicts[i].filename, encoding='utf-8') as dt:
                cont = json.load(dt)
                desc = cont["caseDesc"]
            ids = 'sp-' + str(round(time.time() * 1000))
            ssp = SearchSP(id=ids, name=dicts[i].filename, description=desc, path=cur_paths[i])
            db.session.add(ssp)
            db.session.commit()
        print(dicts)
        return 201


if __name__ == '__main__':
    # 13位时间戳
    tp = str(round(time.time() * 1000))
    print(tp)
