import streamlit as st
import requests

st.title("AI Customer Review Agent")

review = st.text_area("Enter customer review")
email = st.text_input("Customer email")
name = st.text_input("Customer name")

if st.button("Submit Review"):
    with st.spinner("Analyzing your feedback... (Please wait)"):
        try:
            # No timeout specified - will wait indefinitely
            response = requests.post(
                "http://127.0.0.1:8000/review",
                json={
                    "review": review,
                    "email": email,
                    "name": name
                }
                # timeout removed - will wait forever
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result["sentiment"] == "negative":
                    st.success("Your complaint has been received")
                    if "ticket_id" in result:
                        st.write("Ticket ID:", result["ticket_id"])
                else:
                    st.success("Thank you for your feedback!")
                
                st.write(result["response"])
            else:
                st.error(f"Something went wrong. Status code: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API. Make sure FastAPI server is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")