# python-lammda-workflow
> 在aws 实例上部署程序，通过aws云函数lammda获取返回参数，再通过手机快捷指令调用lammda函数得到想要的值。

### `app.py` 代码

+ 利用`Flask`框架实现接口;
+ 查询`v2ray`端口;
+ 修改`v2ray`端口;
+ 对返回结果进行预处理;
+ 对`Token`进行认证;


### `lammda_hander.py` AWS自带的云函数

+ 调用`app.py`程序;
+ 对`app.py`返回结果状态进行预处理;
+ 构建`Flask` 应用程序的`URL`;
+ 提取`vmess`地址;
+ 云函数配置选项会生成一个`url`链接的触发器:`https://XXXXXX.execute-api.us-east-1.amazonaws.com/default/lammda`;

### 苹果/MAC的`Workflow`
+ 配置`workflow`;
+ 从`url`的内容获取词典；
+ 将`词典`添加到`txt`;
+ 在`txt`中获取`vmess_url`的`值`;
+ URL`编码``词典值`;
+ 文本：shadowrocket://add/`词典值`
+ 打开`文本`;

### 许可证

MIT License