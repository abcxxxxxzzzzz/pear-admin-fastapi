from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from datetime import timedelta
from apps.api.admin.utils.AddToSession import add_auth_session
from apps.api.admin.models import User,Role
from apps.api.admin.services.AdminLogServices import login_log
from apps.depends.mem_session import mem_session
from apps.depends.manager import manager
from apps.core.config import KEY_EXPIRES
from apps.common.reponse import APIResponse
from werkzeug.security import generate_password_hash
from fastapi_sqlalchemy import db
from sqlalchemy import and_
import logging




class Service:

    async def CheckLoginForm(self,request, username: str, password: str, captcha: str):

        s_code = await self.vaildate_captcha(captcha)
        if captcha != s_code:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='验证码错误')
        
        user = await self.get_by_name(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='不存在的用户') 
        
        if user.enable == 0:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='用户被暂停使用')
        
        if username != user.username or not user.validate_password(password): 
            login_log(request, username, uid=user.id, is_access=False)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='用户名或密码错误')
        
        
        add_auth_session(user)

        access_token = manager.create_access_token(
            data=dict(sub=username),
            expires=timedelta(hours=KEY_EXPIRES)
        )
        # response = JSONResponse(content={"code":1, "msg":"登录成功", "success":True})
        # response = JSONResponse(content={"msg":"登录成功"})
        
        response = APIResponse(msg='登录成功')
        manager.set_cookie(response, access_token)

        login_log(request, username, uid=user.id, is_access=True)
        return response




    async def get_list_data(self, params, filters):
        sql = db.session.query(User).filter(and_(*[getattr(User, k).like(v) for k, v in filters.items()]))
        query = sql.order_by(User.id.desc()).offset((params.page-1)*params.limit).limit(params.limit).all()
        count = sql.count()
        return query, count
    

    async def list(self, params, filters):
        query, count = await self.get_list_data(params, filters)
        query = jsonable_encoder(query, exclude=['password_hash'])
        return query, count
    

    async def add(self, item):
        """
        :添加用户
        """
        exists = await self.get_by_name(item.username)
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='此用户已经存在') 

        item = jsonable_encoder(item, exclude_none=True)
        item['password_hash'] = generate_password_hash(item['password'])
        item['role'] = db.session.query(Role).filter(Role.id.in_(item['role'])).all() if item['role'] else []
        item.pop('password')
  

        query = User(**item)
        db.session.add(query)
        db.session.commit()
        return jsonable_encoder(query)
    
    async def update(self, item):
        '''
            更新用户
        '''
        obj = await self.get_by_id(item.userId)
        obj.realname = item.realName
        obj.role = db.session.query(Role).filter(Role.id.in_(item.roleIds)).all() if item.roleIds else item.roleIds
        db.session.commit()



    # 验证验证码
    async def vaildate_captcha(self, captcha: str):
        """
        :param captcha: 查询验证码
        :return: 返回查询结果， True | False
        """
        return mem_session.pop(captcha, None)
    
    # 删除
    async def delete_by_id(self, id):
        try:
            user = db.session.query(User).filter_by(id=id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败,也许此用户不存在')
            
            roles_id = []
            for role in user.role:
                roles_id.append(role.id)
            roles = db.session.query(Role).filter(Role.id.in_(roles_id)).all()
            for r in roles:
                user.role.remove(r)

            db.session.query(User).filter_by(id=id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(str(e))
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='删除失败,请稍后再试')
            
    
    # 批量删除
    async def batch_remove(self, ids):
        try:
            # db.session.query(User).filter(User.id.in_(ids)).update({'role': []})
            users = db.session.query(User).filter(User.id.in_(ids)).all()
            for u in users:
                u.role = []
            db.session.query(User).filter(User.id.in_(ids)).delete(synchronize_session=False)
            db.session.commit()
        except Exception as e:
            logging.error(str(e))
            db.session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='批量删除失败,请稍后再试')
        


    # 启动
    async def enable_status(self,id):
        enable = 1
        user = db.session.query(User).filter_by(id=id).update({"enable": enable})
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='启动失败,也许此用户不存在')
        db.session.commit()
        
        


    # 停用
    async def disable_status(self, id):
        enable = 0
        user = db.session.query(User).filter_by(id=id).update({"enable": enable})
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='停用失败,也许此用户不存在')
        db.session.commit()


    async def get_by_name(self, username):
        return db.session.query(User).filter_by(username=username).first()
    

    async def get_by_id(elf, id):
        return db.session.query(User).filter_by(id=id).first()

    # 判断用户是否存在
    async def is_exists(elf,username):
        res = db.session.query(User).filter_by(username=username).count()
        return bool(res)


Service = Service()