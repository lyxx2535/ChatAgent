import ast
import operator
from .base import BaseTool

class CalculatorTool(BaseTool):
    """
    计算器工具 - 执行数学计算
    支持基本的四则运算、幂运算、括号等
    """
    
    def __init__(self):
        super().__init__(
            name="Calculator",
            description="执行数学计算。支持加减乘除、幂运算、括号等。例如: '2 + 2', '10 * (5 + 3)', '2 ** 8'"
        )
        
        # 定义允许的运算符
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.USub: operator.neg,  # 负号
        }
    
    def _eval_expr(self, node):
        """安全地评估 AST 节点"""
        if isinstance(node, ast.Constant):  # Python 3.8+
            return node.value
        elif isinstance(node, ast.Num):  # Python 3.7-
            return node.n
        elif isinstance(node, ast.BinOp):
            left = self._eval_expr(node.left)
            right = self._eval_expr(node.right)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"不支持的运算符: {type(node.op).__name__}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_expr(node.operand)
            op = self.operators.get(type(node.op))
            if op is None:
                raise ValueError(f"不支持的一元运算符: {type(node.op).__name__}")
            return op(operand)
        else:
            raise ValueError(f"不支持的表达式类型: {type(node).__name__}")
    
    def run(self, query: str) -> str:
        """
        执行数学计算
        
        参数:
            query: 数学表达式字符串，如 "2 + 2" 或 "10 * (5 + 3)"
        
        返回:
            计算结果的字符串表示
        """
        try:
            # 清理输入
            query = query.strip()
            
            # 使用 AST 安全解析表达式
            tree = ast.parse(query, mode='eval')
            result = self._eval_expr(tree.body)
            
            # 格式化输出
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            return f"计算结果: {query} = {result}"
            
        except SyntaxError:
            return f"错误: 无效的数学表达式 '{query}'"
        except ZeroDivisionError:
            return "错误: 除数不能为零"
        except ValueError as e:
            return f"错误: {str(e)}"
        except Exception as e:
            return f"计算出错: {str(e)}"

