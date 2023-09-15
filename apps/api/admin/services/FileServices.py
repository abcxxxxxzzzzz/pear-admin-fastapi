from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException,status
from apps.api.admin.models import Photo
from apps.core.config import UPLOAD_PATH
from fastapi_sqlalchemy import db
from sqlalchemy import desc
import logging
import os,time


base_url = UPLOAD_PATH



class Service:

    
    # list
    async def list(self, page, limit):
        obj = db.session.query(Photo)
        query = obj.order_by(desc(Photo.create_time)).offset((page-1)*limit).limit(limit).all()
        count = obj.count()

        query = jsonable_encoder(query)
        return query, count


    @staticmethod
    async def upload_one(photo, mime):
        try:
            filename = "".join(photo.filename.split(".")[:-1]) + "_" + str(int(time.time())) + "." + mime.split("/")[-1]
            with open(base_url + filename, "wb") as f:
                f.write(photo.file.read())
            file_url = "/" + UPLOAD_PATH + filename

            size = os.path.getsize(base_url + filename)
            photo = Photo(name=filename, href=file_url, mime=mime, size=size)
            db.session.add(photo)
            db.session.commit()
            return file_url
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='添加失败')

    @staticmethod
    async def delete_photo_by_id(id):
        try:
            photo_name = db.session.query(Photo).filter_by(id=id).first().name
            db.session.query(Photo).filter_by(id=id).delete()
            db.session.commit()
            os.remove(base_url + photo_name)
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败')


    @staticmethod
    async def batchRemove(ids):
        try:
            obj = db.session.query(Photo).filter(Photo.id.in_(ids)).all()
            photo_name = list(map(lambda x:x.name, obj))
            db.session.query(Photo).filter(Photo.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
            for p in photo_name:
                os.remove(base_url + p)
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='批量删除失败')
        
        


Service = Service()