# PersonaAI 🤖✨

## Problem Statement
Current AI assistants follow a rigid “one-size-fits-all” approach, where users must repeatedly provide detailed prompts to establish context, role, and intent. This creates friction and leads to generic, non-personalized responses.

In reality, users are multi-dimensional—simultaneously acting as students, professionals, entrepreneurs, and fitness enthusiasts. Existing systems fail to manage these overlapping identities effectively, resulting in context confusion, lack of personalization, and inefficient user experiences.

---

## Project Description
PersonaAI is a **context-aware, multi-persona intelligent assistant ecosystem** that adapts dynamically to the user instead of forcing the user to adapt to the system.

The core idea is to transform a traditional chatbot into a **persona-driven AI companion** that changes its behavior, reasoning style, and UI based on the user’s active role and emotional context.

Key features include:

- **Gamified Onboarding System**: A fast, swipe-based (Tinder-style) onboarding flow that captures user intent, goals, and communication preferences without long forms.
- **Progressive UI Adaptation**: The interface dynamically transforms based on persona:
  - 🎓 Student → interactive, gamified learning interface  
  - 💼 Business → structured, analytical dashboard  
  - 🏋️ Fitness → goal-oriented tracking and motivation UI  
- **Role-Based Memory System**: User data is segmented into isolated persona-specific memory silos to ensure context accuracy and prevent cross-domain confusion.
- **Voice-First Multilingual Support**: Enables natural interaction using speech input/output, with native support for Malayalam and English for accessibility and regional inclusion.
- **Adaptive Intelligence Engine**: The AI modifies tone, depth, and reasoning style based on user role, emotional state, and intent.

This results in a deeply personalized experience where PersonaAI behaves like multiple specialized assistants inside a single unified system.

---

## Google AI Usage

### Tools / Models Used
- Google Gemini 1.5 Flash API (@google/generative-ai SDK)
- Google AI Studio (for prompt design and system instruction testing)
- Gemini contextual reasoning (long-context input handling)

---

### How Google AI Was Used

PersonaAI is built using a **Dynamic Prompt Orchestration architecture powered by Google Gemini models**.

- **Dynamic Cognitive Routing**: The backend dynamically modifies system instructions sent to Gemini based on the active persona (e.g., Student, Business, Fitness). This allows the same model to behave as different expert systems depending on context.

- **Simulated RAG (Context Injection)**: Before each Gemini API call, the backend retrieves relevant user memory from a structured storage system. This persona-specific context (e.g., academic level, goals, preferences) is injected into the prompt, enabling highly personalized and grounded responses.

- **Role-Based Behavioral Switching**: Gemini is instructed at runtime to adopt specific cognitive styles:
  - 🎓 Student mode → Socratic tutor, explanatory and educational  
  - 💼 Business mode → analytical, ROI-focused strategist  
  - 🏋️ Fitness mode → motivational and action-driven coach  

- **Multilingual Intelligence (Malayalam + English)**: Instead of external translation services, Gemini’s native multilingual capabilities are used directly. The system enforces language constraints within prompts to ensure culturally and linguistically accurate responses.

- **Google AI Studio for System Design**: AI Studio was used extensively for rapid prototyping of system instructions, persona tuning, and behavior testing before backend integration.

Overall, Google Gemini acts as the **core reasoning engine**, while the backend orchestrates context, memory, and persona switching to create a truly adaptive AI system.
---

## Proof of Google AI Usage

<img width="1399" height="730" alt="Screenshot 2026-03-31 at 2 43 12 PM" src="https://github.com/user-attachments/assets/ce6c2cba-67e9-4606-b860-358905cb969b" />

<img width="1399" height="730" alt="Screenshot 2026-03-31 at 2 43 24 PM" src="https://github.com/user-attachments/assets/6bec7e15-0b38-467d-9179-b2cf5bd1cf61" />

<img width="1470" height="730" alt="Screenshot 2026-03-31 at 2 46 41 PM" src="https://github.com/user-attachments/assets/0728684c-105d-46c8-a900-5557b9717ca5" />

---

## Screenshots 
Add project screenshots:

![WhatsApp Image 2026-03-31 at 2 40 34 PM](https://github.com/user-attachments/assets/c051fec5-60d5-43ef-897c-16ebfc31b686)
![ss](https://github.com/user-attachments/assets/2d1c3bba-a2a3-410e-b1fa-ccf01c416569)
![ssss](https://github.com/user-attachments/assets/c9aa71df-e06f-40f7-8e0c-84327c3d3b89)


---

## Demo Video
[Upload your demo video to Google Drive and paste the shareable link here(max 3 minutes).
[Watch Demo](#)](https://drive.google.com/drive/folders/12thXnEOF7owZ_J0Hb28MEA9xwpbbMEfz?usp=sharing)

---

## Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/itsananyaaa/build-with-ai.git

# 2. Go into the project folder
cd build-with-ai

# 3. Set up the backend
## 3a. Navigate to backend directory
cd backend

## 3b. Create a virtual environment
python3 -m venv venv

## 3c. Activate the virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

## 3d. Install backend dependencies
pip install -r requirements.txt

# 4. Set up the frontend
## 4a. Navigate to frontend directory from root
cd ../frontend

# 5. Start the backend server (from backend directory)
# Terminal 1 - Run from backend directory with venv activated
python main.py
# The backend will run on http://localhost:8000

# 6. Start the frontend server (from frontend directory)
# Terminal 2 - Run from frontend directory
python -m http.server 3000
# The frontend will run on http://localhost:3000

# 7. Access the application
# Open your browser and navigate to:
http://localhost:3000

# 8. Login credentials
# Username: testuser
# Password: password123
