import unittest
from markdown_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(blocks, expected)


    def test_markdown_to_blocks_single(self):
        md = """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""
        blocks = markdown_to_blocks(md)
        expected = [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ]
        self.assertEqual(blocks, expected)


    #Tests for leading and trailing whitespaces
    def test_markdown_to_blocks_strip(self):
        md = """
                   This is **bolded** paragraph

      This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line                         

      - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(blocks, expected)

    #Tests for excessive newlines
    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph






This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line










- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        expected = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        self.assertEqual(blocks, expected)


class TestBlockToBlockTypeTrue(unittest.TestCase):
    
    def test_heading(self):
        input = "### Triple Heading"
        output = block_to_block_type(input)
        expected = BlockType.HEADING
        self.assertEqual(output, expected)

    def test_code(self):
        input = "```\ndef bomb(timer):\n\tif timer == 0:\n\t\tprint('Boom')\n\telse:\n\t\treturn timer - 1\n```"
        output = block_to_block_type(input)
        expected = BlockType.CODE
        self.assertEqual(output, expected)

    def test_quote(self):
        input = ">This is my quote\n>With some other quote\n> And a quote with a space at the start"
        output = block_to_block_type(input)
        expected = BlockType.QUOTE
        self.assertEqual(output, expected)

    def test_unordered_list(self):
        input = "- Firstly\n- Secondly\n- Thirdly"
        output = block_to_block_type(input)
        expected = BlockType.UNORDERED_LIST
        self.assertEqual(output, expected)
    
    def test_ordered_list(self):
        input = "1. Firstly\n2. Secondly\n3. Thirdly"
        output = block_to_block_type(input)
        expected = BlockType.ORDERED_LIST
        self.assertEqual(output, expected)

    def test_paragraph(self):
        input = "This is a paragraph"
        output = block_to_block_type(input)
        expected = BlockType.PARAGRAPH
        self.assertEqual(output, expected)

class TestBlockToBlockTypeFalse(unittest.TestCase):
    
    def test_heading(self):
        input = "####### Triple Heading"
        output = block_to_block_type(input)
        expected = BlockType.HEADING
        self.assertNotEqual(output, expected)

    def test_code(self):
        input = "````\ndef bomb(timer):\n\tif timer == 0:\n\t\tprint('Boom')\n\telse:\n\t\treturn timer - 1\n```"
        output = block_to_block_type(input)
        expected = BlockType.CODE
        self.assertNotEqual(output, expected)

    def test_quote(self):
        input = ">This is my quote\n>With some other quote\n< And a quote with a space at the start"
        output = block_to_block_type(input)
        expected = BlockType.QUOTE
        self.assertNotEqual(output, expected)

    def test_unordered_list(self):
        input = "- Firstly\n- Secondly\n-Thirdly"
        output = block_to_block_type(input)
        expected = BlockType.UNORDERED_LIST
        self.assertNotEqual(output, expected)
    
    def test_ordered_list(self):
        input = "1. Firstly\n2. Secondly\n4. Thirdly"
        output = block_to_block_type(input)
        expected = BlockType.ORDERED_LIST
        self.assertNotEqual(output, expected)

    def test_paragraph(self):
        input = "# This is not a paragraph"
        output = block_to_block_type(input)
        expected = BlockType.PARAGRAPH
        self.assertNotEqual(output, expected)


class TestBlockToBlockTypeSolution(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNodeEach(unittest.TestCase):

    def test_paragraph(self):
        input = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
"""
        node = markdown_to_html_node(input)
        output = node.to_html()
        expected = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(output, expected)

    def test_heading(self):
        input_heading = """
        ### Triple header
        """
        node_heading = markdown_to_html_node(input_heading)
        html = node_heading.to_html()
        output_heading = "<div><h3>Triple header</h3></div>"
        self.assertEqual(html, output_heading)

    def test_code(self):
        input_code = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node_code = markdown_to_html_node(input_code)
        html = node_code.to_html()
        output_code = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>"
        self.assertEqual(html, output_code)

    def test_quote(self):
        input = ">This is my quote\n>With some other quote\n> And a quote with a space at the start"
        node = markdown_to_html_node(input)
        html = node.to_html()
        output = "<div><blockquote>This is my quote With some other quote And a quote with a space at the start</blockquote></div>"
        self.assertEqual(html, output)

    def test_unordered_list(self):
        input = """
- Item 1
- Item 2
- Item 3
"""
        node = markdown_to_html_node(input)
        html = node.to_html()
        output = "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>"
        self.assertEqual(html, output)

    def test_ordered_list(self):
        input = """
1. Item 1
2. Item 2
3. Item 3
"""
        node = markdown_to_html_node(input)
        html = node.to_html()
        output = "<div><ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol></div>"
        self.assertEqual(html, output)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


class TestMarkdownToHtmlSolution(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )