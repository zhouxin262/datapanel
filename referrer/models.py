# coding=utf-8
from django.db import models

'''重复
CREATE TABLE `tmp_refrrer_id` (
    `id` INT(10) NULL,
    `c` INT(10) NULL
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM;

INSERT INTO tmp_refrrer_id SELECT max(id) id, count(*) c FROM referrer_keyword GROUP BY name;
DELETE FROM tmp_refrrer_id WHERE c <=1;
DELETE t FROM referrer_keyword t LEFT JOIN tmp_refrrer_id r ON t.id = r.id WHERE r.id is not null;
DROP TABLE tmp_refrrer_id;


CREATE TABLE `tmp_refrrer_id` (
    `id` INT(10) NULL,
    `c` INT(10) NULL
)
COLLATE='utf8_general_ci'
ENGINE=MyISAM;

INSERT INTO tmp_refrrer_id SELECT max(id) id, count(*) c FROM referrer_site GROUP BY name;
DELETE FROM tmp_refrrer_id WHERE c <=1;
DELETE t FROM referrer_site t LEFT JOIN tmp_refrrer_id r ON t.id = r.id WHERE r.id is not null;
DROP TABLE tmp_refrrer_id;
'''


class Site(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'域名', default='')


class Keyword(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'关键词', default='')
