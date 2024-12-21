import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time

# Load environment variables
if "GOOGLE_API_KEY" in os.environ:
    load_dotenv()
    api_key = os.environ.get("GOOGLE_API_KEY")
else:
    api_key = st.secrets["GOOGLE_API_KEY"]

# Configure the Generative AI model
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
temperature = 0.2
generation_config = genai.GenerationConfig(temperature=temperature)

# Streamlit app title and description
st.set_page_config(page_title="Not Rock Paper Scissors", layout="centered")
st.markdown(
    """
    <h1 style="text-align: center; color: #FF5733;">Welcome to Not Rock Paper Scissors!</h1>
    <p style="text-align: center; font-size: 18px; color: #777777;">
    Prepare to witness the ultimate clash of imagination, where any concept can become a combatant. Let the battle of wits and creativity begin!
    </p>
    """,
    unsafe_allow_html=True,
)

# Input section
col1, col2 = st.columns(2)

with col1:
    st.markdown("<h3 style='color: #4CAF50;'>Player 1, unleash your wildest creation!</h3>", unsafe_allow_html=True)
    player1_input = st.text_area("", placeholder="Enter Player 1's creation", height=100)

with col2:
    st.markdown("<h3 style='color: #FF5733;'>Player 2, counter with your ultimate creation!</h3>", unsafe_allow_html=True)
    player2_input = st.text_area("", placeholder="Enter Player 2's creation", height=100)


# Battle button
if st.button("BATTLE"):
    if not player1_input or not player2_input:
        st.warning("Both players must enter their creations before battling!")
    else:
        st.markdown("<h3 style='text-align: center;'>Let the battle commence!</h3>", unsafe_allow_html=True)

        progress_text = st.empty()
        progress_bar = st.progress(0)

        prompt = f'''
        you are a judge of an intense game of battle between two imaginary objects. the game will be like rock, paper and scissors but with infinite creativity and endless possibilities. If the winner is obvious, then it should win (for example if it is rock vs scissor - rock wins, if there is elephant vs cat, logically elephant should win, etc). If there is no logical winner, you have to be very creative and wild in your decision and you have full creative liberty to let anyone win but it should have a justifiable answer. You have to provide your output as:
        player ___ wins with its ____(item name)
        --next line--
        reason in maximum 2 lines with proper entertaining narration of the scene.

        player one's choice for battle is {player1_input}
        player two's choice for battle is {player2_input}
        '''
        progress_bar.progress(15, text="Player 1 is gearing up...")
        time.sleep(0.75)
        progress_bar.progress(30, text="Player 2 is getting oiled up...")
        
        try:
            response = model.generate_content(prompt)
            progress_bar.progress(45, text="The battle is heating up...")
            response.resolve()
            progress_bar.progress(70, text="The battle is heating up...")
            progress_bar.progress(85, text="Victory is near...")
            time.sleep(1)
            result = response.candidates[0].content.parts[0].text
            progress_bar.progress(100, text="The judge is making the final call...")

            st.markdown("<h2 style='text-align: center; color: #4CAF50;'>Battle Results</h2>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 18px;'>{result}</p>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"An error occurred while processing the battle: {e}")
