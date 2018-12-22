# XSS_SCAN
### python selenium+chrome检测get参数xss demo

##### 环境(暂时win)：

* python2.7
* selenium 3.141.0
* chrome 71.0.3578.98
* chromediver 71.0.3578.80

> 这环境是真的难配，开始准备用phantoms发现无法监听到弹框消息，改用firefox因为python，firefox，selenium三者版本适配问题无法正常访问，坑很多。

##### 出现的问题：

* 多线程资源开销大

* 环境安装复杂

* POST数据包需要解析dom，自动化复杂

* jython无法直接使用python selenium库，不能做成burp插件





