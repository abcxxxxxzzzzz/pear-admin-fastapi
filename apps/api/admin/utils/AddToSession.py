from apps.depends.mem_session import mem_session




# 授权路由存入session
def add_auth_session(current_user):
    role = current_user.role
    user_power = []
    for i in role:
        if i.enable == 0:
            continue
        for p in i.power:
            if p.enable == 0:
                continue
            user_power.append(p.code)
    mem_session[current_user.username] = user_power