import os
import streamlit as st
from openai import OpenAI
from PIL import Image
from io import BytesIO
import base64

# Streamlit app layout
st.title("Whiteboard Summary App")
st.write("Upload an image of a whiteboard and get a summary of its content.")

# Input for API key
api_key = st.text_input("Enter your OpenAI API key:", type="password")

if api_key:
    # Set the API key for the session
    os.environ["OPENAI_API_KEY"] = api_key
    client = OpenAI()

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Whiteboard.', use_column_width=True)

        # Prepare the image for sending to OpenAI API
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        # Convert image data to a data URI
        img_data_uri = "data:image/jpeg;base64," + img_str

        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Write a summary of what is written on this whiteboard"},
                        {
                            "type": "image_url",
                            "image_url": img_data_uri,  # Sending the base64 encoded image
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

        # Display the summary
        summary = response.choices[0].message.content
        st.write("Summary of the Whiteboard:")
        st.write(summary)

        # Export as .txt
        txt_file = BytesIO()
        txt_file.write(summary.encode())
        txt_file.seek(0)
        st.download_button(
            label="Download Summary as TXT",
            data=txt_file,
            file_name="whiteboard_summary.txt",
            mime="text/plain"
        )

else:
    st.warning("Please enter your OpenAI API key to proceed.")
