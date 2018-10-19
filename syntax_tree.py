from typing import List, TypeVar

class IdNode(object):
    dtype: int = None
    value: str = None
    def __init__(self, dtype: int, value: str):
        self.dtype = dtype
        self.value = value

class ParametersNode(object):
    parameters: List[IdNode] = None
    def __init__(self, parameters: List[IdNode]):
        self.parameters = parameters

class FuncCallNode(object):
    value: str = None
    parameters: ParametersNode = None
    def __init__(self, value: str, parameters: ParametersNode):
        self.value = value
        self.parameters = parameters

class LiteralNode(object):
    dtype: int = None
    value: str = None
    def __init__(self, dtype: int, value: str):
        self.dtype = dtype
        self.value = value

class BinaryExpressionNode(object):
    dtype: int = None
    operator: int = None
    left = None
    right = None
    def __init__(self, dtype: int, operator: int, left, right):
        self.dtype = dtype
        self.operator = operator
        self.left = left
        self.right = right

class UnaryExpressionNode(object):
    dtype: int = None
    operator: int = None
    id_node: IdNode
    def __init__(self, dtype: int, operator: int, id_node: IdNode):
        self.dtype = dtype
        self.operator = operator
        self.id_node = id_node

class DeclarationNode(object):
    dtype: int = None
    value: str = None
    def __init__(self, dtype: int, value: str):
        self.dtype = dtype
        self.value = value

class DeclarationsNode(object):
    declarations: List[DeclarationNode] = None
    def __init__(self, declarations: List[DeclarationNode]):
        self.declarations = declarations

Value = TypeVar('Value', IdNode, LiteralNode, FuncCallNode)
ExpressionNode = TypeVar('Expression', Value, BinaryExpressionNode, UnaryExpressionNode)
class AssNode(object):
    left: IdNode = None
    right: ExpressionNode
    def __init__(self, left: IdNode, right: ExpressionNode):
        self.left = left
        self.right = right

class WhileNode(object):
    boolean: IdNode = None
    body = None
    def __init__(self, boolean: IdNode, body):
        self.boolean = boolean
        self.body = body

class IfNode(object):
    boolean: IdNode = None
    body = None
    def __init__(self, boolean: IdNode, body):
        self.boolean = boolean
        self.body = body

StatementNode = TypeVar('StatementNode', IfNode, WhileNode, AssNode)
class BodyNode(object):
    statements = None
    def __init__(self, statements):
        self.statements = statements

class ReturnNode(object):
    dtype: int = None
    value: str = None
    def __init__(self, dtype: int, value: str):
        self.dtype = dtype
        self.value = value

class FuncNode(object):
    arguments: DeclarationsNode = None
    declarations: DeclarationsNode = None
    body: BodyNode = None
    return_statement: ReturnNode = None
    def __init__(self, arguments: DeclarationsNode, declarations: DeclarationsNode, body: BodyNode, return_statement: ReturnNode):
        self.arguments = arguments
        self.body = body
        self.return_statement = return_statement

class MainNode(object):
    declarations: DeclarationsNode = None
    body: BodyNode = None
    def __init__(self, declarations: DeclarationsNode, body: BodyNode):
        self.declarations = declarations
        self.body = body

class FileNode(object):
    functions: List[FuncNode] = None
    def __init__(self, functions: List[FuncNode], main: MainNode):
        self.functions = functions
        self.main = main
