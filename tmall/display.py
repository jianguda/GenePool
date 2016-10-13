# -*- coding=utf-8 -*-
import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
import pymongo

define("port", default=8000, help="run on the given port", type=int)

global id
id = '3610047'


class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
			(r"/", MainHandler),
			(r"/contrast/", ContrastHandler),
			(r"/gene_pool/", GenePoolHandler),
			(r"/list_slogan/", ListSloganHandler),
			(r"/related_list/", RelatedListHandler),
			(r".*", BaseHandler),
		]
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			ui_modules={"Entry": EntryModule, "Item": ItemModule, "Pin": PinModule},
			debug=True,
		)
		conn = pymongo.MongoClient("localhost", 27017)
		self.db = conn["display"]
		tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"dash_board.html",
		)


class ContrastHandler(tornado.web.RequestHandler):
	def get(self):
		coll0m = self.application.db.boot_media
		coll0a = self.application.db.static_a
		coll0b = self.application.db.static_b
		coll_gather = self.application.db.boot_gather
		entry0m = coll0m.find_one({"id": id})
		entry0a = coll0a.find_one({"id": id})
		entry0b = coll0b.find_one({"id": id})
		entry_gather = coll_gather.find_one({"id": id})
		mixer = [
			'name', 'director', 's_director', 'actor', 's_actor', 'cate', 's_cate', 'area', 'year', 'alias', 'rate',
			'tag', 'tag2',
			'time', 'site', 'inst', 'comm'
		]
		moxer = [
			'名称', '导演', '名导演', '演员', '名演员', '类型', '细类型', '地区', '年份', '又名', '打分', '标签1', '标签2',
			'时间', '地点', '组织', '评价'
		]
		table0 = []
		isis0 = entry0b.get('name')
		isis1 = ("../static/image/" + id + ".jpg")
		for i in range(len(mixer)):
			if i == 2 or i == 4 or i == 6:
				head_column = entry0a.get(mixer[i - 1])
			elif i == 11:
				head_column = ' '.join(
					[entry0b.get(mixer[1]), entry0b.get(mixer[3]), entry0b.get(mixer[5]), entry0b.get(mixer[7])]
				)
			elif i == 12:
				head_column = ' '.join(
					[
						entry_gather.get(mixer[13]), entry_gather.get(mixer[14]),
						entry_gather.get(mixer[15]), entry_gather.get(mixer[16])
					]
				)
			elif i >= 13:
				head_column = entry_gather.get(mixer[i])
			else:
				head_column = entry0b.get(mixer[i])
			tail_column = entry0m.get(mixer[i])
			if head_column and tail_column:
				table0.append([moxer[i], head_column, tail_column])
			elif head_column:
				table0.append([moxer[i], head_column, ""])
			elif tail_column:
				table0.append([moxer[i], "", tail_column])
			else:
				table0.append([moxer[i], "", ""])
		if entry0a and entry0b and entry0m:
			self.render(
				"contrast.html",
				isis0=isis0,
				isis1=isis1,
				entries0=table0
			)
		else:
			self.redirect("/contrast/")

	def post(self):
		coll0m = self.application.db.boot_media
		coll0a = self.application.db.static_a
		coll0b = self.application.db.static_b
		coll_gather = self.application.db.boot_gather
		global id
		enter = self.get_argument("id")
		if enter.isdigit():
			id = enter
		else:
			entry_temp = coll0b.find_one({"name": {'$regex': '\S*' + enter + '\S*'}})
			if entry_temp:
				id = entry_temp.get('id')
		entry0m = coll0m.find_one({"id": id})
		entry0a = coll0a.find_one({"id": id})
		entry0b = coll0b.find_one({"id": id})
		entry_gather = coll_gather.find_one({"id": id})
		mixer = [
			'name', 'director', 's_director', 'actor', 's_actor', 'cate', 's_cate', 'area', 'year', 'alias', 'rate',
			'tag', 'tag2',
			'time', 'site', 'inst', 'comm'
		]
		moxer = [
			'名称', '导演', '名导演', '演员', '名演员', '类型', '细类型', '地区', '年份', '又名', '打分', '标签1', '标签2',
			'时间', '地点', '组织', '评价'
		]
		table0 = []
		isis0 = entry0b.get('name')
		isis1 = ("../static/image/" + id + ".jpg")
		for i in range(len(mixer)):
			if i == 2 or i == 4 or i == 6:
				head_column = entry0a.get(mixer[i - 1])
			elif i == 11:
				head_column = ' '.join(
					[entry0b.get(mixer[1]), entry0b.get(mixer[3]), entry0b.get(mixer[5]), entry0b.get(mixer[7])]
				)
			elif i == 12:
				head_column = ' '.join(
					[
						entry_gather.get(mixer[13]), entry_gather.get(mixer[14]),
						entry_gather.get(mixer[15]), entry_gather.get(mixer[16])
					]
				)
			elif i >= 13:
				head_column = entry_gather.get(mixer[i])
			else:
				head_column = entry0b.get(mixer[i])
			tail_column = entry0m.get(mixer[i])
			if head_column and tail_column:
				table0.append([moxer[i], head_column, tail_column])
			elif head_column:
				table0.append([moxer[i], head_column, ""])
			elif tail_column:
				table0.append([moxer[i], "", tail_column])
			else:
				table0.append([moxer[i], "", ""])
		if entry0a and entry0b and entry0m:
			self.render(
				"contrast.html",
				isis0=isis0,
				isis1=isis1,
				entries0=table0
			)
		else:
			self.redirect("/contrast/")


class GenePoolHandler(tornado.web.RequestHandler):
	def get(self):
		coll0a = self.application.db.static_a
		coll0b = self.application.db.static_b
		coll1a = self.application.db.segment_a
		coll1b = self.application.db.segment_b
		coll2a = self.application.db.trans_a
		coll2b = self.application.db.trans_b
		coll3a = self.application.db.comment_a
		coll3b = self.application.db.comment_b
		entry0a = coll0a.find_one({"id": id})
		entry0b = coll0b.find_one({"id": id})
		entry1a = coll1a.find_one({"id": id})
		entry1b = coll1b.find_one({"id": id})
		entry2a = coll2a.find_one({"id": id})
		entry2b = coll2b.find_one({"id": id})
		entry3a = coll3a.find_one({"id": id})
		entry3b = coll3b.find_one({"id": id})
		mixer0 = ['name', 'director', 'actor', 'cate', 'area', 'year', 'alias', 'rate']
		mixer1 = ['time', 'site', 'inst']
		mixer2 = ['time', 'site', 'inst', 'comm']
		mixer3 = ['comm']
		moxer0 = ['名称', '导演', '演员', '类型', '地区', '年份', '别名', '打分']
		moxer1 = ['时间', '地点', '组织']
		moxer2 = ['时间', '地点', '组织', '评价']
		moxer3 = ['评价']
		table0 = []
		table1 = []
		table2 = []
		table3 = []
		isis0 = entry0b.get('name')
		isis1 = ("../static/image/" + id + ".jpg")
		for i in range(len(mixer0)):
			head_column = entry0b.get(mixer0[i])
			tail_column = entry0a.get(mixer0[i])
			if head_column and tail_column:
				table0.append([moxer0[i], head_column, tail_column])
			elif head_column:
				table0.append([moxer0[i], head_column, ""])
			elif tail_column:
				table0.append([moxer0[i], "", tail_column])
			else:
				table0.append([moxer0[i], "", ""])
		for i in range(len(mixer1)):
			head_column = entry1b.get(mixer1[i])
			tail_column = entry1a.get(mixer1[i])
			if head_column and tail_column:
				table1.append([moxer1[i], head_column, tail_column])
			elif head_column:
				table1.append([moxer1[i], head_column, ""])
			elif tail_column:
				table1.append([moxer1[i], "", tail_column])
			else:
				table1.append([moxer1[i], "", ""])
		for i in range(len(mixer2)):
			head_column = entry2b.get(mixer2[i])
			tail_column = entry2a.get(mixer2[i])
			if head_column and tail_column:
				table2.append([moxer2[i], head_column, tail_column])
			elif head_column:
				table2.append([moxer2[i], head_column, ""])
			elif tail_column:
				table2.append([moxer2[i], "", tail_column])
			else:
				table2.append([moxer2[i], "", ""])
		for i in range(len(mixer3)):
			head_column = entry3b.get(mixer3[i])
			tail_column = entry3a.get(mixer3[i])
			if head_column and tail_column:
				table3.append([moxer3[i], head_column, tail_column])
			elif head_column:
				table3.append([moxer3[i], head_column, ""])
			elif tail_column:
				table3.append([moxer3[i], "", tail_column])
			else:
				table3.append([moxer3[i], "", ""])
		if entry0b and entry1b:
			self.render(
				"gene_pool.html",
				isis0=isis0,
				isis1=isis1,
				entries0=table0,
				entries1=table1,
				entries2=table2,
				entries3=table3
			)
		else:
			self.redirect("/gene_pool/")

	def post(self):
		coll0a = self.application.db.static_a
		coll0b = self.application.db.static_b
		coll1a = self.application.db.segment_a
		coll1b = self.application.db.segment_b
		coll2a = self.application.db.trans_a
		coll2b = self.application.db.trans_b
		coll3a = self.application.db.comment_a
		coll3b = self.application.db.comment_b
		global id
		enter = self.get_argument("id")
		if enter.isdigit():
			id = enter
		else:
			entry_temp = coll0b.find_one({"name": {'$regex': '\S*' + enter + '\S*'}})
			if entry_temp:
				id = entry_temp.get('id')
		entry0a = coll0a.find_one({"id": id})
		entry0b = coll0b.find_one({"id": id})
		entry1a = coll1a.find_one({"id": id})
		entry1b = coll1b.find_one({"id": id})
		entry2a = coll2a.find_one({"id": id})
		entry2b = coll2b.find_one({"id": id})
		entry3a = coll3a.find_one({"id": id})
		entry3b = coll3b.find_one({"id": id})
		mixer0 = ['name', 'director', 'actor', 'cate', 'area', 'year', 'alias', 'rate']
		mixer1 = ['time', 'site', 'inst']
		mixer2 = ['time', 'site', 'inst', 'comm']
		mixer3 = ['comm']
		moxer0 = ['名称', '导演', '演员', '类型', '地区', '年份', '别名', '打分']
		moxer1 = ['时间', '地点', '组织']
		moxer2 = ['时间', '地点', '组织', '评价']
		moxer3 = ['评价']
		table0 = []
		table1 = []
		table2 = []
		table3 = []
		isis0 = entry0b.get('name')
		isis1 = ("../static/image/" + id + ".jpg")
		for i in range(len(mixer0)):
			head_column = entry0b.get(mixer0[i])
			tail_column = entry0a.get(mixer0[i])
			if head_column and tail_column:
				table0.append([moxer0[i], head_column, tail_column])
			elif head_column:
				table0.append([moxer0[i], head_column, ""])
			elif tail_column:
				table0.append([moxer0[i], "", tail_column])
			else:
				table0.append([moxer0[i], "", ""])
		for i in range(len(mixer1)):
			head_column = entry1b.get(mixer1[i])
			tail_column = entry1a.get(mixer1[i])
			if head_column and tail_column:
				table1.append([moxer1[i], head_column, tail_column])
			elif head_column:
				table1.append([moxer1[i], head_column, ""])
			elif tail_column:
				table1.append([moxer1[i], "", tail_column])
			else:
				table1.append([moxer1[i], "", ""])
		for i in range(len(mixer2)):
			head_column = entry2b.get(mixer2[i])
			tail_column = entry2a.get(mixer2[i])
			if head_column and tail_column:
				table2.append([moxer2[i], head_column, tail_column])
			elif head_column:
				table2.append([moxer2[i], head_column, ""])
			elif tail_column:
				table2.append([moxer2[i], "", tail_column])
			else:
				table2.append([moxer2[i], "", ""])
		for i in range(len(mixer3)):
			head_column = entry3b.get(mixer3[i])
			tail_column = entry3a.get(mixer3[i])
			if head_column and tail_column:
				table3.append([moxer3[i], head_column, tail_column])
			elif head_column:
				table3.append([moxer3[i], head_column, ""])
			elif tail_column:
				table3.append([moxer3[i], "", tail_column])
			else:
				table3.append([moxer3[i], "", ""])
		if entry0b and entry1b:
			self.render(
				"gene_pool.html",
				isis0=isis0,
				isis1=isis1,
				entries0=table0,
				entries1=table1,
				entries2=table2,
				entries3=table3
			)
		else:
			self.redirect("/gene_pool/")


class ListSloganHandler(tornado.web.RequestHandler):
	def get(self):
		keys = [
			"oa幸福#oa唯美", "oa诙谐#oa幽默", "oa惊悚#oa惊魂", "oa清新#oa纯真", "ot冬天", "ot青春期", "nt马戏团", "nt大学"
		]
		slogans = [
			"幸福与唯美永远同在", "诙谐的事和幽默的人", "惊悚到底，直到惊魂", "清新的日子纯真的人", "发生在冬天的故事", "青春期的少男少女", "马戏团的欢声笑语", "大学里的那些事儿"
		]
		coll_ot = self.application.db.table_ot
		coll_ns = self.application.db.table_ns
		coll_nt = self.application.db.table_nt
		coll_oa = self.application.db.table_oa
		coll_static = self.application.db.static_b
		coll_gather = self.application.db.boot_gather
		tables0 = []
		tables1 = []
		tables2 = []
		for key in keys:
			item_key = []
			key_list = key.split("#")
			for key_it in key_list:
				if key_it.startswith("ot"):
					item_key.append(coll_ot.find_one({"name": key_it[2:]}).get("entry"))
				elif key_it.startswith("ns"):
					item_key.append(coll_ns.find_one({"name": key_it[2:]}).get("entry"))
				elif key_it.startswith("nt"):
					item_key.append(coll_nt.find_one({"name": key_it[2:]}).get("entry"))
				elif key_it.startswith("oa"):
					item_key.append(coll_oa.find_one({"name": key_it[2:]}).get("entry"))
			temp_set = set()
			for item_it in item_key:
				temp_list = item_it.split("/")
				if len(temp_set) > 0:
					temp_set = temp_set.intersection(set(temp_list))
				else:
					temp_set = set(temp_list)
			item_key = list(temp_set)
			#
			table0 = item_key
			table_len = len(table0)
			for it in range(0, table_len):
				item_static = coll_static.find_one({"id": table0[it]})
				table0[it] = {
					"id": table0[it],
					"rate": item_static.get("rate"),
					"year": item_static.get("year")
				}
			for table_it in table0:
				if table_it.get("year") >= '2000':
					table0.remove(table_it)
			table_len = len(table0)
			for ix in range(0, table_len - 1):
				max_node = ix
				for iy in range(ix + 1, table_len):
					if float(table0[iy].get("rate")) > float(table0[max_node].get("rate")):
						max_node = iy
				if max_node != ix:
					temp_dict = table0[ix]
					table0[ix] = table0[max_node]
					table0[max_node] = temp_dict
			for it in range(0, table_len):
				table0[it] = table0[it].get("id")
			table1 = []
			table2 = []
			for it in range(0, table_len):
				item_static = coll_static.find_one({"id": table0[it]})
				if item_static:
					table1.append(item_static.get("name"))
				else:
					table1.append("None")
				table2.append("../static/image/" + table0[it] + ".jpg")
			item_base = []
			for tabs in table0:
				temp_base = ""
				for key_it in key_list:
					if key_it.startswith("ot"):
						if temp_base != "":
							temp_base += "#"
						temp_base += coll_gather.find_one({"id": tabs}).get("time")
					elif key_it.startswith("ns"):
						if temp_base != "":
							temp_base += "#"
						temp_base += coll_gather.find_one({"id": tabs}).get("site")
					elif key_it.startswith("nt"):
						if temp_base != "":
							temp_base += "#"
						temp_base += coll_gather.find_one({"id": tabs}).get("inst")
					elif key_it.startswith("oa"):
						if temp_base != "":
							temp_base += "#"
						temp_base += coll_gather.find_one({"id": tabs}).get("comm")
				item_base.append(temp_base)
			tables0.append(item_base)
			tables1.append(table1)
			tables2.append(table2)
		if tables0 and tables1 and tables2:
			self.render(
				"list_slogan.html",
				isis0="--------视频基因库--------",
				isis1="../static/____.jpg",
				itemss0=tables0,
				itemss1=tables1,
				itemss2=tables2,
				slogans=slogans
			)
		else:
			self.redirect("/list_slogan/")


class RelatedListHandler(tornado.web.RequestHandler):
	def get(self):
		coll_ot = self.application.db.table_ot
		coll_ns = self.application.db.table_ns
		coll_nt = self.application.db.table_nt
		coll_oa = self.application.db.table_oa
		coll_static = self.application.db.static_b
		coll_gather = self.application.db.boot_gather
		item_gather = coll_gather.find_one({"id": id})
		list_ot = item_gather.get("time").split("#")
		list_ns = item_gather.get("site").split("#")
		list_nt = item_gather.get("inst").split("#")
		list_oa = item_gather.get("comm").split("#")
		queue_all = list()
		for ot in list_ot:
			item_ot = coll_ot.find_one({"name": ot})
			if item_ot:
				queue_all.extend(item_ot.get("entry").split("/"))
		for ns in list_ns:
			item_ns = coll_ns.find_one({"name": ns})
			if item_ns:
				queue_all.extend(item_ns.get("entry").split("/"))
		for nt in list_nt:
			item_nt = coll_nt.find_one({"name": nt})
			if item_nt:
				queue_all.extend(item_nt.get("entry").split("/"))
		for oa in list_oa:
			item_oa = coll_oa.find_one({"name": oa})
			if item_oa:
				queue_all.extend(item_oa.get("entry").split("/"))
		if len(queue_all) > 0:
			temp_list = []
			for temp_it in queue_all:
				if temp_it != id:
					temp_list.append(temp_it)
			queue_all = list(set(temp_list))
			len_queue = len(queue_all)
			# 影视类型
			temp_static = coll_static.find_one({"id": id})
			set_cate_static = set(temp_static.get("cate").split("#"))
			set_actor_static = set(temp_static.get("actor").split("#"))
			set_ot_gather = set(list_ot)
			set_ns_gather = set(list_ns)
			set_nt_gather = set(list_nt)
			set_oa_gather = set(list_oa)
			for it in range(0, len_queue):
				item_static = coll_static.find_one({"id": queue_all[it]})
				item_gather = coll_gather.find_one({"id": queue_all[it]})
				queue_all[it] = {
					"id": queue_all[it],
					"cate": len(set(item_static.get("cate").split("#")).intersection(set_cate_static)),
					"actor": len(set(item_static.get("actor").split("#")).intersection(set_actor_static)),
					"time": len(set(item_gather.get("time").split("#")).intersection(set_ot_gather)),
					"site": len(set(item_gather.get("site").split("#")).intersection(set_ns_gather)),
					"inst": len(set(item_gather.get("inst").split("#")).intersection(set_nt_gather)),
					"comm": len(set(item_gather.get("comm").split("#")).intersection(set_oa_gather)),
					"rate": item_static.get("rate"),
					"year": item_static.get("year")
				}
			for it in range(0, len_queue):
				len_union_ot = len(set(item_gather.get("time").split("#")).union(set_ot_gather))
				len_union_ns = len(set(item_gather.get("site").split("#")).union(set_ns_gather))
				len_union_nt = len(set(item_gather.get("inst").split("#")).union(set_nt_gather))
				len_union_oa = len(set(item_gather.get("comm").split("#")).union(set_oa_gather))
				if queue_all[it].get("time") == len_union_ot:
					queue_all[it]["time"] = 3
				elif queue_all[it].get("time") >= len_union_ot / 2:
					queue_all[it]["time"] = 2
				elif queue_all[it].get("time") > 0:
					queue_all[it]["time"] = 1
				else:
					queue_all[it]["time"] = 0
				if queue_all[it].get("site") == len_union_ns:
					queue_all[it]["site"] = 3
				elif queue_all[it].get("site") >= len_union_ns / 2:
					queue_all[it]["site"] = 2
				elif queue_all[it].get("site") > 0:
					queue_all[it]["site"] = 1
				else:
					queue_all[it]["site"] = 0
				if queue_all[it].get("inst") == len_union_nt:
					queue_all[it]["inst"] = 3
				elif queue_all[it].get("inst") >= len_union_nt / 2:
					queue_all[it]["inst"] = 2
				elif queue_all[it].get("inst") > 0:
					queue_all[it]["inst"] = 1
				else:
					queue_all[it]["inst"] = 0
				if queue_all[it].get("comm") == len_union_oa:
					queue_all[it]["comm"] = 3
				elif queue_all[it].get("comm") >= len_union_oa / 2:
					queue_all[it]["comm"] = 2
				elif queue_all[it].get("comm") > 0:
					queue_all[it]["comm"] = 1
				else:
					queue_all[it]["comm"] = 0
			for it in range(0, len_queue):
				queue_all[it] = {
					"id": queue_all[it].get("id"),
					"rate": queue_all[it].get("rate"),
					"year": queue_all[it].get("year"),
					"score": "%s" % (
						4 * (queue_all[it].get("cate")) + 4 * queue_all[it].get("actor") + queue_all[it].get("time")
						+ queue_all[it].get("site") + queue_all[it].get("inst") + queue_all[it].get("comm")
					)
				}
			for ix in range(0, len_queue - 1):
				max_node = ix
				for iy in range(ix + 1, len_queue):
					if int(queue_all[iy].get("score")) > int(queue_all[max_node].get("score")) or \
							(int(queue_all[iy].get("score")) == int(queue_all[max_node].get("score")) and float(
								queue_all[iy].get("rate")) > float(queue_all[max_node].get("rate"))) or \
							(int(queue_all[iy].get("score")) == int(queue_all[max_node].get("score")) and float(
								queue_all[iy].get("rate")) == float(queue_all[max_node].get("rate")) and int(
								queue_all[iy].get("year")) > int(queue_all[max_node].get("year"))):
						max_node = iy
				if max_node != ix:
					temp_dict = queue_all[ix]
					queue_all[ix] = queue_all[max_node]
					queue_all[max_node] = temp_dict
			for it in range(0, len_queue):
				queue_all[it] = queue_all[it].get("id")
		table0 = []
		table1 = []
		table2 = []
		table3 = []
		table4 = []
		table5 = []
		table6 = []
		table7 = []
		item_static = coll_static.find_one({"id": id})
		item_gather = coll_gather.find_one({"id": id})
		isis0 = item_static.get('name')
		isis1 = "类型：" + item_static.get('cate').replace('#', ' ')
		isis2 = "时间：" + item_gather.get('time').replace('#', ' ')
		isis3 = "地点：" + item_gather.get('site').replace('#', ' ')
		isis4 = "组织：" + item_gather.get('inst').replace('#', ' ')
		isis5 = "评价：" + item_gather.get('comm').replace('#', ' ')
		isis6 = ("../static/image/" + id + ".jpg")
		#
		queue_len = 24
		queue_all = queue_all[:queue_len]
		list_static_name = []
		list_static_cate = []
		list_merge_ot = []
		list_merge_ns = []
		list_merge_nt = []
		list_merge_oa = []
		list_image = []
		for it in range(0, queue_len):
			item_static = coll_static.find_one({"id": queue_all[it]})
			item_gather = coll_gather.find_one({"id": queue_all[it]})
			if item_static:
				list_static_name.append(item_static.get("name"))
				list_static_cate.append("类型：" + item_static.get("cate").replace('#', ' '))
			else:
				list_static_name.append("None")
				list_static_cate.append("None")
			if item_gather:
				list_merge_ot.append(
					"时间：" + ' '.join(list(set(item_gather.get("time").split("#")).intersection(set_ot_gather)))
				)
				list_merge_ns.append(
					"地点：" + ' '.join(list(set(item_gather.get("site").split("#")).intersection(set_ns_gather)))
				)
				list_merge_nt.append(
					"组织：" + ' '.join(list(set(item_gather.get("inst").split("#")).intersection(set_nt_gather)))
				)
				list_merge_oa.append(
					"评价：" + ' '.join(list(set(item_gather.get("comm").split("#")).intersection(set_oa_gather)))
				)
			else:
				list_merge_ot.append("None")
				list_merge_ns.append("None")
				list_merge_nt.append("None")
				list_merge_oa.append("None")
			list_image.append("../static/image/" + queue_all[it] + ".jpg")
		table0.extend(queue_all)
		table1.extend(list_static_name)
		table2.extend(list_static_cate)
		table3.extend(list_merge_ot)
		table4.extend(list_merge_ns)
		table5.extend(list_merge_nt)
		table6.extend(list_merge_oa)
		table7.extend(list_image)
		if table0 and table1 and table2 and table3 and table4 and table5 and table6 and table7:
			self.render(
				"related_list.html",
				isis0=isis0,
				isis1=isis1,
				isis2=isis2,
				isis3=isis3,
				isis4=isis4,
				isis5=isis5,
				isis6=isis6,
				pins0=table0,
				pins1=table1,
				pins2=table2,
				pins3=table3,
				pins4=table4,
				pins5=table5,
				pins6=table6,
				pins7=table7
			)
		else:
			self.redirect("/related_list/")

	def post(self):
		coll_ot = self.application.db.table_ot
		coll_ns = self.application.db.table_ns
		coll_nt = self.application.db.table_nt
		coll_oa = self.application.db.table_oa
		coll_static = self.application.db.static_b
		coll_gather = self.application.db.boot_gather
		global id
		enter = self.get_argument("id")
		if enter.isdigit():
			id = enter
		else:
			entry_temp = coll_static.find_one({"name": {'$regex': '\S*' + enter + '\S*'}})
			if entry_temp:
				id = entry_temp.get('id')
		item_gather = coll_gather.find_one({"id": id})
		list_ot = item_gather.get("time").split("#")
		list_ns = item_gather.get("site").split("#")
		list_nt = item_gather.get("inst").split("#")
		list_oa = item_gather.get("comm").split("#")
		queue_all = list()
		for ot in list_ot:
			item_ot = coll_ot.find_one({"name": ot})
			if item_ot:
				queue_all.extend(item_ot.get("entry").split("/"))
		for ns in list_ns:
			item_ns = coll_ns.find_one({"name": ns})
			if item_ns:
				queue_all.extend(item_ns.get("entry").split("/"))
		for nt in list_nt:
			item_nt = coll_nt.find_one({"name": nt})
			if item_nt:
				queue_all.extend(item_nt.get("entry").split("/"))
		for oa in list_oa:
			item_oa = coll_oa.find_one({"name": oa})
			if item_oa:
				queue_all.extend(item_oa.get("entry").split("/"))
		if len(queue_all) > 0:
			temp_list = []
			for temp_it in queue_all:
				if temp_it != id:
					temp_list.append(temp_it)
			queue_all = list(set(temp_list))
			len_queue = len(queue_all)
			# 影视类型
			temp_static = coll_static.find_one({"id": id})
			set_cate_static = set(temp_static.get("cate").split("#"))
			set_actor_static = set(temp_static.get("actor").split("#"))
			set_ot_gather = set(list_ot)
			set_ns_gather = set(list_ns)
			set_nt_gather = set(list_nt)
			set_oa_gather = set(list_oa)
			for it in range(0, len_queue):
				item_static = coll_static.find_one({"id": queue_all[it]})
				item_gather = coll_gather.find_one({"id": queue_all[it]})
				queue_all[it] = {
					"id": queue_all[it],
					"cate": len(set(item_static.get("cate").split("#")).intersection(set_cate_static)),
					"actor": len(set(item_static.get("actor").split("#")).intersection(set_actor_static)),
					"time": len(set(item_gather.get("time").split("#")).intersection(set_ot_gather)),
					"site": len(set(item_gather.get("site").split("#")).intersection(set_ns_gather)),
					"inst": len(set(item_gather.get("inst").split("#")).intersection(set_nt_gather)),
					"comm": len(set(item_gather.get("comm").split("#")).intersection(set_oa_gather)),
					"rate": item_static.get("rate"),
					"year": item_static.get("year")
				}
			for it in range(0, len_queue):
				len_union_ot = len(set(item_gather.get("time").split("#")).union(set_ot_gather))
				len_union_ns = len(set(item_gather.get("site").split("#")).union(set_ns_gather))
				len_union_nt = len(set(item_gather.get("inst").split("#")).union(set_nt_gather))
				len_union_oa = len(set(item_gather.get("comm").split("#")).union(set_oa_gather))
				if queue_all[it].get("time") == len_union_ot:
					queue_all[it]["time"] = 3
				elif queue_all[it].get("time") >= len_union_ot / 2:
					queue_all[it]["time"] = 2
				elif queue_all[it].get("time") > 0:
					queue_all[it]["time"] = 1
				else:
					queue_all[it]["time"] = 0
				if queue_all[it].get("site") == len_union_ns:
					queue_all[it]["site"] = 3
				elif queue_all[it].get("site") >= len_union_ns / 2:
					queue_all[it]["site"] = 2
				elif queue_all[it].get("site") > 0:
					queue_all[it]["site"] = 1
				else:
					queue_all[it]["site"] = 0
				if queue_all[it].get("inst") == len_union_nt:
					queue_all[it]["inst"] = 3
				elif queue_all[it].get("inst") >= len_union_nt / 2:
					queue_all[it]["inst"] = 2
				elif queue_all[it].get("inst") > 0:
					queue_all[it]["inst"] = 1
				else:
					queue_all[it]["inst"] = 0
				if queue_all[it].get("comm") == len_union_oa:
					queue_all[it]["comm"] = 3
				elif queue_all[it].get("comm") >= len_union_oa / 2:
					queue_all[it]["comm"] = 2
				elif queue_all[it].get("comm") > 0:
					queue_all[it]["comm"] = 1
				else:
					queue_all[it]["comm"] = 0
			for it in range(0, len_queue):
				queue_all[it] = {
					"id": queue_all[it].get("id"),
					"rate": queue_all[it].get("rate"),
					"year": queue_all[it].get("year"),
					"score": "%s" % (
						4 * (queue_all[it].get("cate")) + 4 * queue_all[it].get("actor") + queue_all[it].get("time")
						+ queue_all[it].get("site") + queue_all[it].get("inst") + queue_all[it].get("comm")
					)
				}
			for ix in range(0, len_queue - 1):
				max_node = ix
				for iy in range(ix + 1, len_queue):
					if int(queue_all[iy].get("score")) > int(queue_all[max_node].get("score")) or \
							(int(queue_all[iy].get("score")) == int(queue_all[max_node].get("score")) and float(
								queue_all[iy].get("rate")) > float(queue_all[max_node].get("rate"))) or \
							(int(queue_all[iy].get("score")) == int(queue_all[max_node].get("score")) and float(
								queue_all[iy].get("rate")) == float(queue_all[max_node].get("rate")) and int(
								queue_all[iy].get("year")) > int(queue_all[max_node].get("year"))):
						max_node = iy
				if max_node != ix:
					temp_dict = queue_all[ix]
					queue_all[ix] = queue_all[max_node]
					queue_all[max_node] = temp_dict
			for it in range(0, len_queue):
				queue_all[it] = queue_all[it].get("id")
		table0 = []
		table1 = []
		table2 = []
		table3 = []
		table4 = []
		table5 = []
		table6 = []
		table7 = []
		item_static = coll_static.find_one({"id": id})
		item_gather = coll_gather.find_one({"id": id})
		isis0 = item_static.get('name')
		isis1 = "类型：" + item_static.get('cate').replace('#', ' ')
		isis2 = "时间：" + item_gather.get('time').replace('#', ' ')
		isis3 = "地点：" + item_gather.get('site').replace('#', ' ')
		isis4 = "组织：" + item_gather.get('inst').replace('#', ' ')
		isis5 = "评价：" + item_gather.get('comm').replace('#', ' ')
		isis6 = ("../static/image/" + id + ".jpg")
		#
		queue_len = 24
		queue_all = queue_all[:queue_len]
		list_static_name = []
		list_static_cate = []
		list_merge_ot = []
		list_merge_ns = []
		list_merge_nt = []
		list_merge_oa = []
		list_image = []
		for it in range(0, queue_len):
			item_static = coll_static.find_one({"id": queue_all[it]})
			item_gather = coll_gather.find_one({"id": queue_all[it]})
			if item_static:
				list_static_name.append(item_static.get("name"))
				list_static_cate.append("类型：" + item_static.get("cate").replace('#', ' '))
			else:
				list_static_name.append("None")
				list_static_cate.append("None")
			if item_gather:
				list_merge_ot.append(
					"时间：" + ' '.join(list(set(item_gather.get("time").split("#")).intersection(set_ot_gather)))
				)
				list_merge_ns.append(
					"地点：" + ' '.join(list(set(item_gather.get("site").split("#")).intersection(set_ns_gather)))
				)
				list_merge_nt.append(
					"组织：" + ' '.join(list(set(item_gather.get("inst").split("#")).intersection(set_nt_gather)))
				)
				list_merge_oa.append(
					"评价：" + ' '.join(list(set(item_gather.get("comm").split("#")).intersection(set_oa_gather)))
				)
			else:
				list_merge_ot.append("None")
				list_merge_ns.append("None")
				list_merge_nt.append("None")
				list_merge_oa.append("None")
			list_image.append("../static/image/" + queue_all[it] + ".jpg")
		table0.extend(queue_all)
		table1.extend(list_static_name)
		table2.extend(list_static_cate)
		table3.extend(list_merge_ot)
		table4.extend(list_merge_ns)
		table5.extend(list_merge_nt)
		table6.extend(list_merge_oa)
		table7.extend(list_image)
		if table0 and table1 and table2 and table3 and table4 and table5 and table6 and table7:
			self.render(
				"related_list.html",
				isis0=isis0,
				isis1=isis1,
				isis2=isis2,
				isis3=isis3,
				isis4=isis4,
				isis5=isis5,
				isis6=isis6,
				pins0=table0,
				pins1=table1,
				pins2=table2,
				pins3=table3,
				pins4=table4,
				pins5=table5,
				pins6=table6,
				pins7=table7
			)
		else:
			self.redirect("/related_list/")


class BaseHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"error_404.html",
		)


class EntryModule(tornado.web.UIModule):
	def render(self, entry):
		return self.render_string(
			"modules/entry.html",
			entry=entry,
		)


class ItemModule(tornado.web.UIModule):
	def render(self, item0, item1, item2):
		return self.render_string(
			"modules/item.html",
			item0=item0,
			item1=item1,
			item2=item2,
		)


class PinModule(tornado.web.UIModule):
	def render(self, pin0, pin1, pin2, pin3, pin4, pin5, pin6, pin7):
		return self.render_string(
			"modules/pin.html",
			pin0=pin0,
			pin1=pin1,
			pin2=pin2,
			pin3=pin3,
			pin4=pin4,
			pin5=pin5,
			pin6=pin6,
			pin7=pin7,
		)


if __name__ == "__main__":
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
