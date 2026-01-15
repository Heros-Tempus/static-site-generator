import unittest
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_links,
    extract_markdown_images
)
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with **bolded words**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("bolded words", TextType.BOLD)
            ],
            new_nodes
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes
        )

    def test_delim_italic(self):
        node = TextNode("This is text with _italic words_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with ", TextType.TEXT),
                TextNode("italic words", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC)
            ],
            new_nodes
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT)
            ],
            new_nodes
        )

    def test_extract_markdown_images(self):
        github_profile = "https://avatars.githubusercontent.com/u/20712274?v=4"
        matches = extract_markdown_images(
            f"This is text with an ![image]({github_profile})"
        )
        self.assertListEqual([("image", github_profile)], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://google.com) and [another link](https://bing.com)"
        )
        self.assertListEqual(
            [
                ("link", "https://google.com"),
                ("another link", "https://bing.com"),
            ],
            matches
        )

    def test_split_images(self):
        github_profile = "https://avatars.githubusercontent.com/u/20712274?v=4"
        google_logo = "https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg"
        node = TextNode(
            f"This is text with an ![image]({github_profile}) and another ![second image]({google_logo})",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, github_profile),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, google_logo)
            ],
            new_nodes
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://google.com) and [another link](https://bing.com) with text that follows",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://bing.com"),
                TextNode(" with text that follows", TextType.TEXT)
            ],
            new_nodes
        )

    def test_text_to_textnodes(self):
        github_profile = "https://avatars.githubusercontent.com/u/20712274?v=4"
        nodes = text_to_textnodes(
            f"This is **text** with an _italic_ word and a `code block` and an ![image]({github_profile}) and a [link](https://google.com)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, github_profile),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com")
            ],
            nodes
        )

if __name__ == "__main__":
    unittest.main()
