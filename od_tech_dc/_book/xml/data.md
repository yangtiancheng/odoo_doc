# xml文件知识

## data文件初始化中的知识点
### 1.结构
```xml
<openerp>
    <data>
        <record>
            <filed></filed>
        </record>
    </data>
    <data>...</data>
    ...
</openerp>
```

### 属性
> noupdate
```text
data块有noupdate属性，当noupdate="1"时，该data块只会在安装的时候加载，之后的每次模块升级都不会再执行数据重写初始化。
默认noupdate为False。其中当初始化的record记录被删除 升级时依旧不会被重新装载。
```

> forcecreate
```text
data块的record有forcecreate属性，该属性的意义实际上是，如果forcecreate="1",那么data块的noupdate="1",
当record记录被删除时，本不应该被重新加载，但如果使用了forcecreate属性，记录会在更新的时候被重新加载上去。
```
<p style="color:red">如果删除了noupdate块中data文件初始化的数据记录，然后你重新更新它不重置，你可以看一下ir_module_data表，
对应的data块外部id记录中，noupdate=True,把那条记录删除再升级就出来了。</p>

## 普通
> 自动递增 递增间隔 最开始的值
<field name="line_number" required="1"  options="{'line_number':1,'interval':10,'initial':10}"/>

## Domain 
- XML定义的domain会覆盖字段定义的domain
