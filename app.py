import streamlit as st
import random
import json

# Page config
st.set_page_config(
    page_title="AI-Powered Data Engineer Flashcards",
    page_icon="🧠",
    layout="centered"
)

# Custom CSS
st.markdown("""
    <style>
    .main-card {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .question-text {
        font-size: 1.3rem;
        font-weight: 500;
        color: #1f2937;
        margin: 1rem 0;
    }
    .answer-text {
        font-size: 1.1rem;
        color: #374151;
        line-height: 1.6;
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .ai-feedback {
        background-color: #f3e8ff;
        border-left: 4px solid #9333ea;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .hint-box {
        background-color: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
    .category-badge {
        background-color: #3b82f6;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        display: inline-block;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        font-weight: 500;
    }
    </style>
""", unsafe_allow_html=True)

# Flashcards data
flashcards = [
    {"category": "Fundamentals", "question": "What is the difference between OLTP and OLAP?", 
     "answer": "OLTP systems handle day-to-day transactions and are optimized for many small inserts and updates, like banking or e-commerce systems. OLAP systems are designed for analytics, with fewer writes but heavy read queries over large datasets, such as aggregations and reporting."},
    {"category": "Fundamentals", "question": "What is batch processing vs stream processing?", 
     "answer": "Batch processing handles data in chunks at scheduled times, for example daily CSV imports. Stream processing handles data in real time or near real time, such as click events or sensor data."},
    {"category": "Data Modeling", "question": "How would you model the Country table in a data warehouse?", 
     "answer": "I would create a Country dimension table with attributes like country name, code, and continent. Population could either remain in the dimension if it's static or move to a fact table if it changes over time."},
    {"category": "Data Modeling", "question": "What is a star schema?", 
     "answer": "A star schema consists of a central fact table connected to dimension tables. It simplifies queries and improves performance for analytics."},
    {"category": "ETL", "question": "Explain ETL vs ELT.", 
     "answer": "ETL means transforming data before loading it into the warehouse, often used in traditional systems. ELT loads raw data first and transforms it inside the warehouse, which is common in cloud data platforms."},
    {"category": "ETL", "question": "How would you load this CSV daily without duplicates?", 
     "answer": "I would use a staging table, load the CSV into it, then insert only new records into the final table using a unique key or a timestamp to avoid duplicates."},
    {"category": "Data Quality", "question": "How do you ensure data quality?", 
     "answer": "I check for null values, validate data ranges, enforce uniqueness, and monitor row counts and freshness after each load."},
    {"category": "Data Quality", "question": "What would you do if population values were negative?", 
     "answer": "I would block the data from loading, log the issue, and notify stakeholders, because negative population values indicate invalid data."},
    {"category": "Performance", "question": "When should you create an index?", 
     "answer": "Indexes should be created on columns frequently used in filters, joins, or sorting, but avoided on columns with frequent updates."},
    {"category": "Performance", "question": "What is partitioning?", 
     "answer": "Partitioning splits data into logical segments, such as by date or continent, which improves query performance and manageability."},
    {"category": "Python", "question": "How would you read this CSV in Python?", 
     "answer": "I would use pandas with `read_csv`, inspect the data, handle missing values, and validate schema before loading."},
    {"category": "Python", "question": "Why use virtual environments?", 
     "answer": "Virtual environments isolate dependencies so different projects don't conflict with each other."},
    {"category": "Tools", "question": "What is Airflow?", 
     "answer": "Airflow is a workflow orchestration tool used to schedule, monitor, and manage data pipelines using directed acyclic graphs."},
    {"category": "Tools", "question": "How do you schedule pipelines?", 
     "answer": "Pipelines can be scheduled using cron jobs or orchestration tools like Airflow."},
    {"category": "Behavioral", "question": "What do you do if data is late?", 
     "answer": "I first verify the source, communicate the delay, and ensure downstream systems are informed. Then I investigate and fix the root cause."},
    {"category": "Behavioral", "question": "How do you explain data issues to non-technical people?", 
     "answer": "I explain the impact in business terms, such as missing reports or delayed decisions, without technical jargon."},
    {"category": "Behavioral", "question": "Do you have any questions for us?", 
     "answer": "Yes. How do you monitor data quality in production, and what tools does the team use for pipeline reliability?"}
]

# Initialize session state
if "card_index" not in st.session_state:
    st.session_state.card_index = 0
    st.session_state.show_answer = False
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.current_category = "All"
    st.session_state.user_answer = ""
    st.session_state.ai_feedback = ""
    st.session_state.hint = ""
    st.session_state.custom_cards = []

# AI Helper Functions
async def get_ai_feedback(question, correct_answer, user_answer):
    """Get AI feedback on user's answer"""
    try:
        response = await fetch("https://api.anthropic.com/v1/messages", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": f"""You are a helpful data engineering mentor. A student answered an interview question.

Question: {question}

Correct Answer: {correct_answer}

Student's Answer: {user_answer}

Please provide:
1. Whether their answer is correct/partially correct/incorrect
2. What they got right
3. What they missed or got wrong
4. A tip to improve their answer

Keep it concise and encouraging."""
                }]
            })
        })
        data = await response.json()
        return data["content"][0]["text"]
    except Exception as e:
        return f"Unable to get AI feedback at this time."

async def get_hint(question, answer):
    """Get a hint for the current question"""
    try:
        response = await fetch("https://api.anthropic.com/v1/messages", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": f"""Provide a helpful hint for this data engineering interview question without giving away the full answer.

Question: {question}

Full Answer (for context): {answer}

Give a hint that points the student in the right direction. Keep it brief (2-3 sentences)."""
                }]
            })
        })
        data = await response.json()
        return data["content"][0]["text"]
    except Exception as e:
        return "Unable to generate hint at this time."

async def generate_custom_card(topic, difficulty):
    """Generate a custom flashcard on a specific topic"""
    try:
        response = await fetch("https://api.anthropic.com/v1/messages", {
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{
                    "role": "user",
                    "content": f"""Generate a {difficulty} level data engineering interview question about: {topic}

Respond ONLY with valid JSON in this exact format (no markdown, no backticks):
{{"category": "Custom", "question": "your question here", "answer": "detailed answer here"}}"""
                }]
            })
        })
        data = await response.json()
        text = data["content"][0]["text"].strip()
        # Remove any markdown code block markers
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception as e:
        st.error(f"Unable to generate custom card: {e}")
        return None

# Sidebar
st.sidebar.title("📚 Flashcard Settings")

# AI Features Toggle
st.sidebar.markdown("### 🤖 AI Features")
ai_enabled = st.sidebar.checkbox("Enable AI Features", value=True)

# Category selection
categories = ["All"] + sorted(list(set([card["category"] for card in flashcards + st.session_state.custom_cards])))
selected_category = st.sidebar.selectbox("Choose category:", categories, key="category_select")

# Update current category if changed
if selected_category != st.session_state.current_category:
    st.session_state.current_category = selected_category
    st.session_state.card_index = 0
    st.session_state.show_answer = False
    st.session_state.ai_feedback = ""
    st.session_state.hint = ""

# Filter cards by category
all_cards = flashcards + st.session_state.custom_cards
filtered_cards = all_cards if selected_category == "All" else [c for c in all_cards if c["category"] == selected_category]

# Stats
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Your Progress")
if st.session_state.total > 0:
    accuracy = (st.session_state.score / st.session_state.total) * 100
    st.sidebar.metric("Accuracy", f"{accuracy:.1f}%")
st.sidebar.metric("Correct", st.session_state.score)
st.sidebar.metric("Total Answered", st.session_state.total)
st.sidebar.metric("Cards in Category", len(filtered_cards))

# Reset button
if st.sidebar.button("🔄 Reset Progress"):
    st.session_state.score = 0
    st.session_state.total = 0
    st.rerun()

# Custom card generator
if ai_enabled:
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ✨ Generate Custom Card")
    with st.sidebar.form("custom_card_form"):
        topic = st.text_input("Topic", placeholder="e.g., Data Lakes")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        if st.form_submit_button("Generate"):
            with st.spinner("Generating custom flashcard..."):
                import asyncio
                card = asyncio.run(generate_custom_card(topic, difficulty))
                if card:
                    st.session_state.custom_cards.append(card)
                    st.success(f"Created custom card about {topic}!")
                    st.rerun()

# Helper functions
def next_card():
    st.session_state.card_index = random.randint(0, len(filtered_cards) - 1)
    st.session_state.show_answer = False
    st.session_state.user_answer = ""
    st.session_state.ai_feedback = ""
    st.session_state.hint = ""

def mark_correct():
    st.session_state.score += 1
    st.session_state.total += 1
    next_card()

def mark_incorrect():
    st.session_state.total += 1
    next_card()

# Main content
st.title("🧠 AI-Powered Data Engineer Flashcards")
st.markdown("Practice with intelligent feedback and personalized hints!")

# Display current card
if len(filtered_cards) > 0:
    card = filtered_cards[st.session_state.card_index]
    
    # Category badge
    st.markdown(f'<span class="category-badge">{card["category"]}</span>', unsafe_allow_html=True)
    
    # Question card
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">❓ {card["question"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI-powered practice mode
    if ai_enabled:
        st.markdown("#### 💭 Try answering first:")
        user_answer = st.text_area(
            "Your answer:",
            value=st.session_state.user_answer,
            height=100,
            placeholder="Type your answer here...",
            key=f"answer_input_{st.session_state.card_index}"
        )
        st.session_state.user_answer = user_answer
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💡 Get Hint", use_container_width=True):
                with st.spinner("Generating hint..."):
                    import asyncio
                    hint = asyncio.run(get_hint(card["question"], card["answer"]))
                    st.session_state.hint = hint
                    st.rerun()
        
        with col2:
            if st.button("🤖 Get AI Feedback", use_container_width=True, disabled=not user_answer):
                with st.spinner("Analyzing your answer..."):
                    import asyncio
                    feedback = asyncio.run(get_ai_feedback(card["question"], card["answer"], user_answer))
                    st.session_state.ai_feedback = feedback
                    st.rerun()
        
        # Display hint if requested
        if st.session_state.hint:
            st.markdown(f'<div class="hint-box">💡 <strong>Hint:</strong> {st.session_state.hint}</div>', unsafe_allow_html=True)
        
        # Display AI feedback if available
        if st.session_state.ai_feedback:
            st.markdown(f'<div class="ai-feedback">🤖 <strong>AI Feedback:</strong><br>{st.session_state.ai_feedback}</div>', unsafe_allow_html=True)
    
    # Show answer button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("👁️ Show Answer", use_container_width=True):
            st.session_state.show_answer = True
            st.rerun()
    
    # Display answer if shown
    if st.session_state.show_answer:
        st.markdown(f'<div class="answer-text">✅ <strong>Answer:</strong><br>{card["answer"]}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("#### Did you get it right?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ I got it right", type="primary", use_container_width=True):
                mark_correct()
                st.rerun()
        with col2:
            if st.button("❌ I got it wrong", use_container_width=True):
                mark_incorrect()
                st.rerun()
    
    # Next card button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("⏭️ Skip to Next Card", use_container_width=True):
            next_card()
            st.rerun()

else:
    st.warning("No flashcards available in this category.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #6b7280; font-size: 0.9rem;'>"
    "🤖 Powered by Claude AI • 💡 Get personalized feedback and hints!"
    "</div>",
    unsafe_allow_html=True
)
