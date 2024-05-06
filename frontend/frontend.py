import streamlit as st
import requests
import json

# set the url of API
API_URL = "http://localhost:5000/analyze"

# set the page config
st.set_page_config(page_title="MedAssist", layout="wide")

# set title of the page
st.title("MedAssist")

# set the introductory of the app/project
st.write("""
Welcome to MedAssist! Please describe your symptoms in the text box below and click 'Analyze' to get insights. 
Remember, this tool does not provide medical advice and is not a substitute for professional diagnosis. 
If you're feeling unwell, please consult a healthcare provider.
""")

# the text input for the user symptoms:
query = st.text_area("Enter your symptoms:", height=150)

# button to send the query to the API
if st.button('Analyze'):
	# check if input empty
	if query:
		try:
			# send POST requests to API
			response = requests.post(API_URL, json={"query": query})
			# raise error for bad response
			response.raise_for_status()
			# get the results from response
			result = response.json()['result']
			# displaying the result
			st.success("Analysis Result:")
			st.write(result)
		except requests.exceptions.RequestException as e:
			st.error(f"An error occurred: {e}")
	else:
		st.error("Please enter your symptoms before clicking 'Analyze'.")

# give some disclaimer
st.markdown("""
**Disclaimer:** MedAssist is not certified to provide medical advice. Always consult a healthcare professional for medical issues.
""")