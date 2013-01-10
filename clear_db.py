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

sql = "DELETE FROM session_greferrerkeyword WHERE timeline_id is null;"
cur.execute(sql)
sql = "DELETE FROM session_greferrersite WHERE timeline_id is null;"
cur.execute(sql)
sql = "DELETE FROM session_gtime WHERE timeline_id is null;"
cur.execute(sql)
sql = "DELETE FROM track_gaction WHERE timeline_id is null;"
cur.execute(sql)
sql = "DELETE FROM track_greferrerkeywordandaction WHERE timeline_id is null;"
cur.execute(sql)
sql = "DELETE FROM track_greferrersiteandaction WHERE timeline_id is null;"
cur.execute(sql)

sql = "INSERT INTO %s(id, project_id, session_key, permanent_session_key, start_time, end_time, user_language, user_timezone, agent_id, os_id, device_id, referrer_site_id, referrer_keyword_id, track_count, timelength, ipaddress) SELECT id, project_id, session_key, permanent_session_key, start_time, end_time, user_language, user_timezone, agent_id, os_id, device_id, referrer_site_id, referrer_keyword_id, track_count, timelength, ipaddress FROM %s f WHERE f.id >= %d" % ('session_session', 'session_sessionarch', 313671)
cur.execute(sql)
sql = "DELETE FROM %s WHERE id >= %d" % ('session_sessionarch', 313671)
cur.execute(sql)
sql = "INSERT INTO %s(id, session_id, valuetype_id, value) SELECT id, session_id, valuetype_id, value FROM %s f WHERE f.session_id >= %d" % ('session_sessionvalue', 'session_sessionvaluearch', 313671)
cur.execute(sql)
sql = "DELETE FROM %s WHERE session_id >= %d" % ('session_sessionvaluearch', 313671)
cur.execute(sql)
sql = "OPTIMIZE TABLE %s" % 'session_sessionarch'
cur.execute(sql)
sql = "OPTIMIZE TABLE %s" % 'session_sessionvaluearch'
cur.execute(sql)
sql = "flush tables"
cur.execute(sql)

sql = "INSERT INTO %s(id, project_id, session_id, action_id, url, from_track_id, referrer_site_id, referrer_keyword_id, step, timelength, dateline) SELECT id, project_id, session_id, action_id, url, from_track_id, referrer_site_id, referrer_keyword_id, step, timelength, dateline FROM %s f WHERE f.id >= %d" % ('track_track', 'track_trackarch', 569976)
cur.execute(sql)
sql = "DELETE FROM %s WHERE id >= %d" % ('track_trackarch', 569976)
cur.execute(sql)
sql = "INSERT INTO %s(id, track_id, valuetype_id, value) SELECT id, track_id, valuetype_id, value FROM %s f WHERE f.track_id >= %d" % ('track_trackvalue', 'track_trackvaluearch', 569976)
cur.execute(sql)
sql = "DELETE FROM %s WHERE track_id >= %d" % ('track_trackvaluearch', 569976)
cur.execute(sql)
sql = "OPTIMIZE TABLE %s" % 'track_trackarch'
cur.execute(sql)
sql = "OPTIMIZE TABLE %s" % 'track_trackvaluearch'
cur.execute(sql)
sql = "flush tables"
cur.execute(sql)
