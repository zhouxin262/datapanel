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

    def write_csv(self, goods_dict, project_id, relation_type):
        f = open('test.csv', 'w')
        for goods, goods_attr in goods_dict.items():
            for k, v in goods_attr.items():
                if not k == goods:
                    f.write('%d,%d,%d,%d,%f\n' % (goods, k, v, goods_attr[goods], round(float(v)/goods_attr[goods]*100, 3)))
        f.close()

    def write_db(self, goods_dict, project_id, relation_type):
        sql = """INSERT INTO ecshop_goodsrelation(project_id, goods_id, goods_related_id, hit_count, hit_percent, relationship) VALUES(%d, %d, %d, %d, %f, %d)"""
        sqls = []
        for goods, goods_attr in goods_dict.items():
            for k, v in goods_attr.items():
                if not k == goods:
                    sqls.append(sql % (project_id, goods, k, v, round(float(v)/goods_attr[goods]*100, 3), relation_type))
        return sqls
        # return sql % values[0]

    def handle_noargs(self, **options):
        conn = _mysql.connect(host='127.0.0.1', user='root', passwd='')
        conn.select_db('datapanel')
        cursor = conn.cursor()
        cursor.execute('SET group_concat_max_len=102400;')
        # for project in Project.objects.filter():
        project_id = 1
        goods_dict = {}
        # cursor.execute(
        #     'select group_concat(distinct(goods_id)) from ecshop_ordergoods where order_id > 0 and project_id=%d GROUP BY order_id;' % project_id)
        # goodstrs = cursor.fetchall()
        # for r in goodstrs:
        #     goodstr = r[0]
        #     self.set_goods_dict(goods_dict, self.split_goods(goodstr))
        # sqls = self.write_db(goods_dict, project_id, 0)
        # for sql in sqls:
        #     cursor.execute(sql)

        goods_dict = {}
        cursor.execute(
            '''SELECT GROUP_CONCAT(DISTINCT(value))
FROM track_trackvaluearch ta
JOIN track_trackarch a ON ta.track_id=a.id
WHERE ta.valuetype_id = 2 and a.project_id = %d
GROUP BY a.session_id''' % project_id)
        goodstrs = cursor.fetchall()

        for r in goodstrs:
            goodstr = r[0]
            self.set_goods_dict(goods_dict, self.split_goods(goodstr))

        sqls = self.write_db(goods_dict, project_id, 1)
        for sql in sqls:
            cursor.execute(sql)
