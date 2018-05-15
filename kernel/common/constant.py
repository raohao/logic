# -*- coding: utf-8 -*-

INSTITUTION = (
    ('Head', '总行'),
    ('Branch', '分行'),
)

HEAD_ORGANIZATION = (
    ('data', '数据中心'),
    ('software', '软件中心'),
)

BRANCH_ORGANIZATION = (
    ('beijing', '北京分行'),
    ('shanghai', '上海分行'),
    ('tianjin', '天津分行'),
    ('chongqing', '重庆分行'),
)

ADMIN_POWERLEVEL = (
    ('sys_admin', '系统管理员'),
    ('head_admin', '总行管理员'),
    ('branch_admin', '分行管理员'),
)

HEAD_POWERLEVEL = (
    ('team_manager', '团队管理员'),
    ('guard_judge', '值班审核员'),
    ('claims_man', '事件调查员'),
    ('guard_manager', '值班管理员'),
    ('temporary', '临时操作员'),
    ('auditor', '审计检查员'),
)

BRANCH_POWERLEVEL = (
    ('branch_assist', '分行协理员'),
    ('dept_manager', '部门管理员'),
    ('dept_operator', '部门操作员'),
    ('auditor', '审计检查员'),
)

RECEIPT_STATUS = (
    ('new', '新建'),
    ('process', '处理中'),
    ('done', '完成'),
    ('close', '关闭'),
)

RECEIPT_RANK = (
    ('1', '一级安全事件'),
    ('2', '二级安全事件'),
    ('3', '三级安全事件'),
)

ARTICLE_STATUS = (
    ('draft', '草稿'),
    ('published', '发布'),
)

ALARM_CHECK_SOLUTION = (
    ('1', '继续观察'),
    ('2', '提交阻断服务请求'),
    ('3', '其他处理方式'),
)

GUARD_LEVEL = (
    ('normal', '平时'),
    ('prepare', '备战'),
    ('wartime', '战时'),
)
