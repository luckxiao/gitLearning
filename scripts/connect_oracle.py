#  连接 oracle 数据库
# @time 2023.11.3

import oracledb

def Conn(host,port,user,password,service_name):
    """
    :param host: 数据库主机地址
    :param port: 端口号
    :param user: 数据库用户名
    :param password: 数据库密码
    :param service_name: 连接数据库
    :return:
    """
    conn = oracledb.connect(host=host, port=port, user=user, password=password, service_name =service_name)
    return conn

def fetch_sql():
    conn = Conn(host, port, user, password, service_name)
    cursor = conn.cursor()
    datas = cursor.execute("select * from WIND_NEW_PDM where rownum<10")
    for row in datas:
        print(row)

if __name__=='__main__':
    # oracle = oracledb.connection(dsn="bigdata_admin/qeGAB9Fx5DX32L9D3W5g@192.168.1.91:1521/bigdatadb")
    # 添加 oracle 客户端安装路径
    oracledb.init_oracle_client(lib_dir=r"D:\\PLSQL\\product\\11.2.0\\dbhome_1\\bin")
    host = '192.168.1.91'
    port = 1521
    user = 'bigdata_admin'
    password = 'qeGAB9Fx5DX32L9D3W5g'
    service_name = 'bigdatadb'
    fetch_sql()



