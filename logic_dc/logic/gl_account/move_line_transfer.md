# 凭证转换

## 流程
触发点位置： 总账 - 配置 - 总账设置 - 凭证转换
1. 通过选取 公司、期间、凭证分组规则 点击转换（transform)
2. 转换逻辑
    1. 通过自动化任务启动转换任务(transform_by_corn),参数当前界面记录ID.
    2. 查询符合条件的凭证记录,如果没有则创建一条自动凭证转换记录,信息为'在当前规则下没有需要处理的记录';
       如果有记录,获取以(分类账、期间、公司、[科目、摘要、制单人、日期])分组的种类,通过这些分组绑定对应的凭证记录,
       更新符合条件的所有明细凭证的状态为已登账、登账人为当前操作员工。
    3. 启动generate_gl_move_transform方法创建总账凭证,参数为(总账分组数据记录集合、凭证分组规则)
    4. generate_gl_move_transform方法首先循环'总账分组数据记录集合',分别创建'总账凭证'记录。
       将创建好的总账凭证ID,回写到明细凭证记录中，如果关联科目页签有相关的记录，对每一条关联科目记录进行总账凭证记录汇总
       generate_gl_move_form_relate_accounts,

