# 资产面板上的转移

## 简介
资产转移 - 存在于资产面板上的更多下拉显示页签，点击弹出相关的转移信息维护界面，
通过维护新科室和核算的成本中心，使得资产从某种意义上达到资产的资金核算转移的实际业务。

## 代码逻辑分析

1. 首先维护好相关的信息后，点击确认走do_batch_transfer方法:
```text
    do_batch_transfer:对维护的相关行信息进行操作(asset_batch_transfer)，当操作完成后返回资产界面，
    这里如果是单条操作，返回对应资产的form页面；如果是批量操作，返回对应这批资产的tree页面。
    
    asset_batch_transfer:这个方法是资产转移的主要方法，该方法用于创建资产转移历史记录，创建资产转移历史记录的分配页信息(每个资产每次调整会生成两条记录 1-调整前的 2-调整后的)
    创建完成后对应修改资产的相关信息 - 新使用科室、责任人、新安装位置，而后执行资产转移后相关操作(after_asset_transfer)。
    
    after_asset_transfer:更新了一下资产分配行上的费用成本中心。
```

# 资产转移申请的转移操作

## 代码逻辑分析
```text
    1. 维护界面后点击提交按钮(action_submitted)
    2. action_submitted 仅仅修改了当前转移操作单的状态为submitted，启用审批流。
    3. 审批流执行完成后会执行最后的操作(complete_approve)
    4. complete_approve 执行了action_approve方法
    5. action_approve 在hrp_asset_funding_source模块中继承重写
        1. 修改当前单据状态为approved
        2. 循环需要处理的转移记录单的资产：
            更新对应资产信息(使用科室、管理位置、责任人)
            如果转移单据的申请课室上维护的有成本中心信息:
                1. 资产分配上的费用成本中心都需要被修改成当前修改的 成本中心
                2. 创建资产转移历史记录
                3. 资产转移历史记录 中创建每一个资产分配行创建相关的资产分配行历史记录(调整前)
                4. 创建资产历史记录
                5. 如果当前资产 为低值资产、已费用 未勾选、资产类别上的启用库存管理 未勾选、资产状态为开饭:
                    1.创建资产事物处理记录
                    2.调用generate_transfer_distribute_line方法创建资产转移事物处理历史记录的分配行
                    3.generate_transfer_distribute_line 通过get_asset_distribution_template获取需要创建的参数集合后 直接创建
                    4.资产的 已费用 修改为True 下次这个方法就进不来了
                    5.把创建的(资产事物记录,当前转移单据id，转移历史记录id)加入transaction_ids列表中
        3. 如果有符合的transaction_ids，将transaction_ids当做args参数直接传入hrp_cron_job执行创建转移凭证的方法create_asset_transfer_account_move
        4. create_asset_transfer_account_move 
            1.检查资产是否可以生成凭证(资产类别上的是否创建凭证分录是否勾选)
            2.如果勾选 则创建资产转移凭证(create_one_asset_transfer_account_move)
                1.针对之前创建完成的资产转移事务历史记录中每一条分配行创建凭证记录
                2.借方的凭证行，根据事务处理历史记录中对应的转移记录分配上的数据项逐条添加
                3.进行数据特征对比 合并借方凭证(这个地方可以优化 - 提前对数据进行分组 for 套 for 影响效率，不过分配行没多少倒是没什么大的影响，有时间可以改一下)
                4.贷方就直接将一条凭证行数据插入创建序列中  
                5.凭证头创建数据获取
                6.判断资产转移的会计分类中是否维护了可创建凭证分录的配置选项
                7.如果维护创建凭证头记录 回写资产事务记录中那条转移记录 已创建凭证的标识
                8.资产分配行成本中心回写(与上面的逻辑有重复)
                9.通过资产分配行循环对应创建上面转移记录中 调整后 的资产分配行变动历史记录
```

