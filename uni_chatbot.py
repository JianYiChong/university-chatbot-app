import streamlit as st
import random
import time

# Set up the page
st.set_page_config(
    page_title="University Life Chatbot",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling and sidebar-aware sticky header
st.markdown("""
<style>
    /* Sticky header */
    .sticky-header {
        position: fixed;
        top: 40px;
        left: 0;
        right: 0;
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 15px 20px;
        z-index: 999;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        box-sizing: border-box;
    }

    /* Sidebar-aware adjustment */
    [data-testid="stSidebar"][aria-expanded="true"] ~ section .sticky-header {
        margin-left: 250px; /* Default sidebar width */
        width: calc(100% - 250px);
    }

    [data-testid="stSidebar"][aria-expanded="false"] ~ section .sticky-header {
        margin-left: 0;
        width: 100%;
    }

    /* Header content */
    .header-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .header-title {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
    }

    .header-subtitle {
        margin: 5px 0 0 0;
        font-size: 16px;
        font-weight: 400;
        opacity: 0.9;
    }

    /* Main content padding to avoid header overlap */
    .main-content {
        padding-top: 100px;
    }

    /* Chat message styling */
    .user-message-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 15px;
    }

    .user-message {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 0 18px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }

    .bot-message-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 15px;
    }

    .bot-message {
        background-color: #f0f2f6;
        color: #333;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 0;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
    }

    /* Chat container */
    .chat-container {
        padding: 1rem;
        margin-bottom: 1rem;
        max-height: 400px;
        overflow-y: auto;
        background-color: transparent;
    }

    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
        margin-bottom: 8px;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Empty state styling */
    .empty-state {
        text-align: center; 
        padding: 40px 20px; 
        color: #666;
        background-color: #f9f9f9;
        border-radius: 8px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Default responses for unknown questions
default_responses = [
    "I'm not sure I understand. Could you rephrase your question?",
    "I don't have information about that yet. Try asking about campus facilities, registration, or student life.",
    "I'm still learning about university processes. Could you ask something about library, exams, or dining?"
]

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def get_bot_response(user_input):
    """Generate a response using mock AI (if/else rules)"""
    user_input = user_input.lower()

    if "library" in user_input:
        return "The main library is located in the center of campus, next to the student union building. It's open from 8 AM to 10 PM on weekdays and 10 AM to 6 PM on weekends."
    
    elif "register" in user_input and "exam" in user_input:
        return "You can register for exams through the student portal. Go to 'Academics' > 'Exam Registration'. Make sure to register before the deadline to avoid late fees!"
    
    elif "dining" in user_input or "food" in user_input or "canteen" in user_input:
        return "We have several dining options on campus: the main cafeteria, a food court with various cuisines, a coffee shop in the library, and several snack kiosks across campus."
    
    elif "student club" in user_input or "join club" in user_input:
        return "To join a student club, visit the Student Activities Office or check out the Club Fair during orientation week. You can also browse and join clubs through the campus app."
    
    elif "housing" in user_input or "dorm" in user_input:
        return "University housing applications are available online through the student portal. The deadline for next semester is November 15th. First-year students are guaranteed housing."
    
    elif "parking" in user_input:
        return "Student parking permits can be purchased from the Campus Security office. You'll need your vehicle registration and student ID. Permits cost $150 per semester."
    
    elif "wifi" in user_input:
        return "Campus WiFi is available everywhere on campus. Connect to 'Campus-Net' and use your student credentials to login. If you have issues, contact the IT Help Desk."
    
    elif "career" in user_input:
        return "The Career Services office offers resume reviews, mock interviews, and career counseling. They're located on the 2nd floor of the Student Success Center."
    
    elif "transcript" in user_input:
        return "You can request official transcripts from the Registrar's Office. There's a small fee for each official transcript. Unofficial transcripts are available for free on the student portal."
    
    elif "tuition" in user_input or "payment" in user_input:
        return "Tuition payments can be made online through the student portal under 'Finances' > 'Make a Payment'. Payment plans are also available for eligible students."
    
    else:
        return random.choice(default_responses)

def display_chat():
    """Display the chat history without the extra container"""
    if st.session_state.chat_history:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div class='user-message-container'>
                    <div class='user-message'>
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class='bot-message-container'>
                    <div class='bot-message'>
                        {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; color: #666;">
            <h3>Hi, how can I help you?</h3>
            <p>Start a conversation by typing a question or selecting a suggested question from the sidebar.</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Sticky header
    st.markdown("""
        <div class="sticky-header">
            <div class="header-content">
                <h1 class="header-title">🎓 University Life Chatbot</h1>
                <p class="header-subtitle">Ask me anything about campus life, courses, and more!</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div class='main-content'>", unsafe_allow_html=True)
    
    # Display chat history
    display_chat()
    
    # Suggested questions in sidebar
    st.sidebar.subheader("💡 Suggested Questions")
    suggested_questions = [
        "Where is the library located?",
        "How do I register for exams?",
        "What dining options are available?",
        "How can I join a student club?",
        "What are the housing options?",
        "How do I get a parking permit?",
        "How to connect to campus WiFi?",
        "Where is career services located?"
    ]
    
    for i, question in enumerate(suggested_questions):
        if st.sidebar.button(question, key=f"suggest_{i}"):
            st.session_state.chat_history.append({'role': 'user', 'content': question})
            with st.spinner("Thinking..."):
                time.sleep(0.5)
                response = get_bot_response(question)
            st.session_state.chat_history.append({'role': 'assistant', 'content': response})
            st.rerun()
    
    # User input
    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state.chat_history.append({'role': 'user', 'content': user_input})
        with st.spinner("Thinking..."):
            time.sleep(0.5)
            response = get_bot_response(user_input)
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
