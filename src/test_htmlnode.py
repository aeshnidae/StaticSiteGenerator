import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
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
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

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

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child", {"class": "highlight"})
        parent_node = ParentNode("div", [child_node], {"id": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="container"><span class="highlight">child</span></div>',
        )
    
    def test_to_html_with_props_child_noprops(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"id": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="container"><span>child</span></div>'
        )

    def test_to_html_mixed_props_children(self):
        child_node = LeafNode("b", "child0")
        child_node2 = LeafNode("span", "child",{"class": "highlight"})
        child_node3 = LeafNode("p", "hello")
        parent_node = ParentNode("div",[child_node,child_node2,child_node3],{"id": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="container"><b>child0</b><span class="highlight">child</span><p>hello</p></div>'
        )

    def test_to_html_nested_parents(self):
        child_node = LeafNode("p","im a child")
        parent_node = ParentNode("div",[child_node],{"id": "container"})
        grandparent_node = ParentNode("span", [parent_node],{"class": "highlight"})
        self.assertEqual(
            grandparent_node.to_html(),
            '<span class="highlight"><div id="container"><p>im a child</p></div></span>'
        )

    def test_to_html_with_grandchildren_with_props(self):
        grandchild_node = LeafNode("b", "grandchild",{"class": "highlight"})
        child_node = ParentNode("span", [grandchild_node], {"id": "container"})
        parent_node = ParentNode("div", [child_node],{"href": "https://www.google.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.google.com"><span id="container"><b class="highlight">grandchild</b></span></div>'
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )
    

if __name__ == "__main__":
    unittest.main()
