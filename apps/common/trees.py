from fastapi.encoders import jsonable_encoder

def make_menu_tree(current_user):
    role = current_user.role
    power0 = []
    power1 = []
    for i in role:
        if i.enable == 0:
            continue
        for p in i.power:
            if p.enable == 0:
                continue
            if int(p.type) == 0:
                power0.append(p)
            else:
                power1.append(p)

    # print(power0)
    # print(power1)
    # print(jsonable_encoder(power0))
    # print(jsonable_encoder(power1)) 
    # return []
    # power_schema = PowerSchema(many=True)  # 用已继承ma.ModelSchema类的自定制类生成序列化类
    # power0_dict = power_schema.dump(power0)  # 生成可序列化对象
    # power1_dict = power_schema.dump(power1)  # 生成可序列化对象

    power0_dict = jsonable_encoder(power0)
    power1_dict = jsonable_encoder(power1)
    power0_dict = sorted(power0_dict, key=lambda i: i['sort'])
    power1_dict = sorted(power1_dict, key=lambda i: i['sort'])
    

    menu = []



    for p0 in power0_dict:
        for p1 in power1_dict:
            if p0.get('id') == int(p1.get('parent_id')):
                if p0.get("children") is None:
                    p0['children'] = []
                p0['children'].append(p1)
        menu.append(p0)

    return menu