import unittest
from generate_page import extract_title


class TestGeneratePage(unittest.TestCase):
    
    def test_extract_title(self):
        markdown = """# This is an heading"""
        
        value = extract_title(markdown)
        
        self.assertEqual(value, "This is an heading")
        
    def test_extract_title_whitespace(self):
        
        markdown = """#      This is an heading"""
        
        value = extract_title(markdown)
        
        self.assertEqual(value, "This is an heading")

    def test_extract_title_no_heading_markdown(self):
        
        with self.assertRaises(ValueError):
            markdown = """This is an heading"""
            extract_title(markdown)
            

if __name__ == '__main__':
    unittest.main()