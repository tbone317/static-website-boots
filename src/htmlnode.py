# src/htmlnode.py

from typing import Dict, List, Optional

class HTMLNode:
    def __init__(self, 
                 tag: Optional[str] = None
                 , value: Optional[str] = None
                 , children: Optional[List["HTMLNode"]] = None
                 , props: Optional[Dict[str, str]] = None
                 ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if not self.props:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children={self.children!r}, "
            f"props={self.props!r})"
        )

class LeafNode(HTMLNode):
    def __init__(self, 
                 tag: str | None,
                 value: str | None,
                 props: Optional[Dict[str, str]] = None,
                 ):
        super().__init__(tag=tag, 
                         value=value, 
                         children=None, 
                         props=props)
    
    def to_html(self):
        if self.value is None and self.tag != "img":
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        props_html = self.props_to_html()
        if self.tag == "img":
            return f"<{self.tag}{props_html} />"
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self,
                 tag: str,
                 children: List[HTMLNode],
                 props: Optional[Dict[str, str]] = None,
                 ):
        super().__init__(tag=tag,
                         value=None,
                         children=children,
                         props=props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None:
            raise ValueError("ParentNode must have children.")
        props_html = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"