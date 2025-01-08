# AI Hiring Assistant Chatbot

Meet your friendly AI interviewer! This smart assistant helps streamline the initial screening process for candidates, making it more comfortable and efficient for everyone involved.

## What Can It Do?

Our AI assistant is like a professional recruiter who:
- Has a friendly chat with candidates through a clean, modern interface
- Guides them through a natural conversation about their background
- Asks thoughtful questions about their technical skills
- Adapts follow-up questions based on their responses

The assistant collects essential information like:
- Your name and contact details
- Professional experience
- Dream job position
- Current location
- Technical expertise

Then, it gets more interesting! Based on your tech skills, it will:
- Ask 4 relevant technical questions to understand your expertise
- Follow up with 2 questions about your real-world experience
- Wrap up with a nice summary of your conversation

## Getting Started

Never used this before? No worries! Here's how to set it up:

1. First, grab a copy of this project:
   ```bash
   git clone [repository-url]
   ```

2. Set up your workspace (it's like creating a special room for our assistant):
   ```bash
   python -m venv venv
   ```

3. Step into that room:
   - If you're using Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - If you're on Mac or Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install all the tools our assistant needs:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the conversation:
   ```bash
   streamlit run app.py
   ```

6. Open your web browser and head to http://localhost:8501 - that's where your interviewer is waiting!

## How Does It Work?

It's as simple as having a regular conversation:
1. The assistant starts by saying hello and asking for your name
2. Just answer naturally, like you would in a real interview
3. Share your technical background, and it'll ask relevant questions
4. Tell your stories about past projects and experiences
5. At the end, you'll get a nice summary of your chat
6. Want to start fresh? Just click "Start New Interview" in the sidebar

## Behind the Scenes

Our assistant is powered by some cool technology:
- A sleek interface built with Streamlit
- The powerful Mixtral-8x7b AI model via Groq
- A carefully designed conversation flow that feels natural
- Smart question generation based on your unique background

## Important Note

While our assistant is friendly, it takes privacy seriously! In a real-world setting, we ensure:
- Your information stays secure
- Data is handled with care
- Everything follows proper privacy rules
- The system is protected from unauthorized access

## What's in the Box?

- `app.py`: The brain of our assistant
- `requirements.txt`: The tools it needs
- `README.md`: This friendly guide
- `Roadmap.md`: Our plans for making it even better

Ready to have a chat with our AI interviewer? Let's get started! 🚀 