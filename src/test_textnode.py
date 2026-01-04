# src/test_textnode.py

import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter

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


class TestSplitNodesDelimiter(unittest.TestCase):
    """Test the split_nodes_delimiter function"""
    
    def test_split_code_delimiter(self):
        """Test splitting with backtick delimiter for code"""
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_bold_delimiter(self):
        """Test splitting with ** delimiter for bold"""
        node = TextNode("This is text with a **bolded phrase** in the middle", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bolded phrase", TextType.BOLD),
            TextNode(" in the middle", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_italic_delimiter(self):
        """Test splitting with _ delimiter for italic"""
        node = TextNode("This is text with _italicized text_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        expected = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("italicized text", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_multiple_delimiters(self):
        """Test splitting text with multiple occurrences of delimiter"""
        node = TextNode("first `code` and second `code` block", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("first ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and second ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_split_non_text_nodes_ignored(self):
        """Test that non-TEXT type nodes are not split"""
        node = TextNode("This is bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Non-TEXT nodes should pass through unchanged
        self.assertEqual(new_nodes, [node])
    
    def test_split_mixed_nodes(self):
        """Test splitting a list with both TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and `code here` in text", TextType.TEXT),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code here", TextType.CODE),
            TextNode(" in text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_start(self):
        """Test delimiter at the start of text"""
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_at_end(self):
        """Test delimiter at the end of text"""
        node = TextNode("ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_missing_closing_delimiter(self):
        """Test error on unclosed delimiter"""
        node = TextNode("This has `unclosed code", TextType.TEXT)
        
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertIn("unclosed delimiter", str(context.exception))
    
    def test_empty_delimited_content(self):
        """Test with empty content between delimiters"""
        node = TextNode("text with `` empty code and `real` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode(" empty code and ", TextType.TEXT),
            TextNode("real", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_delimiter_only(self):
        """Test with only delimiter content"""
        node = TextNode("`code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)
    
    def test_chained_delimiters(self):
        """Test calling split_nodes_delimiter multiple times"""
        node = TextNode("text with `code` and **bold** content", TextType.TEXT)
        
        # First split by backticks for code
        nodes_after_code = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Then split by ** for bold
        nodes_after_bold = split_nodes_delimiter(nodes_after_code, "**", TextType.BOLD)
        
        expected = [
            TextNode("text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" content", TextType.TEXT),
        ]
        self.assertEqual(nodes_after_bold, expected)

if __name__ == "__main__":
    unittest.main()