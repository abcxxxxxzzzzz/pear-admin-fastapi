from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from apps.api.admin.utils.AddToSession import add_auth_session
from apps.api.admin.models import Power,Role
from apps.depends.mem_session import mem_session
from apps.depends.manager import manager
from apps.core.config import KEY_EXPIRES
from apps.common.reponse import APIResponse
from werkzeug.security import generate_password_hash
from fastapi_sqlalchemy import db
from sqlalchemy import and_
import logging
from typing import List






class Service:

    
    # list
    async def list(self):
        query = db.session.query(Power).all()
        return jsonable_encoder(query)


    async def select_parent(self):
        power_dict = await self.list()
        power_dict.append({"id": 0, "title": "顶级权限", "parent_id": -1})
        return power_dict

    async def add(self, item):
        item = jsonable_encoder(item, exclude_none=True)
        query = Power(**item)
        db.session.add(query)
        db.session.commit()
        return jsonable_encoder(query)
    
    # 删除
    async def delete_by_id(self, id):
        try:
            query = db.session.query(Power).filter_by(id=id).first()
            if not query:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败,也许此权限不存在')
            
            role_id_list = []
            roles = query.role
            for role in roles:
                role_id_list.append(role.id)
            roles = db.session.query(Role).filter(Role.id.in_(role_id_list)).all()
            for p in roles:
                query.role.remove(p)
                
            db.session.query(Power).filter_by(id=id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败,请稍后再试')
        
    # 批量删除
    async def batch_remove(self, ids):
        for id in ids:
            await self.delete_by_id(id)

    # enable status
    async def enable_status(self,id):
        enable = 1
        query = db.session.query(Power).filter_by(id=id).update({"enable": enable})
        if not query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='启动失败,也许此用户不存在')
        db.session.commit()
        
    

    # disable status
    async def disable_status(self, id):
        enable = 0
        query = db.session.query(Power).filter_by(id=id).update({"enable": enable})
        if not query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='启动失败,也许此用户不存在')
        db.session.commit()


    async def get_by_id(self, id):
        return db.session.query(Power).filter_by(id=id).first()


    async def update(self, item):
        try:
            data = jsonable_encoder(item)
            id = data.pop('id')
            power = db.session.query(Power).filter_by(id=id).update(data)
            db.session.commit()
            return power
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新权限失败')


Service = Service()