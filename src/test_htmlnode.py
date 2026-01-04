# src/test_htmlnode.py

import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_init(self):
        node = HTMLNode("div", "Hello", [], {"class": "my-class"})
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {"class": "my-class"})

    def test_props_to_html(self):
        node = HTMLNode(props={"id": "header", "class": "main-header"})
        props_html = node.props_to_html()
        self.assertIn(' id="header"', props_html)
        self.assertIn(' class="main-header"', props_html)

    def test_props_to_html_exact(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        result = node.props_to_html()
        # Order-sensitive check
        self.assertEqual(
            result,
            ' href="https://example.com" target="_blank"',
        )
        
    def test_repr(self):
        node = HTMLNode("span", "Text", None, {"style": "color:red;"})
        expected_repr = "HTMLNode(tag='span', value='Text', children=None, props={'style': 'color:red;'})"
        self.assertEqual(repr(node), expected_repr)

    def test_raw_html_leaf_node(self):
        leaf = LeafNode(tag=None, value="Just some text")
        self.assertEqual(leaf.to_html(), "Just some text")

    def test_html_leaf_node_with_no_props(self):
        leaf = LeafNode(tag="b", value="Bold Text")
        expected_html = "<b>Bold Text</b>"
        self.assertEqual(leaf.to_html(), expected_html)
    
    def test_html_leaf_node_with_tag(self):
        leaf = LeafNode(tag="p",
                        value="This is a paragraph.",
                        props={"class": "text"})
        expected_html = '<p class="text">This is a paragraph.</p>'
        self.assertEqual(leaf.to_html(), expected_html)

    def test_html_leaf_node_missing_value(self):
        leaf = LeafNode(tag="span", value=None)
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_parent_node_html(self):
        child1 = LeafNode(tag="li", value="Item 1")
        child2 = LeafNode(tag="li", value="Item 2")
        parent = ParentNode(tag="ul", children=[child1, child2])
        expected_html = "<ul><li>Item 1</li><li>Item 2</li></ul>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    def test_html_parent_node_with_props(self):
        child = LeafNode(tag="a",
                         value="Link",
                         props={"href": "https://example.com"})
        parent = ParentNode(tag="div",
                            children=[child],
                            props={"class": "container"})
        expected_html = '<div class="container"><a href="https://example.com">Link</a></div>'
        self.assertEqual(parent.to_html(), expected_html)

    def test_html_child_no_tag(self):
        child = LeafNode(tag=None, value="No tag here")
        parent = ParentNode(tag="div", children=[child])
        expected_html = "<div>No tag here</div>"
        self.assertEqual(parent.to_html(), expected_html)

    def test_html_parent_node_missing_tag(self):
        child = LeafNode(tag="p", value="Paragraph")
        parent = ParentNode(tag=None, children=[child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_html_parent_node_missing_children(self):
        parent = ParentNode(tag="div", children=None)
        with self.assertRaises(ValueError):
            parent.to_html()