# src/test_textnode.py

import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD.value)
        node2 = TextNode("This is a different text node", TextType.BOLD.value)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.ITALIC.value)
        node2 = TextNode("This is a text node", TextType.ITALIC.value)
        self.assertEqual(node, node2)

    def test_url(self):
        node = TextNode("Click here", TextType.LINK.value, url="http://example.com")
        node2 = TextNode("Click here", TextType.LINK.value, url="http://example.com")
        self.assertEqual(node, node2)

if __name__ == "__main__":
    unittest.main()