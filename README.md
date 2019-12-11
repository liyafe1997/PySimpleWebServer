**！！这不是一个HTML Repo，这是Python，因为example里面有大量的HTML所以github给它打了HTML标签！！**

**!! This is not a HTML Repo, it's python. The reason of github marked it is a HTML project is a lot HTML pages in the example!!**

# 简体中文（Chinese Simplified）
## I am tired to write this so English is temporarily unavailable. Before I written English down, just Google Translate please!

这是一个非常简单的，用python实现http服务（尤其是microservice）的Framework。甚至我不敢称它为一个framework，只是一个template，方便我需要实现http service的时候直接往上面加东西。

这是我找到的最简单、最快速实现http server以及microservice的方式，甚至没有用第三方的库，用到的全部都是Python默认环境自带的模块，也就是说只要你有一个完整的Python3，就能跑起这个Http Server。

简单讲解下用法，对于HTML及文件服务，只需要放在./WEBCONTENT/下就可以，访问/时默认读取index.html

对于实现microservice，你只需要仿照

#------------------Web Services Start-----------------

和

#------------------Web Services End-----------------

之间的Helloworld例子，实现自己的mircoservice就可以了。比如返回一个JSON。

如果你需要“存点东西”，我在里面写好了一个SQLike连接器，你可以用这个所谓的“SQL”数据库来“存点东西”。

只需修改main函数中的sqlikesock.connect(('127.0.0.1', 1667))，对应你的SQLike服务器的IP地址和端口即可

然后只需要调用SQLike_Query("SQL COMMAND balabala")即可完成对SQLike的操作

关于SQLike_Query支持的命令以及返回的数据的格式请看下面SQLike页面最底部的介绍，不过呢我这里可以直接给个Tips，直接（result是SQLike_Query返回的对象）

thedata = result.split('\n')[x].split('\t')[y]

x是你想取的数据在第几行，从1开始算。（第0行是columns，或者叫表头吧，print一下result就懂了）。然后y是第几列。这样就取到对应的数据了。


什么是SQLike？

Oh it's another stuff I just made it for fun(like this project): https://github.com/liyafe1997/SQLike

哦对了，example里面是一个例子。如果要跑起来，你需要去git clone一份SQLike.py到同目录下（与DB文件夹同目录），

然后先把SQLike跑起来。 

python SQLike.py

server 127.0.0.1:1667 （当然你想bind 0.0.0.0也无所谓）

然后python webserver_example.py

然后访问127.0.0.1:8081就有了。

这个example乃至这个repo（抱歉我甚至不想说这是个project）的由来呢，也是对付一个课程设计的作业，题目是一个所谓的“博客管理系统”。最初的目的只是想证明一下SQLike是真的真的“可用”的，可以实现Socket连接操作数据，执行我定义的所谓的“SQL”语句hhhhhh，返回到webserver中，这套系统是真的“可用”的。因此这个所谓的“系统”做得非常粗糙，只是make it works, oh it really works, 所以bug无处不在，所以大家别就这个example中的bug给我反馈了。
