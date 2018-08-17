# 后台任务

## 目前后台任务分为三种:

> 自动化任务
```python
# - 获取cron_job对象
hrp_cron_job_obj = self.env['hrp.cron.job']
# - 定义延时执行的时间
cron_job_date = fields.Datetime.to_string(datetime.now() + timedelta(seconds=30))
# - 直接执行不走cron_job的方法(前期测试使用)
# self.create_asset_acceptance_account_move(args)
# - 延时凭证生成的方法 必须有需要生成的数据项 这里args如果没有数据 也同样会被封装成 元组|所以需要做一个判断
if len(args) > 0 and len(args[0]) > 0:
    hrp_cron_job_obj.run_by_cron(_("Create Asset Receiving Account Move"),# 自动化任务名称
                                 'hrp.asset.receiving.application',# 自动化任务需要调用的方法所在model
                                 'create_asset_acceptance_account_move',# 方法名
                                 [args],# 参数
                                 date_created=cron_job_date)# 延时时间
```

分析一下方法：
```text
def run_by_cron(self, name, model, function, args, priority=10, user_id=False, date_created=False):
    """
    name - 自动化任务名称
    model - 执行方法模型
    function - 执行的方法名称
    args - 参数
    priority - 优先级
    user_id - 执行用户
    date_created - 开始执行时间
    """
    # - 如果没有配置时间 默认立即创建启动执行
    if not date_created:
        date_created = fields.Datetime.now()
    # - 如果没有执行用户 默认当前登录用户
    if not user_id:
        user_id = self.env.user.id
    # - 解析参数 这里的参数最好的格式是一个列表传入
    args = [repr(arg) for arg in args]
    # - 创建一个自动化任务
    self.create({
        'name': name,
        'model': model,
        'function': function,
        'args': '(%s,)' % (', '.join(args)),
        'date_created': date_created,
        'user_id': user_id,
        'priority': priority,
    })
    
# 在自动化任务的create方法中，直接创建了ir.cron记录:
 @api.model
    def create(self, vals):
        # 创建ir_cron
        ir_cron_obj = self.env['ir.cron']
        res = super(HrpCronJob, self).create(vals)
        ir_cron = {
            'name': vals['name'],
            'active': True,
            'user_id': vals['user_id'],
            'priority': vals['priority'],
            'interval_type': 'minutes',
            'nextcall': vals['date_created'],
            'numbercall': 1,
            'doall': True,
            'model': vals['model'],
            'function': vals['function'],
            'args': vals['args'],
            'hrp_cron_job_id': res.id,
        }
        ir_cron_obj.create(ir_cron)
        return res
   
```

> 队列任务

> 并发管理器
