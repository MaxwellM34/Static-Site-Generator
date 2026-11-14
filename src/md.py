from textnode import TextNode, TextType
import re
from enum import Enum

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

def markdown_to_blocks(markdown):
    blocks = []
    for block in markdown.split("\n\n"):
        block = "\n".join(line.strip() for line in block.split("\n")).strip()
        blocks.append(block)
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("*", "**", "***", "****", "*****", "******")):
        return BlockType.HEADING
    if block.startswith("```/n") and block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
       return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                children.append(paragraph_to_html_node(block))
            case BlockType.CODE:
                children.append(code_to_html_node(block))
            case BlockType.HEADING:
                children.append(heading_to_html_node(block))
            case BlockType.QUOTE:
                children.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                children.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                children.append(ordered_list_to_html_node(block))
            case _:
                raise ValueError(f"invalid block type {block_type}")
    return ParentNode("div", children)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]

def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    children = text_to_children(text)
    return ParentNode("p", children)

def heading_to_html_node(block):
    num = len(block) - len(block.lstrip("#"))
    tag = f"h{num}"
    children = text_to_children(block[num + 1:])
    return ParentNode(tag, children)
 
 def code_to_html_node(block):
    text = block[4:-3]
    child = ParentNode("code", [text_node_to_html_node(TextNode(text, TextType.TEXT))])
    return ParentNode("pre", [child])

def unordered_list_to_html_node(block):
    children = []
    for line in block.split("\n"):
        grandchildren = text_to_children(line[2:])
        children.append(ParentNode("li", grandchildren))
    return ParentNode("ul", children)


    



                            
   


###test

    

'''

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url}) 
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"unknown text type: {text_node.text_type}")


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
'''
