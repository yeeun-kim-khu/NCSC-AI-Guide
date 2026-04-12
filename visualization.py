# visualization.py
import streamlit as st
import graphviz
from typing import Dict, List, Optional

def create_architecture_diagram() -> graphviz.Digraph:
    """
    LLM-based Active Scientific Principle Exploration Architecture Diagram
    """
    dot = graphviz.Digraph(comment='LLM Architecture', 
                          format='png',
                          engine='dot',
                          graph_attr={'rankdir': 'LR',
                                    'bgcolor': 'white',
                                    'fontname': 'Malgun Gothic',
                                    'fontsize': '12'})
    
    # Node styles
    dot.attr('node', shape='box', style='rounded,filled', fontname='Malgun Gothic')
    
    # User
    dot.node('U', 'User\n(Users)', 
             fillcolor='lightblue', 
             shape='ellipse')
    
    # LLM Core Process
    with dot.subgraph(name='cluster_llm') as llm:
        llm.attr(label='LLM Core Process', 
                style='filled', 
                fillcolor='lightgray',
                color='gray')
        
        llm.node('P', 'Prompt\n(Prompt)', 
                 fillcolor='lightyellow')
        llm.node('T', 'Thought\n(Intent Analysis\n& Reasoning)', 
                 fillcolor='lightgreen')
        llm.node('A', 'Action\n(Tool Selection)', 
                 fillcolor='lightcoral')
        llm.node('RT', 'Retrieve Tools\n(Tool Execution)', 
                 fillcolor='lightsalmon')
        llm.node('O', 'Observation\n(Result Confirmation)', 
                 fillcolor='lightpink')
        llm.node('FA', 'Final Answer\n(Customized Answer\n& Follow-up)', 
                 fillcolor='lavender')
    
    # Data Sources
    with dot.subgraph(name='cluster_data') as data:
        data.attr(label='Data Sources', 
                 style='filled', 
                 fillcolor='#E6F3FF',
                 color='blue')
        
        data.node('RAG', 'RAG\n(Vector DB)', 
                  fillcolor='lightcyan')
        data.node('REAL', 'Real-time\nInformation\nCollection', 
                  fillcolor='lightcyan')
    
    # Connections - User to LLM
    dot.edge('U', 'P', label='Question', color='red', fontcolor='red')
    dot.edge('FA', 'U', label='Answer', color='blue', fontcolor='blue')
    
    # LLM Internal Flow
    dot.edge('P', 'T', color='red', fontcolor='red')
    dot.edge('T', 'A', color='red', fontcolor='red')
    dot.edge('A', 'RT', color='red', fontcolor='red')
    dot.edge('RT', 'RAG', color='red', fontcolor='red', style='dashed')
    dot.edge('RT', 'REAL', color='red', fontcolor='red', style='dashed')
    dot.edge('RAG', 'O', color='blue', fontcolor='blue')
    dot.edge('REAL', 'O', color='blue', fontcolor='blue')
    dot.edge('O', 'T', color='blue', fontcolor='blue', label='Feedback')
    dot.edge('O', 'FA', color='blue', fontcolor='blue')
    
    return dot

def create_process_flow_diagram(current_step: str = None) -> graphviz.Digraph:
    """
    Dynamic process flow showing current execution state
    """
    dot = graphviz.Digraph(comment='Process Flow',
                          format='png',
                          engine='dot',
                          graph_attr={'rankdir': 'TB',
                                    'bgcolor': 'white',
                                    'fontname': 'Malgun Gothic'})
    
    steps = [
        ('Q', 'User Question', 'lightblue'),
        ('T', 'Thought', 'lightgreen'),
        ('A', 'Action', 'lightcoral'),
        ('E', 'Execute Tools', 'lightsalmon'),
        ('O', 'Observation', 'lightpink'),
        ('F', 'Final Answer', 'lavender')
    ]
    
    for step_id, step_name, color in steps:
        if current_step == step_id:
            dot.node(step_id, step_name, 
                     fillcolor=color, 
                     shape='box',
                     style='filled,bold',
                     penwidth='3')
        else:
            dot.node(step_id, step_name, 
                     fillcolor=color, 
                     shape='box',
                     style='rounded,filled')
    
    # Flow connections
    dot.edge('Q', 'T')
    dot.edge('T', 'A')
    dot.edge('A', 'E')
    dot.edge('E', 'O')
    dot.edge('O', 'T', label='Iterate')
    dot.edge('O', 'F')
    
    return dot

def render_architecture_section():
    """
    Render the architecture visualization section in Streamlit
    """
    st.markdown("## LLM-based Active Scientific Principle Exploration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Architecture Overview")
        
        # Create and display architecture diagram
        try:
            diagram = create_architecture_diagram()
            st.graphviz_chart(diagram)
        except Exception as e:
            st.error(f"Architecture diagram rendering failed: {e}")
            st.info("Please install graphviz: `pip install graphviz`")
    
    with col2:
        st.markdown("### Process Components")
        
        components = {
            "**User**": "Questions and receives answers",
            "**Prompt**": "Initial input to LLM",
            "**Thought**": "Intent analysis & reasoning",
            "**Action**": "Search tool selection",
            "**Retrieve Tools**": "Tool execution",
            "**Observation**": "Result confirmation",
            "**Final Answer**": "Customized response",
            "**RAG**": "Vector database search",
            "**Real-time**": "Live data collection"
        }
        
        for component, description in components.items():
            st.markdown(f"- {component}: {description}")
        
        st.markdown("### Key Features")
        st.markdown("- **Iterative Process**: Thought-Action-Observation loop")
        st.markdown("- **Multi-source**: RAG + Real-time data")
        st.markdown("- **Context-aware**: Dynamic prompt adjustment")
        st.markdown("- **User-centric**: Personalized responses")

def render_process_flow(current_step: Optional[str] = None):
    """
    Render the dynamic process flow
    """
    st.markdown("### Current Process Flow")
    
    try:
        flow_diagram = create_process_flow_diagram(current_step)
        st.graphviz_chart(flow_diagram)
    except Exception as e:
        st.error(f"Process flow rendering failed: {e}")

def get_step_explanation(step: str) -> str:
    """
    Get explanation for each step in the process
    """
    explanations = {
        'Q': "User asks a question about the science museum",
        'T': "LLM analyzes the question and determines what information is needed",
        'A': "LLM selects appropriate tools (RAG search, web crawling, etc.)",
        'E': "Tools are executed to gather information",
        'O': "LLM observes results and evaluates if more information is needed",
        'F': "LLM generates final answer based on all gathered information"
    }
    
    return explanations.get(step, "Unknown step")
