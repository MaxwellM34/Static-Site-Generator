import unittest
from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, None)
        self.assertEqual(node, node2)


    def test_diff(self):
        node = HTMLNode("a")
        node2 = HTMLNode()
        self.assertNotEqual(node, node2)

    def test_children(self):
        child = HTMLNode("b", "bold")
        parent = HTMLNode("p", None, [child])
        self.assertEqual(parent.children[0].tag, "b")
        self.assertEqual(parent.children[0].value, "bold")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h2(self):
        node = LeafNode("h2", "Hello, world!")
        self.assertEqual(node.to_html(), "<h2>Hello, world!</h2>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

