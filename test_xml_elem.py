from game_info_mgr import GameInfoMgr
from xml.etree.ElementTree import tostring, Element

g_inf_mgr = GameInfoMgr()

print(g_inf_mgr.get_attrib_list())

g_inf_mgr.set_attrib_val("name", "test")

print(tostring(g_inf_mgr.gen_xml_node()))

test = Element("gameList")

test.append(g_inf_mgr.gen_xml_node())

print(tostring(test))
