from rich import print
import sys
sys.path.append('./LIBS')
from WXlib import WX

from rich.console import Console
from rich.syntax import Syntax
import json

# Prompt template
prompt_template = """
<|begin_of_text|>
<|start_header_id|>system<|end_header_id|>
You always answer the questions with markdown formatting using GitHub syntax. 
The markdown formatting you support: headings, bold, italic, links, tables, lists, code blocks, 
and blockquotes. You must omit that you answer the questions with markdown.
Any HTML tags must be wrapped in block quotes, for example ```<html>```. You will be penalized 
for not rendering code in block quotes.\n\nWhen returning code blocks, specify language.
You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while 
being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, 
dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive 
in nature. If a question does not make any sense, or is not factually coherent, explain why 
instead of answering something not correct. If you don'\''t know the answer to a question, 
please don'\''t share false information.
<|eot_id|>

<|start_header_id|>user<|end_header_id|>
{{QUESTION}}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
"""

# variables to be replaced in prompt template
promptVariables = {
    'QUESTION' : "Who was the president of USA in 1999?"
}

# Set the model parameters or model name only if you want to change the model ID or its default parameters.
modelParameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 2048,
    "min_new_tokens": 0,
    "stop_sequences": [ ],
    "repetition_penalty": 1
}

model = 'meta-llama/llama-3-3-70b-instruct'


############################# generate code for display 
print("[bold yellow]### Prompt \"" + model + "\" ###[/bold yellow]")
code_example = """# import helper libs
from WXlib import WX
# instantiate wx object
wx = WX()
# Set the model parameters or model name only if you want to change the model ID or its default parameters.
modelarameters = """ + json.dumps(modelParameters, indent=4) + """

wx.wxInstModel(modelID='""" + model + """', modelParams=modelParameters)

# Set the prompt template only once if you want to change the model behavior or expected output.
promptTemplate = \"""
""" + prompt_template + """
\"""
promptVariables = {
""" + json.dumps(promptVariables, indent=4) + """
}

generated_text = wx.wxGenText(promptTemplate=promptTemplate, promptVariables=promptVariables)"""

# Use rich to apply syntax highlighting
syntax = Syntax(code_example, "python", theme="monokai", line_numbers=True)

# Print to console with rich
console = Console()
console.print(syntax)


################# EXECUTE the code 

# Instantiate the wx object only ONCE in your application.
wx = WX()
wx.wxInstModel(modelID=model, modelParams=modelParameters)
generated_text = wx.wxGenText(promptTemplate=prompt_template, promptVariables=promptVariables)

print({
    'question': promptVariables['QUESTION'],
    'answer'  : generated_text
})

