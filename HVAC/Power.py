import lxml.html
import lxml.etree
import requests
import logging

MTU1 = "MTU1_KW"
MTU2 = "MTU2_KW"
MTU3 = "MTU3_KW"
MTU4 = "MTU4_KW"

logger = logging.getLogger(__name__)

def status():
	result = {
		MTU1:0,
		MTU2:0,
		MTU3:0,
		MTU4:0
	}
	page = requests.get("http://192.168.1.124/stats.htm")
#   logger.debug(page.content)
	tree = lxml.html.fromstring(page.content)
	table = tree.xpath("/html/body/center/table[1]/*[text()]")
	for element in table:
		el = element.findall("*")
#		logger.debug(el)
		for item in el:
			logger.debug(item.text)
			if item.text == "Power:":
				result[MTU1] = int(el[1].text)
				result[MTU2] = int(el[2].text)
				result[MTU3] = int(el[3].text)
				result[MTU4] = int(el[4].text)
				return result
	return result
'''
	# these code snippets print out the whole XML tree as element/text pairs
	html = lxml.html.parse(url)
	for element in html.iter():
		print("%s - %s" % (element.tag, element.text))
	texts = html.xpath("//text()")
	for text in texts:
		parent = text.getparent();
		print( parent.tag, text );


	page = requests.get("http://192.168.1.124/stats.htm")
	tree = html.fromstring(page.content)
	table = tree.xpath("/html/body/center/table[1]")
	print(table[0])
	return
	rows = iter(table)
	logger.debug(table)
	headers = [col.text for col in row]
	for row in rows:
		values = [col.text for col in row]
		logger.debug(dict(zip(headers,values)))
	logger.debug(result)
	return
'''
