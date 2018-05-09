# -*- coding: utf-8 -*-
from django.db import models
# Create your models here.


class Workflow(models.Model):
    """
    工作流
    """
    workflow_id = models.CharField('流程号', primary_key=True, max_length=50)
    workflow_name = models.CharField('名称', max_length=50, null=True, blank=True, default='')
    description = models.CharField('描述', max_length=500, null=True, blank=True, default='')
    flow_chart = models.CharField('流程图路径', max_length=200, null=True, blank=True, default='')
    notice_type = models.CharField('通知方式',  max_length=200, null=True, blank=True, default='')
    permission_check = models.BooleanField('权限校验', default=1, help_text='只允许工单的关联人查看工单')

    # 限制周期({'period':24} 24小时), 限制次数({'count':1}在限制周期内只允许提交1次), 限制级别({'level':1} 针对(1特定用户 2全局)限制周期限制次数)
    # 允许特定人员提交({'allow_person':'zhangsan'}只允许张三提交工单,{'allow_dept':1}只允许部门id的用户提交工单，{'allow_role':1}只允许角色id为1的用户提交工单)
    limit_expression = models.CharField('限制表达式', max_length=100, default='', null=True, blank=True)
    form_desplay = models.CharField('展现表单字段', max_length=10000, default='[]', null=True, blank=True,
                                    help_text='json格式，用于用户只有查看权限时显示哪些字段,field_key的list')
    default_notice_to = models.CharField('默认通知人', max_length=50, default='',
                                         null=True, blank=True, help_text='表单创建及结束时会发送相应通知信息')
    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'workflow'
        verbose_name = '工作流'
        verbose_name_plural = '工作流'


class FlowState(models.Model):
    """
    状态记录, 变量支持通过脚本获取
    """
    name = models.CharField('名称', max_length=50)
    workflow_id = models.IntegerField('工作流')
    sub_workflow_id = models.IntegerField('子工作流id(如果需要在此状态启用子工单的话)', default=0, blank=True)
    is_hidden = models.BooleanField('是否隐藏', default=0, help_text='设置为True时,工单步骤中不显示此状态(当前处于此状态时除外)')
    order_id = models.IntegerField('状态顺序', default=0, help_text='用于工单步骤接口时，step上状态的顺序(因为存在网状情况，所以需要认为设定顺序),值越小越靠前')
    type_id = models.IntegerField('状态类型id', default=0, help_text='见service.constant_service中定义')

    participant_type_id = models.IntegerField('参与者类型id', default=1, blank=True, help_text='见service.constant_service中定义')
    participant = models.CharField('参与者', default='', blank=True, max_length=100, help_text='可以为username\多个username(以,隔开)\部门id\角色id\变量id等')

    distribute_type_id = models.IntegerField('分配方式', default=1, help_text='见service.constant_service中定义')  # 1主动接单, 2直接处理,3.随机分配,4.全部处理(要求所有参与人都要处理一遍)
    state_field_str = models.TextField('表单字段', default='{}', help_text='json格式字典存储,包括读写属性1：只读，2：必填，3：可选. 示例：{"created_at":1,"title":2, "sn":1}')  # json格式存储,包括读写属性1：只读，2：必填，3：可选，4：不显示, 字典的字典
    label = models.CharField('状态标签', max_length=1000, default='{}',
                             help_text='json格式，由调用方根据实际定制需求自行确定,如状态下需要显示哪些前端组件:{"components":[{"AppList":1, "ProjectList":7}]}')
    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'flow_state'
        verbose_name = '工作流状态'
        verbose_name_plural = '工作流状态'


class FlowTransition(models.Model):
    """
    工作流流转，定时器，条件(允许跳过)， 条件流转与定时器不可同时存在
    """
    name = models.CharField('操作', max_length=50)
    workflow_id = models.IntegerField('工作流id')
    transition_type_id = models.IntegerField('流转类型', default=1, help_text='见service.constant_service中定义') #常规流转，定时器流转，选择定时器后需要设置定时器时间，同时不得设置条件，不得设置弹窗信息
    source_state_id = models.IntegerField('源状态id')
    destination_state_id = models.IntegerField('目的状态id')
    field_require_check = models.BooleanField('是否校验必填项', default=True, help_text='默认在用户点击操作的时候需要校验工单表单的必填项,如果设置为否则不检查。用于如"退回"属性的操作，不需要填写表单内容')
    alert_enable = models.BooleanField('点击弹窗提示', default=False)
    alert_text = models.CharField('弹窗内容', max_length=100, default='', blank=True)
    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'flow_transition'
        verbose_name = '工作流流转'
        verbose_name_plural = '工作流流转'


class CustomFlowField(models.Model):
    """自定义字段, 设定某个工作流有哪些自定义字段"""
    workflow_id = models.IntegerField('工作流id')
    field_type_id = models.IntegerField('类型', help_text='见service.constant_service中定义')
    field_key = models.CharField('字段标识', max_length=50)
    field_name = models.CharField('字段名称', max_length=50)
    order_id = models.IntegerField('排序', default=0)
    default_value = models.CharField('默认值', null=True, blank=True, max_length=100)
    description = models.CharField('描述', max_length=100, blank=True, default='')
    field_template = models.TextField('模板', default='', blank=True, help_text='文本域字段支持配置内容模板')
    boolean_field_display = models.CharField('布尔类型显示名', max_length=100, null=True, blank=True,
                                             help_text='当为布尔类型时候，可以支持自定义显示形式。{1:"是",0:"否"}或{1:"需要",0:"不需要"}')
    field_choice = models.CharField('radio选项', max_length=1000, default='[]', blank=True,
                                    help_text='radio,checkbox,select,multiselect类型可供选择的选项，格式为json如:{1:"中国",2:"美国"}')

    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'custom_flow_field'
        verbose_name = '工作流自定义字段'
        verbose_name_plural = '工作流自定义字段'


class WorkflowScript(models.Model):
    """
    流程中执行的脚本
    """
    name = models.CharField('名称', max_length=50)
    saved_name = models.CharField('存储的文件名', max_length=50)
    description = models.CharField('描述', max_length=100, null=True, blank=True)
    is_active = models.BooleanField('可用', default=True)

    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'work_flow_script'
        verbose_name = '工作流脚本'
        verbose_name_plural = '工作流脚本'


class CustomFlowNotice(models.Model):
    """
    自定义通知方式，初始化邮件方式
    """
    name = models.CharField('名称', max_length=50)
    description = models.CharField('描述', max_length=100, null=True, blank=True)
    script = models.FileField('通知脚本', upload_to='notice_script', null=True, blank=True)
    title_template = models.CharField('标题模板', max_length=50, null=True, blank=True)  # 如果为空就按照默认模板生成
    content_template = models.CharField('内容模板', max_length=1000, null=True, blank=True)  # 如果为空就按照默认模板生成

    create_user_id = models.CharField('创建人', max_length=20, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    is_deleted = models.BooleanField('已删除', default=False)

    class Meta:
        db_table = 'custom_flow_notice'
        verbose_name = '自定义通知脚本'
        verbose_name_plural = '自定义通知脚本'
