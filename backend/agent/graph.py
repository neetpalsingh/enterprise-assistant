from typing import Literal
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
from agent.state import AgentState
from tools.business_tools import get_all_tools
from llm.models import LLMFactory
import logging

logger = logging.getLogger(__name__)

try:
    from rag.rag_tool import get_rag_tool
    RAG_AVAILABLE = True
except ImportError as e:
    logger.warning(f"RAG dependencies not installed: {e}")
    RAG_AVAILABLE = False
except Exception as e:
    logger.warning(f"RAG initialization failed: {e}")
    RAG_AVAILABLE = False

def get_system_prompt():
    base_prompt = """You are an enterprise AI assistant designed to help with business operations.

You have access to the following capabilities:
- Create support tickets for issues and requests
- Fetch employee information and list employees by department
- Check ticket status and list open tickets
- Generate business reports (employee summaries, ticket summaries)"""

    if RAG_AVAILABLE:
        base_prompt += "\n- Search knowledge base for policies, compliance, procedures, and documented information"

    base_prompt += """

When a user asks a question:
1. Understand their intent
2. Use appropriate tools to gather information or perform actions
3. Provide clear, professional responses"""

    if RAG_AVAILABLE:
        base_prompt += " with source citations when using knowledge base"

    base_prompt += """
4. If you need to create a ticket or perform an action, confirm what you're doing

Be helpful, concise, and professional. Always use tools when appropriate rather than making up information."""

    if RAG_AVAILABLE:
        base_prompt += "\nWhen citing knowledge base sources, always mention the source file names."

    return base_prompt

SYSTEM_PROMPT = get_system_prompt()

class EnterpriseAgent:
    def __init__(self, llm_provider: str = "openai", model_name: str = None):
        self.llm = LLMFactory.create_llm(provider=llm_provider, model_name=model_name)
        self.tools = get_all_tools()

        if RAG_AVAILABLE:
            try:
                self.tools.append(get_rag_tool())
                logger.info("RAG tool enabled")
            except Exception as e:
                logger.warning(f"Failed to add RAG tool: {e}")
        else:
            logger.info("RAG tool disabled (dependencies not installed)")

        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.memory = MemorySaver()
        self.graph = self._create_graph()
    
    def _create_graph(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("agent", self._call_model)
        workflow.add_node("tools", ToolNode(self.tools))
        
        workflow.set_entry_point("agent")
        
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {
                "continue": "tools",
                "end": END
            }
        )
        
        workflow.add_edge("tools", "agent")
        
        return workflow.compile(checkpointer=self.memory)
    
    def _call_model(self, state: AgentState):
        messages = state["messages"]
        
        if not any(isinstance(msg, SystemMessage) for msg in messages):
            messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(messages)
        
        response = self.llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
    def _should_continue(self, state: AgentState) -> Literal["continue", "end"]:
        messages = state["messages"]
        last_message = messages[-1]
        
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "continue"
        return "end"
    
    def run(self, question: str, thread_id: str = "default"):
        config = {"configurable": {"thread_id": thread_id}}
        
        result = self.graph.invoke(
            {"messages": [HumanMessage(content=question)]},
            config=config
        )
        
        return result["messages"][-1].content
