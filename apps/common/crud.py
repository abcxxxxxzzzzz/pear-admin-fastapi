


async def get_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    return model.query.filter_by(id=id).first()


async def delete_one_by_id(model: db.Model, id):
    """
    :param model: 模型类
    :param id: id
    :return: 返回单个查询结果
    """
    r = model.query.filter_by(id=id).delete()
    db.session.commit()
    return r


# 启动状态
async def enable_status(model: db.Model, id):
    enable = 1
    role = model.query.filter_by(id=id).update({"enable": enable})
    if role:
        db.session.commit()
        return True
    return False


# 停用状态
async def disable_status(model: db.Model, id):
    enable = 0
    role = model.query.filter_by(id=id).update({"enable": enable})
    if role:
        db.session.commit()
        return True
    return False
