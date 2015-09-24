## gen-wgtu

**gen-wgtu**是一个用于生成HTML5+移动App差量资源升级包的命令行工具。该工具通过对比两个完整的升级资源包，生成符合要求的.wgtu差量包。HTML5+开发移动App详细介绍请看[这里](http://ask.dcloud.net.cn/docs/#http://ask.dcloud.net.cn/article/89)。

## 命令格式
```
python genwgtu.py <old.wgt>  <new.wgt>  [ -o out.wgtu]
```
## 生成步骤
1. 生成两个不同版本的资源包如 app-1.0.0.wgt和app-1.1.0.wgt（官方资料：[资源包生成](http://ask.dcloud.net.cn/docs/#http://ask.dcloud.net.cn/article/182)）
2. 执行gen-wgtu生成差量资源包，如下生成的差量资源包文件名为：update.wgtu
```
python genwgtu.py app-1.0.0.wgt  app-1.1.0.wgt -o update.wgtu
```

## 环境要求
 python2.7测试通过，其他版本的python未测试。

## 相关资源
*  [资源包生成(wgt)](http://ask.dcloud.net.cn/docs/#http://ask.dcloud.net.cn/article/182)
* [资源差量升级包(wgtu)及包文件格式说明](http://ask.dcloud.net.cn/docs/#http://ask.dcloud.net.cn/article/199) 
