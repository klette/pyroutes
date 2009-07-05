#! /usr/bin/python
import re
import xml.dom.minidom

def process_file(filename, obj, clean = True):
	doc = xml.dom.minidom.parse(filename)
	process(doc, obj, clean)
	return doc

def process(node, obj, clean = True):
	if isinstance(obj, basestring):			# overwrite
		while not node.firstChild is None:
			node.removeChild(node.firstChild)
		doc = _get_document_element(node)
		node.appendChild(doc.createTextNode(obj))
	elif isinstance(obj, xml.dom.Node):		# overwrite
		while not node.firstChild is None:
			node.removeChild(node.firstChild)

		if isinstance(obj, xml.dom.minidom.Document):
			obj = obj.documentElement

		newobj = obj.cloneNode(True)
		node.appendChild(newobj)

		process(newobj, {}, clean)
	elif isinstance(obj, dict):			# substitute
		for child in node.childNodes:
			processed = False

			if child.nodeType == xml.dom.Node.ELEMENT_NODE:
				id = None

				attrs = child.attributes
				attrs_to_remove = []
				if not attrs is None:
					for i in range(attrs.length):
						attr = attrs.item(i)
						if attr.namespaceURI == "http://template.sesse.net/" and attr.localName == "id":
							id = attr.value
							if clean:
								attrs_to_remove.append(attr.name)
						if attr.name.startswith("xmlns:") and attr.value == "http://template.sesse.net/" and clean:
							attrs_to_remove.append(attr.name)

					for a in attrs_to_remove:
						if child.hasAttribute(a):
							child.removeAttribute(a)


				# check all substitutions to see if we found anything
				# appropriate
				for key in obj.keys():
					if key.startswith(child.tagName + "/"):
						child.setAttribute(key.split("/")[1], obj[key])
					elif (not id is None) and key.startswith("#" + id + "/"):
						child.setAttribute(key.split("/")[1], obj[key])

					if not processed:
						if key == child.localName or ((not id is None) and key == "#" + id):
							process(child, obj[key], clean)
							processed = True

			if not processed:
				process(child, obj, clean)
	elif isinstance(obj, list):			# repeat
		doc = _get_document_element(node)
		frag = doc.createElement("temporary-fragment")     # ugh

		while not node.firstChild is None:
			child = node.firstChild
			node.removeChild(child)
			frag.appendChild(child)

		for instance in obj:
			if instance is not None:
				newnode = frag.cloneNode(True)
				node.appendChild(newnode)
				process(newnode, instance, clean)
				if clean:
					_clean(newnode)

		# remove all the <fragment> tags

		children_to_remove = []
		for child in node.childNodes:
			if isinstance(child, xml.dom.minidom.Element) and child.tagName == 'temporary-fragment':
				while not child.firstChild is None:
					child2 = child.firstChild
					child.removeChild(child2)
					node.appendChild(child2)
				children_to_remove.append(child)

		for child in children_to_remove:
			node.removeChild(child)

	if clean:
		_clean(node)

def alternate(tag, array, *elems):
	i = 0
	for ref in array:
		if ref is not None:
			ref[tag] = elems[i % len(elems)]
			i = i + 1
		
	return array

def _clean(node):
	if node.nodeType == xml.dom.Node.ELEMENT_NODE and node.namespaceURI == "http://template.sesse.net/":
		# as this is a dummy node, we want to remove it and move everything further up
		# after we've done any required replacements
		doc = _get_document_element(node)
		parent = node.parentNode

		while not node.firstChild is None:
			child = node.firstChild
			node.removeChild(child)
			parent.insertBefore(child, node)

		parent.removeChild(node)

# ugh
def _get_document_element(node):
	if node.parentNode is None:
		return node
	else:
		return _get_document_element(node.parentNode)
