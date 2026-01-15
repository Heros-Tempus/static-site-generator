import unittest
from generate_page import extract_header

class TestGeneratePage(unittest.TestCase):
    def test_extract_header(self):
        md = extract_header("# Header\n\n## Footer")
        self.assertEqual(md, "Header")
        
    def test_no_header(self):
        with self.assertRaises(ValueError) as e:
            extract_header("No Header")
        self.assertEqual(e.exception.args[0], "No h1 header found in markdown")

    def test_no_h1_header(self):
        with self.assertRaises(ValueError) as e:
            extract_header("## H2\n\n### H3\n\n#### H4\n\n##### H5\n\n###### H6")
        self.assertEqual(e.exception.args[0], "No h1 header found in markdown")


if __name__ == "__main__":
    unittest.main()