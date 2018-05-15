# Generated by Django 2.0.4 on 2018-05-15 06:06

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlarmCheck',
            fields=[
                ('check_id', models.CharField(max_length=254, primary_key=True, serialize=False, verbose_name='单号')),
                ('title', models.CharField(blank=True, default='', max_length=50, verbose_name='标题')),
                ('status', models.CharField(choices=[('new', '新建'), ('process', '处理中'), ('done', '完成'), ('close', '关闭')], default='new', max_length=10, verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='发送时间')),
                ('receive_time', models.DateTimeField(blank=True, null=True, verbose_name='接收时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('close_time', models.DateTimeField(blank=True, null=True, verbose_name='关闭时间')),
                ('rank', models.CharField(choices=[('1', '一级安全事件'), ('2', '二级安全事件'), ('3', '三级安全事件')], default='3', max_length=10, verbose_name='等级')),
                ('describe', models.TextField(blank=True, max_length=3000, null=True, verbose_name='描述')),
                ('influence', models.BooleanField(default=False, verbose_name='影响')),
                ('reason', models.TextField(blank=True, max_length=3000, null=True, verbose_name='原因')),
                ('plan', models.TextField(blank=True, max_length=5000, null=True, verbose_name='解决方案')),
                ('qradar_id', models.CharField(blank=True, max_length=32, null=True, verbose_name='Qradar单号')),
                ('remedy_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Remedy单号')),
                ('classification', models.IntegerField(blank=True, null=True, verbose_name='攻击类型')),
                ('source_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='源IP')),
                ('destination_ip', models.TextField(blank=True, max_length=255, null=True, verbose_name='源目的IP')),
                ('source_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='源地址')),
                ('destination_address', models.CharField(blank=True, max_length=255, null=True, verbose_name='目的地址')),
                ('stream', models.IntegerField(blank=True, null=True, verbose_name='流数目')),
                ('start_from', models.CharField(blank=True, max_length=255, null=True, verbose_name='开始时间')),
                ('sustain', models.CharField(blank=True, max_length=255, null=True, verbose_name='持续时间')),
                ('app', models.CharField(blank=True, max_length=255, null=True, verbose_name='攻击应用')),
                ('solution', models.IntegerField(choices=[('1', '继续观察'), ('2', '提交阻断服务请求'), ('3', '其他处理方式')], default='1', verbose_name='解决方式')),
                ('receive_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.HeadUser', verbose_name='受理人工号')),
            ],
            options={
                'verbose_name': '监控告警单',
                'verbose_name_plural': '监控告警单',
                'db_table': 'alarm_check',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('evaluation_id', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='单号')),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True, verbose_name='时间')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='分数')),
                ('reason', models.CharField(blank=True, max_length=255, null=True, verbose_name='说明')),
                ('candidate_user_id', models.ManyToManyField(related_name='evaluation_candidate_user', to='account.HeadUser', verbose_name='被评人')),
                ('judge_user_id', models.ManyToManyField(related_name='evaluation_judge_user', to='account.HeadUser', verbose_name='评价人')),
            ],
            options={
                'verbose_name': '员工评价单',
                'verbose_name_plural': '员工评价单',
                'db_table': 'evaluation',
            },
        ),
        migrations.CreateModel(
            name='EventCheck',
            fields=[
                ('check_id', models.CharField(max_length=254, primary_key=True, serialize=False, verbose_name='单号')),
                ('title', models.CharField(blank=True, default='', max_length=50, verbose_name='标题')),
                ('status', models.CharField(choices=[('new', '新建'), ('process', '处理中'), ('done', '完成'), ('close', '关闭')], default='new', max_length=10, verbose_name='状态')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='发送时间')),
                ('receive_time', models.DateTimeField(blank=True, null=True, verbose_name='接收时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('close_time', models.DateTimeField(blank=True, null=True, verbose_name='关闭时间')),
                ('rank', models.CharField(choices=[('1', '一级安全事件'), ('2', '二级安全事件'), ('3', '三级安全事件')], default='3', max_length=10, verbose_name='等级')),
                ('describe', models.TextField(blank=True, max_length=3000, null=True, verbose_name='描述')),
                ('influence', models.BooleanField(default=False, verbose_name='影响')),
                ('reason', models.TextField(blank=True, max_length=3000, null=True, verbose_name='原因')),
                ('plan', models.TextField(blank=True, max_length=5000, null=True, verbose_name='解决方案')),
                ('history', models.CharField(blank=True, max_length=255, null=True, verbose_name='历史记录')),
                ('file', models.FileField(blank=True, max_length=255, null=True, upload_to='', verbose_name='附件')),
                ('alarm_check_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_alarm_check', to='guard.AlarmCheck', verbose_name='关联告警单号')),
                ('create_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_create_user', to='account.HeadUser', verbose_name='建单人')),
                ('receive_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_receive_user', to='account.HeadUser', verbose_name='受理人')),
                ('transmit_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event_transmit_user', to='account.HeadUser', verbose_name='转派人')),
            ],
            options={
                'verbose_name': '威胁事件单',
                'verbose_name_plural': '威胁事件单',
                'db_table': 'event_check',
            },
        ),
        migrations.CreateModel(
            name='GuardPlan',
            fields=[
                ('guard_plan_time', models.DateField(default=django.utils.timezone.now, primary_key=True, serialize=False, verbose_name='值班日期')),
                ('product_judge', models.FloatField(default=0, verbose_name='一线值班进度')),
                ('second_judge', models.FloatField(default=100, verbose_name='二线值班进度')),
                ('third_judge', models.FloatField(default=100, verbose_name='三线值班进度')),
                ('report', models.FilePathField(blank=True, max_length=255, null=True, verbose_name='日报')),
                ('product_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guard_product_user', to='account.HeadUser', verbose_name='一线值班员')),
                ('second_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guard_second_user', to='account.HeadUser', verbose_name='二线值班员')),
                ('third_user_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='guard_third_user', to='account.HeadUser', verbose_name='三线值班员')),
            ],
            options={
                'verbose_name': '值班安排表',
                'verbose_name_plural': '值班安排表',
                'db_table': 'guard_plan',
            },
        ),
    ]
