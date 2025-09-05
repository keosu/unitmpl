# PostgreSQL 密码设置指南

## 方案1：通过pgAdmin设置（推荐）
1. 打开 pgAdmin 4（在开始菜单搜索）
2. 首次打开会要求设置 master password
3. 添加服务器连接：
   - Host: localhost
   - Port: 5432
   - Username: postgres
   - 如果提示密码错误，选择"保存密码"为空，然后连接
4. 右键点击 "postgres" 用户 → Properties → Definition
5. 设置新密码：password
6. 保存

## 方案2：通过命令行设置
1. 打开命令提示符（以管理员身份）
2. 临时修改认证方式：
   编辑文件：C:\Program Files\PostgreSQL\17\data\pg_hba.conf
   将这行：
   host    all             all             127.0.0.1/32            scram-sha-256
   改为：
   host    all             all             127.0.0.1/32            trust

3. 重启PostgreSQL服务：
   net stop postgresql-x64-17
   net start postgresql-x64-17

4. 设置密码：
   "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -c "ALTER USER postgres PASSWORD 'password';"

5. 改回安全的认证方式（将trust改回scram-sha-256）
6. 再次重启服务

## 方案3：重新初始化数据库
如果以上方法都不行，可以：
1. 卸载PostgreSQL
2. 删除数据目录：C:\Program Files\PostgreSQL\17\data
3. 重新安装PostgreSQL，在安装过程中设置密码

## 修改配置文件使用PostgreSQL
当密码设置好后，修改 .env 文件：
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/lawchat_db

然后创建数据库：
"C:\Program Files\PostgreSQL\17\bin\createdb.exe" -U postgres lawchat_db