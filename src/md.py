from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            nodes.append(node)
            continue

        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:            
            raise Exception("Something is wrong with delimeters")

        for i , part, in enumerate(parts):
            if not part:
                continue
            if i % 2 != 0:
                nodes.append(TextNode(part, text_type))
                
            else:
                nodes.append(TextNode(part, TextType.TEXT))
    return nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
           new_nodes.append(node)
           continue
        images = extract_markdown_images(node.text)
        splt = re.split(r'(!\[.*?\]\(.*?\))', node.text)
        i = 0
        for text in splt:
            if not text:
                continue
            if text[0] == "!":
                new_nodes.append(TextNode(re.search(r"(?<=!\[)[^\[\]]*(?=\])", text).group(), TextType.IMAGE, re.search(r"(?<=\]\()[^\(\)]*(?=\))", text).group()))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        splt = re.split(r'((?<!!)\[.*?\]\(.*?\))', node.text)
        for text in splt:
            if not text:
                continue
            if re.fullmatch(r"\[[^\[\]]*\]\([^\(\)]*\)", text):
                new_nodes.append(TextNode(re.search(r"(?<=\[)[^\[\]]*(?=\])", text).group(), TextType.LINK, re.search(r"(?<=\]\()[^\(\)]*(?=\))", text).group()))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes   


    """
node = TextNode(
    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
    TextType.TEXT,
)
new_nodes = split_nodes_link([node])
# [
#     TextNode("This is text with a link ", TextType.TEXT),
#     TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
#     TextNode(" and ", TextType.TEXT),
#     TextNode(
#         "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
#     ),
# ]





# images
r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"

# regular links
r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"



text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
print(extract_markdown_images(text))
# [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]












    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

[
    TextNode("This is text with a ", TextType.TEXT),
    TextNode("code block", TextType.CODE),
    TextNode(" word", TextType.TEXT),
]
    """
