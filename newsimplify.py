# Import necessary libraries
import os
import re
import json
from dotenv import load_dotenv # For managing environment variables
from groq import Groq # For accessing Llama model through Groq's API
import websearch # Custom module/tool/function for web search functionality
from article import extract_article # Custom module/tool/function to extract articles
import streamlit as st # Streamlit for building the web UI

# Load environment variables from .env file
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define available tools for the assistant
tools = {
    "search_web": websearch.search_web, # Function to search for articles
    "extract_article": extract_article, # Function to extract article details
}

# Function to detect tool calls in assistant's response
def detect_tool_call(response):
    pattern = r"<function=(.*?)>{(.*?)}<\/function>"
    match = re.search(pattern, response, re.DOTALL)
    if match:
        tool_name = match.group(1).strip()
        arguments = match.group(2).strip()
        return tool_name, arguments
    return None, None

# Function to format tool outputs for the assistant's response
def format_tool_output(tool_output):
    if isinstance(tool_output, str):
        return tool_output
    elif isinstance(tool_output, list):
        # Format the list of articles
        formatted = ""
        for idx, article in enumerate(tool_output, 1):
            formatted += f"{idx}. {article['title']}\n"
            formatted += f"   Source: {article['source']}\n"
            formatted += f"   Link: {article['href']}\n\n"
        return formatted.strip()
    elif isinstance(tool_output, dict): # Extracted article content
        if tool_output.get("error"):
            return f"Error extracting article: {tool_output['error']}"
        else:
            return tool_output.get("text", "")
    else:
        return str(tool_output)

# Function to interact with the Llama 3.3-70B LLM (Groq API)
def LLMinf(messages):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion

# Function to initialize Streamlit session state variables
def initialize_session_state():
    """
    Initializes session state variables for Streamlit.
    Sets up the system prompt and message history.
    """
    if "messages" not in st.session_state:
        # System prompt
        system_prompt = (
        "Environment: python\n"
        "Tools: search_web, extract_article\n"
        "Cutoff Knowledge Date: December 2023\n"
        "Current Date: 30 December 2024\n"
        "\n"
        "# Tool Instructions\n"
        "- When the user provides a topic, use the function 'search_web' to fetch the top 3 news articles.\n"
        "- Always use the tool to fetch the articles; do not generate the articles yourself.\n"
        "- After recieving the tool output, format and show the output (article titles, links, and sources) to the user and ask the user to select any one of them to know more about.\n"
        "- When the user selects an article (by providing its number or title), use the function 'extract_article' to extract the article text.\n"
        "- After receiving the extracted article text from the function, summarize the article and present the summary to the user in your next response.\n"
        "- After presenting the summary of the article ask questions to the user if they are interested in any other topic or if they have any follow up questions within that article."
        "- Answers to the follow up questions by the user should be from the article. Don't make up new answers if the information is not present in the article."
        "- If you choose to call a function, ONLY reply in the following format:\n"
        "<function=function_name>{\"argument_name\": \"argument_value\"}</function>\n"
        "\n"
        "Here are examples:\n"
        "1. To search for articles:\n"
        "<function=search_web>{\"topic\": \"artificial intelligence\"}</function>\n"
        "2. To extract an article:\n"
        "<function=extract_article>{\"url\": \"https://example.com/article\"}</function>\n"
        "\n"
        "Reminder:\n"
        "- Function calls MUST follow the specified format.\n"
        "- Required parameters MUST be specified.\n"
        "- Only call one function at a time.\n"
        "- Put the entire function call reply on one line.\n"
        "- After receiving the tool output, proceed to the next step in the interaction flow.\n"
        "\n"
        "You are a helpful assistant called NEWSimplify. Greet the user and ask for a topic they want to know more about.\n"
        "Do NOT call any tool until the user provide a topic."
    )
        st.session_state.messages = [{"role": "system", "content": system_prompt}]
        st.session_state.articles_list = []
        process_assistant_response()

# Function to process the assistant's response
def process_assistant_response():
    """
    Processes the assistant's response and handles tool calls if detected.
    """
   
    completion = LLMinf(st.session_state.messages)
    assistant_message = completion.choices[0].message.content
    # Append assistant message to conversation history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
    print('')
    print('')
    print('****************************************************************************')
    print(f"Assistant: {assistant_message}")

    # Check if the assistant has requested a tool call
    tool_name, arguments = detect_tool_call(assistant_message)
    if tool_name:
        print('')
        print('****************************************************************************')
        print(f"Tool requested: {tool_name} with arguments: {arguments}")

        try:
            arguments = json.loads("{" + arguments + "}")
        except json.JSONDecodeError as e:
            print(f"Error parsing arguments: {e}")
            return

        if tool_name in tools:
            # Execute the tool and format the output
            tool_output = tools[tool_name](**arguments)
            formatted_output = format_tool_output(tool_output)
            print("Tool output:\n" + formatted_output)
            
            # Store articles list if search_web was used
            if tool_name == "search_web":
                st.session_state.articles_list = tool_output

             # Append tool output to the conversation
            st.session_state.messages.append({"role": "function", "name": tool_name, "content": formatted_output})
            
            # Get follow-up from assistant after tool execution
            completion = LLMinf(st.session_state.messages)
            assistant_message = completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
            print('')
            print('')
            print('****************************************************************************')
            print(f"Assistant: {assistant_message}")
        else:
            print(f"Error: Tool '{tool_name}' is not available.")

# Function to handle user input
def handle_user_input(user_input):
    """
    Handles user input, detects article selections, and processes responses.
    """
    print(f"User Input: {user_input}")
    # User typed a message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Handle article selection if user inputs a number
    if user_input.isdigit() and st.session_state.articles_list:
        selected_index = int(user_input) - 1
        if 0 <= selected_index < len(st.session_state.articles_list):
            selected_article = st.session_state.articles_list[selected_index]
            extract_function_call = f"<function=extract_article>{{\"url\": \"{selected_article['href']}\"}}</function>"
            print(f"Assistant: {extract_function_call}")
            st.session_state.messages.append({"role": "assistant", "content": extract_function_call})
            process_assistant_response()
        else:
            st.warning("Invalid selection. Please try again.")
    else:
        
        process_assistant_response()

# Streamlit UI Setup
st.title("NEWSimplify 📰")

# Initialize session state
initialize_session_state()

# Display the conversation history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='text-align: right; background-color: #DCF8C6; color: black; border-radius: 10px; padding: 10px; margin: 5px;'>
                <b>You:</b> {msg['content']}
            </div>
            """, unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        # Skip function call messages
        if not re.search(r"<function=.*?>", msg["content"]):
            st.markdown(
                f"""
                <div style='text-align: left; background-color: #E6E6FA; color: black; border-radius: 10px; padding: 10px; margin: 5px;'>
                    <b>Assistant:</b> {msg['content']}
                </div>
                """, unsafe_allow_html=True)

# Input box for user interaction
user_query = st.text_input("Your message:", key="user_input")

# Handle user input when "Send" button is clicked
if st.button("Send") and user_query.strip() != "":
    handle_user_input(user_query.strip())
    st.rerun()
