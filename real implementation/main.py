import openai
import pandas as pd
import streamlit as st

# Set up your OpenAI API key
openai.api_key = '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'

# Function to generate AI persona for a given text
def generate_persona(text):
    response = openai.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "system", "content": text}],
      max_tokens=150
    )

    persona = response.choices[0].message.content.strip()
    return persona

# Function to load profiles from CSV
def load_profiles(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Function to get profile info
def get_profile_info(df, role, name):
    profile = df[(df['role'] == role) & (df['name'] == name)].iloc[0]
    profile_info = f"""
    - Person: {profile['name']}, {profile['title']} at {profile['company']}
    - Company: {profile['company']}, {profile['description']}
    """
    return profile_info, profile['company'], profile['name']

# Load profiles from CSV
csv_file = 'profile.csv'
profiles_df = load_profiles(csv_file)

# Standard questions templates
user_questions = [
    "What is your role in the company?",
    "What are your main responsibilities?",
    "What skills do you bring to your role?",
    "What are your short-term goals?",
    "What are your long-term goals?",
    "What challenges do you face in your role?",
    "How do you handle those challenges?",
    "What do you enjoy most about your work?",
    "What improvements would you like to see in your role?"
]

company_questions = [
    "What is the company's mission and vision?",
    "What are the company's main products or services?",
    "What are the company's core values?",
    "What are the company's short-term goals?",
    "What are the company's long-term goals?",
    "What challenges does the company face?",
    "How does the company address those challenges?",
    "What sets the company apart from its competitors?",
    "What improvements would the company like to make?"
]

# Streamlit UI to input text and generate AI personas
st.title("User and Company AI Persona Generator")

role = st.selectbox("Select Role", options=['seller', 'buyer'])

if role:
    names_for_role = profiles_df[profiles_df['role'] == role]['name'].tolist()
    name = st.selectbox("Select Name", options=names_for_role)

    if st.button("Generate AI Personas") and name:
        user_profile_info, company_name, user_name = get_profile_info(profiles_df, role, name)
        
        st.header(f"{user_name} Persona")
        user_persona = generate_persona('\n'.join(user_questions))
        st.write(user_persona)
        
        st.header(f"{company_name} Company Persona")
        company_persona = generate_persona('\n'.join(company_questions))
        st.write(company_persona)
