import xml.etree.ElementTree as ET

print("starting to read....")
xml_file = open("/exports/projects/msc_students_2014/ljingyun/marker/ena.xml").read()  #str

xml_str = ET.fromstring(xml_file)
print(".... finished reading")

tax_node = xml_str.getiterator("entry") 
for node in tax_node:
	for node2 in node.getchildren():
		
		if node2.tag=="feature":
			
			node3=node2.getchildren()
			if node3[0].attrib.has_key("taxId") > 0:
				print '>' + node3[0].attrib['taxId']
		if node2.tag=="sequence":
			print node2.text
					   
