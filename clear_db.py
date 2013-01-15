import MySQLdb as mdb
import logging

con = mdb.connect('localhost', 'root', '', 'datapanel')
cur = con.cursor()


def get_foreign_key_names(database_name):
    cur.execute("SELECT `table_schema`, `table_name`, `constraint_name` FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY' AND table_schema = %s;", [database_name])
    return cur.fetchall()


def remove_foreign_key(schema_name, table_name, key_name):
    logging.info("Removing foreign key %s from %s.%s" % (key_name, schema_name, table_name))
    sql = "ALTER TABLE %s.%s DROP FOREIGN KEY %s;" % (schema_name, table_name, key_name)
    cur.execute(sql)


def remove_all_foreign_keys(database_name):
    foreign_keys = get_foreign_key_names(database_name)
    logging.info("Removing all foreign key constraints from database: %s" % database_name)
    for schema_name, table_name, key_name in foreign_keys:
        remove_foreign_key(schema_name, table_name, key_name)

remove_all_foreign_keys('datapanel')

sql = 'SELECT id, order_sn FROM ecshop_orderinfo'
cur.execute(sql)
orders = {}
for id, order_sn in cur.fetchall():
    orders[id] = order_sn

del_order = []
for k, v in orders.items():
    sql = "SELECT id FROM ecshop_orderinfo WHERE order_sn='%s' AND id<%d" % (v, k)
    cur.execute(sql)
    res = cur.fetchone()
    if res and res[0] not in del_order:
        del_order.append(res[0])

for order_id in del_order:
    sql = "DELETE FROM ecshop_orderinfo WHERE id=%d" % order_id
    cur.execute(sql)

# sql = "show tables"
# cur.execute(sql)
# t = cur.fetchone()[0]
# msql = ""
# while t:
#     try:
#         #print t
#         msql += "ALTER TABLE " + t + " ENGINE=MyISAM;\n"
#         t = cur.fetchone()[0]
#     except:
#         break

# print msql
# cur.execute(msql)