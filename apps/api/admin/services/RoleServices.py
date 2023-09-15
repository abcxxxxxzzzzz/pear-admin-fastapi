from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from apps.api.admin.utils.AddToSession import add_auth_session
from apps.api.admin.models import User,Role,Power
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

    async def get_list_data(self, params, filters):
        sql = db.session.query(Role).filter(and_(*[getattr(Role, k).like(v) for k, v in filters.items()]))
        query = sql.order_by(Role.id.desc()).offset((params.page-1)*params.limit).limit(params.limit).all()
        count = sql.count()
        return query, count
    

    async def list(self, params, filters):
        query, count = await self.get_list_data(params, filters)
        query = jsonable_encoder(query)
        return query, count
    

    async def add(self, item):
        exists = await self.get_by_name(item.roleName)
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='此角色已经存在') 

        
        newItem = {}
        newItem['name'] = item.roleName
        newItem['code'] = item.roleCode
        newItem['enable'] = item.enable
        newItem['sort'] = item.sort
        newItem['details'] = item.details

        query = Role(**newItem)
        db.session.add(query)
        db.session.commit()
        return jsonable_encoder(query)
    
    # 更新
    async def update(self, item):
        try:

            data = {
                "code": item.roleCode,
                "name": item.roleName,
                "sort": item.sort,
                "enable": item.enable,
                "details": item.details
            }

            query = db.session.query(Role).filter_by(id=item.roleId).update(data)
            db.session.commit()
            return query
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新角色失败')


    
    # 删除
    async def delete_by_id(self, id):
        try:
            role = db.session.query(Role).filter_by(id=id).first()
            # 删除该角色的权限
            power_id_list = []
            for p in role.power:
                power_id_list.append(p.id)

            powers = db.session.query(Power).filter(Power.id.in_(power_id_list)).all()
            for p in powers:
                role.power.remove(p)
            user_id_list = []
            for u in role.user:
                user_id_list.append(u.id)
            users = db.session.query(User).filter(User.id.in_(user_id_list)).all()
            for u in users:
                role.user.remove(u)
            r = db.session.query(Role).filter_by(id=id).delete()
            db.session.commit()
            return r
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败,请稍后再试')
            
    
    # 批量删除
    async def batch_remove(self, ids):
        for id in ids:
            await self.delete_by_id(id)
        


    # 获取角色的权限
    async def get_role_power(self, id):
        role = db.session.query(Role).filter_by(id=id).first()
        check_powers = role.power
        check_powers_list = []
        for cp in check_powers:
            check_powers_list.append(cp.id)
        powers = db.session.query(Power).all()
        # power_schema = PowerSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
        # output = power_schema.dump(powers)  # 生成可序列化对象
        output = jsonable_encoder(powers)
        for i in output:
            if int(i.get("id")) in check_powers_list:
                i["checkArr"] = "1"
            else:
                i["checkArr"] = "0"
        return output

    # 更新角色权限
    async def update_role_power(self,id, power_list):
        try:
            role = db.session.query(Role).filter_by(id=id).first()
            power_id_list = []
            for p in role.power:
                power_id_list.append(p.id)

            powers = db.session.query(Power).filter(Power.id.in_(power_id_list)).all()
            for p in powers:
                role.power.remove(p)
            powers = db.session.query(Power).filter(Power.id.in_(power_list)).all()
            for p in powers:
                role.power.append(p)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='更新角色权限失败')

    # 启动
    async def enable_status(self,id):
        enable = 1
        user = db.session.query(Role).filter_by(id=id).update({"enable": enable})
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='启动失败,也许此角色不存在')
        db.session.commit()
        
        


    # 停用
    async def disable_status(self, id):
        enable = 0
        user = db.session.query(Role).filter_by(id=id).update({"enable": enable})
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='停用失败,也许此角色不存在')
        db.session.commit()


    async def get_by_name(self, name):
        return db.session.query(Role).filter_by(name=name).first()
    

    async def get_by_id(elf, id):
        return db.session.query(Role).filter_by(id=id).first()

    # 判断用户是否存在
    async def is_exists(self,name):
        res = db.session.query(Role).filter_by(name=name).count()
        return bool(res)


Service = Service()