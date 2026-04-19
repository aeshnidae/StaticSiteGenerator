
class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        if self.props == None:
            return ""
        result = ""
        for item in self.props:
            result += f" {item}=\"{self.props[item]}\""
        return result
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    
    def __eq__(self, other):
        return (
			self.tag == other.tag
			and self.value == other.value
			and self.children == other.children
            and self.props == other.props)
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return str(self.value)
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("invalid HTML: no tag")
        if self.children == None:
            raise ValueError("invalid HTML: no children")
        
        result = ""

        for child in self.children:
            result += child.to_html()
     
        return f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"

