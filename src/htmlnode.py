class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
    )

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def props_to_html(self):
        if not self.props:
            return ""
        else:
            props = ""
            for key, value in self.props.items():
               props += f' {key}="{value}"'
        return props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, value, None, props)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list["HTMLNode"],
        props: dict[str, str] | None = None,
    ):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("there needs to be a tag")
        if not self.children:
            raise ValueError("there needs to be a child")
        else:
            inner = "".join(child.to_html() for child in self.children)
            return f"<{self.tag}{self.props_to_html()}>{inner}</{self.tag}>"

