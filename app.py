import groq
import streamlit as st
from typing import List, Dict

# Initialize Groq client
groq_client = groq.Groq(api_key="api")

class HiringAssistant:
    def __init__(self):
        self.conversation_history = []
        self.candidate_info = {
            'name': None,
            'email': None,
            'phone': None,
            'experience': None,
            'position': None,
            'location': None,
            'tech_stack': None
        }
        self.current_question = 'name'
        self.technical_questions = []
        self.current_tech_question = 0
        self.technical_phase = False
        self.follow_up_phase = False
        
    def get_llm_response(self, prompt: str) -> str:
        completion = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": """You are a professional hiring assistant conducting initial screening interviews. Follow these guidelines:
                1. Ask only one question at a time.
                2. Keep responses concise and clear.
                3. Be professional and polite.
                4. After getting an answer, store it and move to the next question.
                5. Generate technical questions only after collecting all basic information."""},
                *self.conversation_history,
                {"role": "user", "content": prompt}
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
        )
        return completion.choices[0].message.content

    def get_next_question(self) -> str:
        questions = {
            'name': "Hello! Welcome to the initial screening interview. Could you please provide your full name?",
            'email': "Thank you. What is your email address?",
            'phone': "Could you please share your phone number?",
            'experience': "How many years of professional experience do you have?",
            'position': "What position(s) are you interested in applying for?",
            'location': "What is your current location?",
            'tech_stack': "Please list your technical skills, including programming languages, frameworks, databases, and tools you're proficient in.",
            'complete': "Thank you for providing all the information. Now I'll ask some technical questions based on your tech stack."
        }
        return questions.get(self.current_question, "")

    def update_current_question(self):
        question_order = ['name', 'email', 'phone', 'experience', 'position', 'location', 'tech_stack', 'complete']
        current_index = question_order.index(self.current_question)
        if current_index < len(question_order) - 1:
            self.current_question = question_order[current_index + 1]

    def generate_technical_questions(self, tech_stack: str) -> list:
        prompt = f"""Based on the candidate's tech stack: {tech_stack}, generate exactly 4 technical questions. 
        Format each question as a complete, standalone question.
        Make questions progressively more challenging, covering different aspects of their tech stack.
        Return exactly 4 questions, one per line."""
        
        response = self.get_llm_response(prompt)
        try:
            # Clean up and extract questions
            questions = [q.strip() for q in response.split('\n') if q.strip() and '?' in q]
            # Ensure we have exactly 4 questions
            if len(questions) > 4:
                questions = questions[:4]
            elif len(questions) < 4:
                questions.extend([
                    f"Could you explain your experience with {tech} in more detail?" 
                    for tech in tech_stack.split(',')[:4-len(questions)]
                ])
            return questions[:4]
        except:
            # Fallback questions
            return [
                f"Could you explain your experience with {tech_stack}?",
                f"What's the most challenging project you've worked on using {tech_stack}?",
                f"How do you stay updated with the latest developments in {tech_stack}?",
                f"Can you describe a technical problem you solved using {tech_stack}?"
            ]

    def generate_follow_up_questions(self) -> list:
        prompt = """Based on all previous responses, generate exactly 2 follow-up questions about:
        1. A challenging project experience
        2. Problem-solving approach in a team setting
        Make questions specific to the candidate's background."""
        
        response = self.get_llm_response(prompt)
        try:
            questions = [q.strip() for q in response.split('\n') if q.strip() and '?' in q]
            return questions[:2]  # Limit to 2 questions
        except:
            return ["Could you tell me about a challenging project you worked on?"]

    def chat(self, message: str) -> str:
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Track if interview is complete
        self.interview_complete = getattr(self, 'interview_complete', False)
        
        # If interview is already complete, only handle goodbye
        if self.interview_complete:
            return "The interview has already concluded. Have a great day!"
            
        # Skip getting next question if this is the first message since we already greeted
        if len(self.conversation_history) == 1 and hasattr(self, 'initial_greeting_sent'):
            self.candidate_info[self.current_question] = message
            self.update_current_question()
            response = self.get_next_question()
        else:
            # Handle the final phase first to prevent new questions
            if hasattr(self, 'waiting_for_final_response') and self.waiting_for_final_response:
                self.interview_complete = True
                if message.lower() in ['no', 'nope', 'none', 'not really', 'no questions']:
                    response = """Perfect! Thank you for your time today. We appreciate your participation in this interview process. 
                    Our team will review your responses and contact you soon regarding the next steps.
                    
                    Have a great day! Goodbye!"""
                else:
                    response = """Thank you for your questions. I've noted them down and our team will address them when they contact you.
                    
                    Thank you again for your time today. Have a great day! Goodbye!"""
                return response

            # Regular interview flow
            if not self.technical_phase and not self.follow_up_phase:
                self.candidate_info[self.current_question] = message
                self.update_current_question()
                
                if self.current_question == 'complete':
                    self.technical_questions = self.generate_technical_questions(self.candidate_info['tech_stack'])
                    self.technical_phase = True
                    response = "Thank you for providing your tech stack. Let's begin with some technical questions.\n\nFirst question:\n" + self.technical_questions[0]
                else:
                    response = self.get_next_question()
            
            elif self.technical_phase:
                self.current_tech_question += 1
                
                if self.current_tech_question < len(self.technical_questions):
                    question_number = self.current_tech_question + 1
                    response = f"Thank you. Question {question_number}:\n" + self.technical_questions[self.current_tech_question]
                else:
                    self.technical_phase = False
                    self.follow_up_phase = True
                    self.technical_questions = self.generate_follow_up_questions()
                    self.current_tech_question = 0
                    response = "Thank you for answering the technical questions. I have two follow-up questions about your experience.\n\nFirst follow-up question:\n" + self.technical_questions[0]
            
            elif self.follow_up_phase:
                self.current_tech_question += 1
                
                if self.current_tech_question < len(self.technical_questions):
                    response = "Final follow-up question:\n" + self.technical_questions[self.current_tech_question]
                else:
                    self.follow_up_phase = False
                    self.waiting_for_final_response = True  # Add this flag
                    response = """Thank you for completing the interview. I've gathered all the necessary information about your background, technical skills, and experience. 
                    Our team will review your responses and get back to you soon with the next steps. Do you have any questions for me?"""
        
        self.conversation_history.append({"role": "assistant", "content": response})
        return response

def create_streamlit_interface():
    st.set_page_config(page_title="Hiring Assistant", layout="wide")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = HiringAssistant()
        st.session_state.assistant.initial_greeting_sent = True  # Add this flag
    if 'messages' not in st.session_state:
        st.session_state.messages = []
        # Add initial greeting only once
        initial_greeting = st.session_state.assistant.get_next_question()
        st.session_state.messages.append({"role": "assistant", "content": initial_greeting})
    if 'show_summary' not in st.session_state:
        st.session_state.show_summary = False

    # Header
    st.title("AI Hiring Assistant")
    st.markdown("""
    Welcome to the initial screening interview. This AI assistant will ask you questions about:
    - Basic Information
    - Technical Skills
    - Work Experience
    """)

    # Chat interface
    chat_container = st.container()
    
    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Show summary if interview is complete
        if st.session_state.show_summary:
            with st.expander("Interview Summary", expanded=True):
                for key, value in st.session_state.assistant.candidate_info.items():
                    if value:
                        st.write(f"**{key.capitalize()}:** {value}")

    # Reset button
    if st.sidebar.button("Start New Interview"):
        st.session_state.assistant = HiringAssistant()
        st.session_state.messages = []
        st.session_state.show_summary = False
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Type your response here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Get assistant response
        response = st.session_state.assistant.chat(prompt)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.write(response)

        # Show summary if interview is complete
        if st.session_state.assistant.interview_complete:
            st.session_state.show_summary = True
            
        # Rerun to update the display
        st.rerun()

if __name__ == "__main__":
    create_streamlit_interface() 
