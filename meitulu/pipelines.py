# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonItemExporter
import MySQLdb

class MeituluPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonExporterPipleline(object):
    def __init__(self):
        self.file = open('metulu.json','wb')
        self.exporter = JsonItemExporter(self.file , encoding='utf-8' , ensure_ascii= False)
        self.exporter.start_exporting()
    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()
    def process_item(self,item,spider):
        self.exporter.export_item(item=item)
        return item

class MysqlPipleline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1' , 'root' , 'root' , 'scrapy' , charset='utf8',use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        url = ','.join(item.get('pirc_srcs'))
        info = ','.join(item.get('info'))
        insert_sql = """
            insert into metulu(title,info,message,pirc) VALUES (%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql,(item.get("title"), info, item.get("message"), url))
        self.conn.commit()


