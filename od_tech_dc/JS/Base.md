# JS - 基础

1. 定义ir.action.client 带tag 与绑定的菜单对象
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<openerp>
    <data>
        <record id="widget_menu_action" model="ir.actions.client">
            <field name="name">Widget Menu Action</field>
            <field name="tag">tps_widget.widget_menu</field>
        </record>
        <menuitem id="tps_widget_top_menu"
                  name="Widget Top Menu"
                  sequence="10"/>
        <menuitem id="tps_widget_sub_menu"
                  name="Widget Sub Menu"
                  parent="tps_widget_top_menu"
                  sequence="10"/>
        <menuitem id="tps_widget_func_menu"
                  name="Widget Func Menu"
                  parent="tps_widget_sub_menu"
                  action="widget_menu_action"
                  sequence="10"/>
    </data>
</openerp>
```
2. 定义一个extend_widget.js文件
   js文件包含content：
```javascript
openerp.tps_widget = function (instance, local) {
    var _t = instance.web._t,
        _lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.MyWidget = instance.Widget.extend({
        start: function () {
            console.log("load Mywidget.")
        }
    });
    //第一个参数是tag 第二个参数是widget的完整地址
    instance.web.client_actions.add('tps_widget.widget_menu', 'instance.MyWidget');
}
```
3. 引入js文件，定义一个xml
   views/xxx_template.xml
```xml
<?xml version="1.0" encoding="UTF-8" ?>
<openerp>
    <data>
        <template id="assets_backend" name="tps_widget" inherit_id="web.assets_backend">
            <xpath expr="." position="inside">
                <script type="text/javascript" src="/tps_widget/static/js/extend_widget.js"></script>
            </xpath>
        </template>
    </data>
</openerp>
```

4. 注意这里暂时没有py文件，但是xml文件需要在__openerp__.py中注册[定义菜单的 和 引入js的]。

------------------------------
this
this.$el
ob.appendTo(this.$el)
this.getParent().$el
this.getChildren()[0].$el


