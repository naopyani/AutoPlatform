# -*- coding: utf-8 -*-
from flask_restful import Api
from resources.upload import Upload
from resources.sp_list import SearchList, DelList, ViewDetail, DownLoadSP, addDirSP, delDirSP, getDirSP
from flask_cors import CORS
from common import app

api = Api(app)
CORS(app, supports_credentials=True)

api.add_resource(Upload, '/upload')
api.add_resource(SearchList, '/splist/searchlist')
api.add_resource(DelList, '/splist/dellist/')
api.add_resource(ViewDetail, '/splist/viewdetail')
api.add_resource(DownLoadSP, '/splist/downloadsp')
api.add_resource(addDirSP, '/splist/adddirsp')
api.add_resource(delDirSP, '/splist/deldirsp')
api.add_resource(getDirSP, '/splist/getdirsp')
if __name__ == '__main__':
    app.run()
