from rich import print
import sys
sys.path.append('./LIBS')
from WXlib import WX

model='meta-llama/llama-3-3-70b-instruct'
#model='meta-llama/llama-3-2-90b-vision-instruct'
#model='codellama/codellama-34b-instruct-hf'
#model='ibm/granite-34b-code-instruct'
#model='ibm/granite-20b-multilingual'
#model='meta-llama/llama-3-70b-instruct'
#model='mistralai/mistral-large'
#model='meta-llama/llama-3-405b-instruct'

print(f"[bold yellow]### Get model specs {model} ###[/bold yellow]")
from rich.console import Console
from rich.syntax import Syntax

code_example = """# import helper libs
from WXlib import WX
# instantiate wx object
wx = WX()
# read model specs
specs = wx.wxGetModelSpecs(""" + model + ")"

# Use rich to apply syntax highlighting
syntax = Syntax(code_example, "python", theme="monokai", line_numbers=True)

# Print to console with rich
console = Console()
console.print(syntax)


wx = WX()
specs = wx.wxGetModelSpecs(model)

print(specs)




