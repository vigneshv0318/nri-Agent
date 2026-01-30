import os
import json
import re
from typing import Annotated, TypedDict, List
from fastapi import APIRouter, Form
from pydantic import BaseModel
import database
from dotenv import load_dotenv

load_dotenv()

# LangChain / LangGraph Imports
# LangChain / LangGraph Imports
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator

router = APIRouter()
database.init_db()

# --- 1. Define Tools ---

from duckduckgo_search import DDGS

@tool
def search_youtube(query: str, language: str = "English"):
    """Searches for a relevant video story. 
    Provide the language to get localized results.
    Returns the video URL inside a [VIDEO: url] tag."""
    try:
        refined_query = f"{query} {language} backstory cartoon for kids Strictly no violence"
        with DDGS() as ddgs:
            results = ddgs.videos(refined_query, max_results=1)
            if results:
                video = results[0]
                video_url = video.get('content') or video.get('href')
                return f"[VIDEO: {video_url}]"
            return f"No {language} video found for {query}."
    except Exception as e:
        return f"Video Search Error: {str(e)}"

@tool
def search_image(query: str, language: str = "Indian"):
    """Searches for a cartoon celebration image. 
    Returns the image URL inside an [IMAGE: url] tag."""
    try:
        refined_query = f"{query} {language} festival celebration cartoon kid friendly"
        with DDGS() as ddgs:
            results = ddgs.images(refined_query, max_results=1)
            if results:
                img = results[0]
                img_url = img.get('image')
                return f"[IMAGE: {img_url}]"
            return f"No {language} image found for {query}."
    except Exception as e:
        return f"Image Search Error: {str(e)}"

@tool
def update_user_score(username: str, points: str, stamp: str = None):
    """Updates points. Only for correct answers."""
    try:
        if isinstance(points, str):
            pts_str = ''.join(c for c in points if c.isdigit())
            pts = int(pts_str) if pts_str else 0
        else:
            pts = int(points)
    except:
        pts = 0
    result = database.update_score(username, pts, stamp)
    return json.dumps(result)

@tool
def get_festival_content(festival_name: str):
    """Retrieves educational context/story for a festival."""
    data = {
        "pongal": "Pongal is a harvest festival of Tamil Nadu, thanking the Sun God and cattle.",
        "diwali": "Diwali (Deepavali) is the festival of lights, celebrating the return of Lord Rama and the victory of light.",
        "onam": "Onam is the harvest festival of Kerala, welcoming King Mahabali with beautiful floral Pookalam.",
        "ugadi": "Ugadi is the Telugu and Kannada New Year, celebrated with Pachadi—a dish of six tastes representing life's emotions.",
        "holi": "Holi is the festival of colors, celebrating spring and the triumph of Prahlada over Holika.",
        "navratri": "Navratri celebrates the nine forms of Goddess Durga over nine nights of dance and prayer.",
        "puthandu": "Puthandu is the Tamil New Year, marked by mango pachadi and family gatherings.",
        "ganesh": "Ganesh Chaturthi celebrates the birth of Lord Ganesha, the remover of obstacles.",
        "vishu": "Vishu is the Malayalam New Year, where families look at 'Vishukkani'—a setting of auspicious items.",
        "thaipusam": "Thaipusam is a Tamil festival honoring Lord Murugan's victory over evil."
    }
    
    fn = festival_name.lower()
    for k in data:
        if k in fn or fn in k:
            return f"Story Context: {data[k]}"
    return f"I can find the story of {festival_name} for you using my search tools!"

@tool
def get_relevant_festival(language: str):
    """Returns a list of appropriate festivals for the given language."""
    mapping = {
        "tamil": ["Pongal", "Deepavali", "Puthandu", "Thaipusam", "Karthigai Deepam"],
        "hindi": ["Diwali", "Holi", "Navratri", "Ganesh Chaturthi", "Durga Puja"],
        "malayalam": ["Onam", "Vishu"],
        "telugu": ["Ugadi", "Sankranti", "Bonalu", "Deepavali"],
        "kannada": ["Dasara", "Ugadi", "Deepavali"]
    }
    return mapping.get(language.lower(), ["Deepavali", "Holi"])

tools = [update_user_score, get_festival_content, search_youtube, get_relevant_festival, search_image]

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    username: str

# Initialize Model
llm = ChatGroq(
    groq_api_key=os.environ.get("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b"
).bind_tools(tools)

# Define Nodes
def agent_node(state: AgentState):
    return {"messages": [llm.invoke(state["messages"])]}

tool_node = ToolNode(tools)

# Define Logic for Conditional Edges
def should_continue(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "action"
    return END

# Build Graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("action", tool_node)

workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("action", "agent")

app_graph = workflow.compile()

# --- 3. API Endpoint ---

def get_system_prompt(language: str):
    if language.lower() == "tamil":
        persona, style = "Ammachi", "Tanglish"
    elif language.lower() == "hindi":
        persona, style = "Dadi", "Hinglish"
    else:
        persona, style = "Grandma", "English"

    return f"""Role: {persona}, a warm Grandma. 👵 Heritage: {language} ({style}).

Operation:
1. Greet child.
2. List festivals using 'get_relevant_festival'. STOP & WAIT.
3. Once festival picked, use 'get_festival_content', 'search_image', and 'search_youtube'.
4. Include tool media outputs [IMAGE:...] and [VIDEO:...] EXACTLY.
5. Challenge child. Give points/stamp via 'update_user_score' ONLY if correct.
6. Ask a question. Award 10 points/stamp with 'update_user_score' if correct.
7. Use tanglish/hinglish/english based on language.
8. Use many emojie and bullet points to make it more engaging.

RULES:
- NEVER type tool names or internal code like {{...}} or <...>.
- Speak ONLY warm conversation. No "I am searching" talk.
- Dont use too much selected language, use simple language with mix of {language} and English.
- Include media tags ONCE at the start of original story."""

class CultureResponse(BaseModel):
    response: str
    points: int
    stamps: List[str]

@router.post("/chat", response_model=CultureResponse)
def chat_culture(
    message: str = Form(...),
    history: str = Form(...),
    username: str = Form("student"),
    language: str = Form("Tamil")
):
    # Rehydrate History
    try:
        raw_history = json.loads(history)
    except:
        raw_history = []
    
    # Dynamic System Prompt
    system_prompt = get_system_prompt(language)
    messages = [SystemMessage(content=system_prompt)]
    messages.append(SystemMessage(content=f"Context: User '{username}', Language '{language}'."))

    # Aggressive scrubbing of technical artifacts
    def scrub_technical_bits(text: str) -> str:
        # 1. Remove { "function": "...", ... } pattern (and similar JSON leaks)
        text = re.sub(r'\{[^{]*"function":\s*"[^"]*"[^{]*\}', '', text, flags=re.DOTALL)
        # 2. Remove actual tool name calls if leaked as text
        text = re.sub(r'\{[a-zA-Z0-9_]+\s*\{[^}]*\}\}', '', text)
        # 3. Remove LangChain/OpenAI style JSON blocks
        text = re.sub(r'\{[^{]*"name":\s*"[^"]*"[^{]*"parameters":\s*\{[^}]*\}', '', text, flags=re.DOTALL)
        # 4. Remove XML style tags
        text = re.sub(r'<function.*?>.*?</function>', '', text, flags=re.DOTALL)
        text = re.sub(r'<tool.*?>.*?</tool>', '', text, flags=re.DOTALL)
        # 5. Remove dangling artifacts
        text = re.sub(r'<function.*', '', text)
        text = re.sub(r'\{[a-zA-Z0-9_]+\s*\{.*', '', text)
        return text.strip()

    for msg in raw_history:
        clean_content = scrub_technical_bits(msg['content'])
        if not clean_content: continue

        if msg['role'] == 'user':
            messages.append(HumanMessage(content=clean_content))
        elif msg['role'] == 'assistant':
            messages.append(AIMessage(content=clean_content))
            
    messages.append(HumanMessage(content=message))

    # Run Graph
    try:
        inputs = {"messages": messages, "username": username}
        final_state = app_graph.invoke(inputs)
        
        last_msg = final_state["messages"][-1]
        response_text = scrub_technical_bits(last_msg.content)

        print(f"DEBUG: Agent Response: {response_text[:100]}...")

        # Fetch latest user stats
        user_data = database.get_user(username)

        return CultureResponse(
            response=response_text,
            points=user_data['points'],
            stamps=user_data['stamps']
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        return CultureResponse(
            response=f"Agent Error: {str(e)}",
            points=0,
            stamps=[]
        )
