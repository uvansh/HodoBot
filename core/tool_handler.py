from langchain_core.messages import HumanMessage, AIMessage

class ToolHandler:
    def __init__(self, llm, available_functions):
        self.llm = llm
        self.functions = available_functions
        
    def execute_tools(self, question):
        response = self.llm.bind_tools(self.functions).invoke([HumanMessage(content=question)])
        
        if response.tool_calls:
            results = []
            for tool_call in response.tool_calls:
                func_name = tool_call['name']
                func_args = tool_call['args']
                
                if func_name in self.functions:
                    result = self.functions[func_name](**func_args)
                    results.append(result)
            return results
        return None