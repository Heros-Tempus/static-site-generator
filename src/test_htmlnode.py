import unittest
from htmlnode import LeafNode, ParentNode, HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "html props",
            None,
            {"class": "test", "href": "https://google.com"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="test" href="https://google.com"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "This is a node",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "This is a node",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "repr test",
            None,
            {"class": "test"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, repr test, children: None, {'class': 'test'})",
        )

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "to link test", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">to link test</a>'
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "no tag test")
        self.assertEqual(node.to_html(), "no tag test")

    def test_to_html_with_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                LeafNode("b", "Bold text")
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><i>italic text</i>Normal text<b>Bold text</b></p>",
        )
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("p", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><p>grandchild</p></span></div>",
        )

if __name__ == "__main__":
    unittest.main()
