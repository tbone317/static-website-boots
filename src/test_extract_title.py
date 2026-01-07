import unittest
from inline_markdown import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        """Test extracting a simple h1 title"""
        md = "# Hello"
        result = extract_title(md)
        self.assertEqual(result, "Hello")
    
    def test_extract_title_with_whitespace(self):
        """Test extracting title with leading and trailing whitespace"""
        md = "#   Hello World   "
        result = extract_title(md)
        self.assertEqual(result, "Hello World")
    
    def test_extract_title_with_content_below(self):
        """Test extracting title when there's content below"""
        md = "# My Title\n\nSome paragraph text\n\n## Subtitle"
        result = extract_title(md)
        self.assertEqual(result, "My Title")
    
    def test_extract_title_with_multiple_lines(self):
        """Test extracting title from markdown with multiple lines"""
        md = """# Tolkien Fan Club

![JRR Tolkien sitting](/images/tolkien.png)

Here's the deal, **I like Tolkien**."""
        result = extract_title(md)
        self.assertEqual(result, "Tolkien Fan Club")
    
    def test_extract_title_ignores_h2_headers(self):
        """Test that h2 headers are ignored"""
        md = "## Not H1\n\n# This is H1"
        result = extract_title(md)
        self.assertEqual(result, "This is H1")
    
    def test_extract_title_ignores_h3_headers(self):
        """Test that h3 headers are ignored"""
        md = "### Not H1\n\n# Actual Title"
        result = extract_title(md)
        self.assertEqual(result, "Actual Title")
    
    def test_extract_title_no_h1_raises_exception(self):
        """Test that exception is raised when no h1 is found"""
        md = "## Only H2\n\n### Only H3\n\nSome paragraph"
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_extract_title_empty_markdown_raises_exception(self):
        """Test that exception is raised for empty markdown"""
        md = ""
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertEqual(str(context.exception), "No h1 header found in markdown")
    
    def test_extract_title_no_space_after_hash(self):
        """Test that #NoSpace doesn't match as h1"""
        md = "#NoSpace\n\n# Correct Title"
        result = extract_title(md)
        self.assertEqual(result, "Correct Title")
    
    def test_extract_title_with_special_characters(self):
        """Test extracting title with special characters"""
        md = "# Hello, World! @#$%"
        result = extract_title(md)
        self.assertEqual(result, "Hello, World! @#$%")


if __name__ == "__main__":
    unittest.main()
