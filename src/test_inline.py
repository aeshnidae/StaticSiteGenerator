import unittest
from textnode import TextNode, TextType
from inline import(
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,

)

class TestInline(unittest.TestCase):
    def test_single_delimiter(self):
        node = TextNode("This is a text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        check = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, check)

    def test_single_delimiter_first(self):
        node = TextNode("**This** is a text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        check = [
            TextNode("This", TextType.BOLD),
            TextNode(" is a text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, check)

    def test_multiple_delimiter(self):
        node = TextNode("This is a text with a **bold phrase** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        check = [
            TextNode("This is a text with a ", TextType.TEXT),
            TextNode("bold phrase", TextType.BOLD),
            TextNode(" in it", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, check)

    def test_invalid_bad_delimiter(self):
        node = TextNode("This is a text with a **bold phrase in it", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: delimiters does not match")
        
    def test_multiple_phrases(self):
        node = TextNode("This is a text **with** multiple **bold** words", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        check = [
            TextNode("This is a text ", TextType.TEXT),
            TextNode("with", TextType.BOLD),
            TextNode(" multiple ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, check)

    def test_with_multiple_nodes(self):
        old_node1 = TextNode("First node", TextType.BOLD)
        old_node2 = TextNode("Second **bold** node", TextType.TEXT)
        old_node3 = TextNode("Third _italic_ node", TextType.ITALIC)
        node = [old_node1, old_node2, old_node3]
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        check = [
            TextNode("First node", TextType.BOLD),
            TextNode("Second ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" node", TextType.TEXT),
            TextNode("Third _italic_ node", TextType.ITALIC)

        ]
        self.assertEqual(new_nodes, check)




class TestInlineFromSolutions(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
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
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


class TestRegex(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_not_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([], matches)

    def test_not_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([], matches)

class TestSplitNodes(unittest.TestCase):

    # Testing images
    def test_image_no_image(self):
        node = TextNode("Hello", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("Hello", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_image_split_single(self):
        node = TextNode("![image](https://www.boot.dev/img/bootdev-logo-full-150.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/img/bootdev-logo-full-150.png")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_image_split_multiple(self):
        node = TextNode("![image1](https://www.boot.dev/logo1.png)![image2](https://www.boot.dev/logo2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("image1", TextType.IMAGE, "https://www.boot.dev/logo1.png"),
            TextNode("image2", TextType.IMAGE, "https://www.boot.dev/logo2.png")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_image_split_text_left(self):
        node = TextNode("Text from the left side ![image](https://www.boot.dev/logo.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("Text from the left side ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/logo.png")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_image_split_text_right(self):
        node = TextNode("![image](https://www.boot.dev/logo.png) Text from the right side", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/logo.png"),
            TextNode(" Text from the right side", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_images_split_text_between(self):
        node = TextNode("![image](https://www.boot.dev/logo.png) Text between images ![image2](https://www.boot.dev/logo2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/logo.png"),
            TextNode(" Text between images ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://www.boot.dev/logo2.png")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_images_split_text_before_in_after(self):
        node = TextNode("Text before image ![image](https://www.boot.dev/logo.png) Text between images ![image2](https://www.boot.dev/logo2.png) Text after images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("Text before image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/logo.png"),
            TextNode(" Text between images ", TextType.TEXT),
            TextNode("image2", TextType.IMAGE, "https://www.boot.dev/logo2.png"),
            TextNode(" Text after images", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_images_split_before_after(self):
        node = TextNode("Text before image ![image](https://www.boot.dev/logo.png)![image2](https://www.boot.dev/logo2.png) Text after images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        answer = [
            TextNode("Text before image ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://www.boot.dev/logo.png"),
            TextNode("image2", TextType.IMAGE, "https://www.boot.dev/logo2.png"),
            TextNode(" Text after images", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    # Testing links
    def test_link_no_link(self):
        node = TextNode("Hello", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("Hello", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_link_split_single(self):
        node = TextNode("[link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_link_split_multiple(self):
        node = TextNode("[link1](https://www.boot.dev)[link2](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("link1", TextType.LINK, "https://www.boot.dev"),
            TextNode("link2", TextType.LINK, "https://www.google.com")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_link_split_text_left(self):
        node = TextNode("Text from the left side [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("Text from the left side ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_link_split_text_right(self):
        node = TextNode("[link](https://www.boot.dev) Text from the right side", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" Text from the right side", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_links_split_text_between(self):
        node = TextNode("[link1](https://www.boot.dev) Text between links [link2](https://www.google.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("link1", TextType.LINK, "https://www.boot.dev"),
            TextNode(" Text between links ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://www.google.com")
        ]
        self.assertListEqual(new_nodes, answer)

    def test_links_split_text_before_in_after(self):
        node = TextNode("Text before link [link1](https://www.boot.dev) Text between links [link2](https://www.google.com) Text after links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("Text before link ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://www.boot.dev"),
            TextNode(" Text between links ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "https://www.google.com"),
            TextNode(" Text after links", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)

    def test_links_split_before_after(self):
        node = TextNode("Text before link [link1](https://www.boot.dev)[link2](https://www.google.com) Text after links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        answer = [
            TextNode("Text before link ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "https://www.boot.dev"),
            TextNode("link2", TextType.LINK, "https://www.google.com"),
            TextNode(" Text after links", TextType.TEXT)
        ]
        self.assertListEqual(new_nodes, answer)
    

class TestSplitNodesSolution(unittest.TestCase):

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://wikipedia.org) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://wikipedia.org"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

class TestTextToTextnodes(unittest.TestCase):
    
    def test_text_to_textnodes_mix(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        output = text_to_textnodes(input)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(output, expected)

    def test_text_to_textnodes_justtext(self):
        input = "Some text"
        output = text_to_textnodes(input)
        expected = [
            TextNode("Some text", TextType.TEXT)
        ]
        self.assertListEqual(output, expected)

    def test_text_to_textnodes_empty(self):
        input = ""
        output = text_to_textnodes(input)
        expected = []
        self.assertListEqual(output, expected)

    def test_text_to_textnodes_whitespace(self):
        input = " "
        output = text_to_textnodes(input)
        expected = [
            TextNode(" ", TextType.TEXT)
        ]
        self.assertListEqual(output, expected)

    def test_text_to_textnodes_no_text(self):
        input = "**text**_italic_`code block`![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)[link](https://boot.dev)"
        output = text_to_textnodes(input)
        expected = [
            TextNode("text", TextType.BOLD),
            TextNode("italic", TextType.ITALIC),
            TextNode("code block", TextType.CODE),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(output, expected)

    def test_text_to_textnodes_multiple_bolds(self):
        input = "**some****bold****text****only**"
        output = text_to_textnodes(input)
        expected = [
            TextNode("some", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode("text", TextType.BOLD),
            TextNode("only", TextType.BOLD)
        ]
        self.assertListEqual(output, expected)


if __name__ == "__main__":
    unittest.main()