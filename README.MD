###需求分析
01.用户加密认证；
利用md5进行加密，客户端密码录入采用隐藏模式（仅限Linux）；
02.允许同时多用户登录;
03.每个用户有自己的家目录，且只能访问自己的家目录：
服务器配置每个用户独立的目录，切换目录时做了验证；
04.对用户进行磁盘配额，每个用户的可用空间不同：
由客户端的配置文件user.txt来记录配额，配额目前只支持MB；
05.允许用户再ftp server上随意切换目录(cd)
- 只影响客户端的显示
- 服务器的根目录不变
- 要校验，只能访问自己的家目录

6.允许用户查看当前目录下文件(ls);
7.允许上传和下载文件，保证文件一致性(md5);
8.文件传输过程中显示进度条；

###系统设计
- FTP的注册用户、密码和配额都存储在ftp_server/db下；
- 上传和下载文件，采用了大小来界定文件的边界，防止TCP粘包；
- 上传和下载，均采用md5文件校验的方式，保持数据传输的一致性；
- 服务器的目录可以随时切换，切换的原理：服务器用户的根目录不变，变化的仅仅是客户端的目录显示；
- 上传文件的额度，在登录验证时，通过服务器返回额度和已用额度，已用额度采用实时计算目录大小的方式；
- FTP服务器与客户端之间的交互，参考HTTP的状态码，成功与失败都会有；
- 多用户同时访问的功能，FTP服务器采用Socketserver，多线程来实现多用户操作；

###测试
测试账号：
- user1 / 123456
- user2 / 123456
