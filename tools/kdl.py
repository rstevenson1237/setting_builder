"""The KDL subset the framework uses: nodes, string/identifier/integer values, properties,
children, and // comments."""
import re

TOKEN = re.compile(r'''
    (?P<ws>[ \t]+) | (?P<comment>//[^\n]*) | (?P<nl>\n|;) | (?P<open>\{) | (?P<close>\}) |
    (?P<eq>=) | (?P<str>"(?:[^"\\\n]|\\.)*") | (?P<int>-?\d+(?![\w.])) |
    (?P<ident>[^\s\\/(){};\[\]"#=]+)
''', re.X)


class Node:
    def __init__(self, name, line):
        self.name, self.line, self.args, self.props, self.children = name, line, [], {}, []

    def __repr__(self):
        return f"Node({self.name!r}, {self.args}, {self.props}, {self.children})"


def tokens(text, line=1):
    pos = 0
    while pos < len(text):
        m = TOKEN.match(text, pos)
        if not m:
            raise SyntaxError(f"line {line}: unexpected {text[pos]!r}")
        kind = m.lastgroup
        if kind not in ("ws", "comment"):
            yield kind, m.group(), line
        line += m.group().count("\n")
        pos = m.end()


def value(kind, raw):
    if kind == "str":
        return re.sub(r'\\(.)', r'\1', raw[1:-1])
    return int(raw) if kind == "int" else raw


def parse(text, line=1):
    root, stack, node, key = [], [], None, None
    level = root
    for kind, raw, line in tokens(text, line):
        if key is not None and kind in ("nl", "open", "close", "eq"):
            raise SyntaxError(f"line {line}: property {key!r} has no value")
        if kind == "nl":
            node = None
        elif kind == "open":
            if node is None:
                raise SyntaxError(f"line {line}: '{{' with no node")
            stack.append(level)
            level, node = node.children, None
        elif kind == "close":
            if not stack:
                raise SyntaxError(f"line {line}: unmatched '}}'")
            level, node = stack.pop(), None
        elif kind == "eq":
            if node is None or not node.args or node.args[-1][0] == "int":
                raise SyntaxError(f"line {line}: '=' with no property name")
            key = value(*node.args.pop())
        elif node is None:
            if kind == "int":
                raise SyntaxError(f"line {line}: node name {raw!r} is a number")
            node = Node(value(kind, raw), line)
            level.append(node)
        elif key is not None:
            node.props[key], key = value(kind, raw), None
        else:
            node.args.append((kind, raw))
    if stack:
        raise SyntaxError("unclosed '{'")
    for n in walk(root):
        n.args = [value(k, r) for k, r in n.args]
    return root


def walk(nodes):
    for n in nodes:
        yield n
        yield from walk(n.children)


def fenced(text):
    """The nodes of every ```kdl fence in a markdown text, with file line numbers."""
    out, lines, start = [], text.splitlines(), None
    for i, line in enumerate(lines):
        if start is None and line.strip() == "```kdl":
            start = i + 1
        elif start is not None and line.strip() == "```":
            out += parse("\n".join(lines[start:i]), start + 1)
            start = None
    if start is not None:
        raise SyntaxError(f"line {start}: unclosed ```kdl fence")
    return out


BARE = re.compile(r'[^\s\\/(){};\[\]"#=0-9-][^\s\\/(){};\[\]"#=]*')


def show(v):
    if isinstance(v, int) or BARE.fullmatch(v):
        return str(v)
    return '"' + v.replace("\\", "\\\\").replace('"', '\\"') + '"'


def dump(n):
    """A node and its children on one line."""
    parts = [show(n.name)] + [show(a) for a in n.args] + [f"{k}={show(v)}" for k, v in n.props.items()]
    if n.children:
        parts.append("{ " + "; ".join(dump(c) for c in n.children) + " }")
    return " ".join(parts)
