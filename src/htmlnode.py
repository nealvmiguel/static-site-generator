class HTMLNode:
    """
    Represents a generic node in an HTML document structure.

    Attributes:
        tag (str, optional): The HTML tag (e.g., 'div', 'p', 'a').
        value (str, optional): The text value or content inside the HTML element.
        children (list[HTMLNode], optional): A list of child HTMLNode instances representing nested elements.
        props (dict, optional): A dictionary of HTML attributes (e.g., {"class": "my-class", "href": "#"}).

    Methods:
        to_html(): Abstract method intended to return a string representation of the node in HTML format.
        props_to_html(): Converts the props dictionary into a string of HTML attributes.
    """

    def __init__(self, tag=None, value=None, children=None, props=None) -> None:
        """
        Initializes an HTMLNode instance.

        Parameters:
            tag (str, optional): The HTML tag name.
            value (str, optional): The textual value or content.
            children (list[HTMLNode], optional): List of child HTMLNode objects.
            props (dict, optional): A dictionary of HTML attributes.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode into an HTML string.

        This method must be implemented by subclasses. It is currently abstract.

        Raises:
            NotImplementedError: This method is intended to be overridden.
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Converts the props dictionary into a string suitable for HTML attributes.

        Returns:
            str: A space-separated string of HTML attributes.
                 Example: 'class="my-class" id="main"'
        """
        if self.props is None:
            return ""

        string = ""

        for attribute, value in self.props.items():
            string += f'{attribute}="{value}" '

        return string.strip()

    def __repr__(self) -> str:
        """
        Returns a string representation of the HTMLNode instance.

        Returns:
            str: Readable representation showing tag, value, children, and props.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    """
    Represents a leaf node in an HTML document, which contains only a value
    and does not have any child nodes.

    Inherits from:
        HTMLNode

    Attributes:
        tag (str): The HTML tag (e.g., 'p', 'span', 'h1').
        value (str): The text or inner HTML content.
        props (dict, optional): HTML attributes for the element.

    Methods:
        to_html(): Returns the HTML string for this node.
    """

    def __init__(self, tag, value, props=None):
        """
        Initializes a LeafNode instance.

        Parameters:
            tag (str): The HTML tag name.
            value (str): The content inside the tag.
            props (dict, optional): A dictionary of HTML attributes.
        """
        super().__init__(tag, value, None, props)

    def to_html(self):
        """
        Converts the LeafNode to an HTML string.

        Returns:
            str: The HTML representation of the node.

        Raises:
            ValueError: If the value is None (leaf nodes must have content).
        """
        
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        if self.props:
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

        return f"<{self.tag}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    
class ParentNode(HTMLNode):
    """
    Represents an HTML node that contains child nodes.

    This class is used for elements that wrap other elements or text,
    like <div>, <ul>, or <section>.

    Inherits from:
        HTMLNode

    Attributes:
        tag (str): The HTML tag name (e.g., 'div', 'ul').
        children (list[HTMLNode]): A list of child HTMLNode instances.
        props (dict, optional): A dictionary of HTML attributes.

    Methods:
        to_html(): Converts the node and its children into an HTML string.
    """

    def __init__(self, tag, children, props=None) -> None:
        """
        Initializes a ParentNode instance.

        Parameters:
            tag (str): The HTML tag name.
            children (list[HTMLNode]): List of child HTMLNode objects.
            props (dict, optional): HTML attributes for the tag.
        """
        super().__init__(tag, None, children, props)

    def to_html(self):
        """
        Converts the ParentNode and its children into an HTML string.

        Returns:
            str: The HTML string representing the tag and its children.

        Raises:
            ValueError: If tag is missing or children are not provided.
        """
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")

        if self.children is None or len(self.children) == 0:
            raise ValueError("invalid HTML: no children")

        html_children = ""

        for child in self.children:
            html_children += child.to_html()

        # Add a space before attributes only if props exist
        props_str = f" {self.props_to_html()}" if self.props else ""

        return f"<{self.tag}{props_str}>{html_children}</{self.tag}>"

    def __repr__(self) -> str:
        return f"ParentNode({self.tag}, children: {self.children}, props: {self.props})"
