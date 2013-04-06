# coding=utf-8
import MySQLdb as _mysql

from django.core.management.base import NoArgsCommand
from project.models import Project


class Command(NoArgsCommand):

    def split_goods(self, goods_ids):
        return [int(i) for i in goods_ids.split(',')]

    def set_goods_dict(self, goods_dict, goods_ids):
        for g1 in goods_ids:
            if g1 not in goods_dict:
                goods_dict[g1] = {}
            for g2 in goods_ids:
                if g2 in goods_dict[g1]:
                    goods_dict[g1][g2] += 1
                else:
                    goods_dict[g1][g2] = 1

    def write_csv(self, goods_dict):
        f = open('test.csv', 'w')
        for goods, goods_attr in goods_dict.items():
            for k, v in goods_attr.items():
                if not k == goods:
                    f.write('%d,%d,%d,%d,%f\n' % (goods, k, v, goods_attr[goods], float(v)/goods_attr[goods]*100))
        f.close()

    def write_db(self, goods_dict, project_id, relation_type):
        sql = """INSERT INTO ecshop_goods_relation(project_id, goods_id, goods_related, hit_count, hit_percent, relationship) VALUES(%d, %d, %d, %d, %f, %s)"""
        values = []
        for goods, goods_attr in goods_dict.items():
            for k, v in goods_attr.items():
                if not k == goods:
                    values .append((project_id, goods, k, v, float(v)/goods_attr[goods]*100, relation_type))
        return (sql, values)

    def handle_noargs(self, **options):
        conn = _mysql.connect(host='127.0.0.1', user='root', passwd='')
        conn.select_db('datapanel')
        cursor = conn.cursor()
        for project in Project.objects.filter():
            project_id = project.id
            goods_dict = {}
            cursor.execute(
                'select group_concat(distinct(goods_id)) from ecshop_ordergoods where order_id > 0 and project_id=%d GROUP BY order_id;' % project_id)
            goodstrs = cursor.fetchall()
            for r in goodstrs:
                goodstr = r[0]
                self.set_goods_dict(goods_dict, self.split_goods(goodstr))

            sql, values = self.write_db(goods_dict, project_id, 'buy')
            cursor.executemany(sql, values)

            cursor.execute(
                'select group_concat(distinct(goods_id)) from track_trackvaluearch tv JOIN track_trackarch a ON ta.track_id=a.track_id where a.session_id > 0 WHERE project_id=%d GROUP BY a.session_id;' % project_id)
            goodstrs = cursor.fetchall()
            for r in goodstrs:
                goodstr = r[0]
                self.set_goods_dict(goods_dict, self.split_goods(goodstr))

            sql, values = self.write_db(goods_dict, project_id, 'view')
            cursor.executemany(sql, values)

        conn.close()
