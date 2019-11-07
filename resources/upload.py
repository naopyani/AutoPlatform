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
        dict1 = request.files
        dicts = dict1.getlist('files[]')
        for _dict in dicts:
            paths = os.path.abspath('.')
            sp_path = str(paths + "\\SoloPiDir\\").replace("\\", '/')
            _dict.save(sp_path + _dict.filename)
            with open(sp_path + _dict.filename, encoding='utf-8') as dt:
                cont = json.load(dt)
                desc = cont["caseDesc"]
            ids = 'sp-' + str(round(time.time() * 1000))
            ssp = SearchSP(id=ids, name=_dict.filename, description=desc)
            db.session.add(ssp)
            db.session.commit()
        print(dicts)
        return 201


if __name__ == '__main__':
    # 13位时间戳
    tp = str(round(time.time() * 1000))
    print(tp)
