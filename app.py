# -*- coding: utf-8 -*-
from flask_restful import Api
from resources.upload import Upload
from resources.sp_list import SPList, SearchList, DelList,ViewDetail,DownLoadSP
from flask_cors import CORS
from common import app

api = Api(app)
CORS(app, supports_credentials=True)

api.add_resource(Upload, '/upload')
api.add_resource(SPList, '/splist/')
api.add_resource(SearchList, '/splist/searchlist')
api.add_resource(DelList, '/splist/dellist/')
api.add_resource(ViewDetail, '/splist/viewdetail')
api.add_resource(DownLoadSP, '/splist/downloadsp')
if __name__ == '__main__':
    app.run()
