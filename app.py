
import streamlit as st
import pandas as pd
from openai import OpenAI
import os

st.title("Shopify CSV Generator with GPT")

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    output = []

    for _, row in df.iterrows():
        prompt = f"Сделай краткое описание товара: {row['Name']}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        description = response.choices[0].message.content
        output.append({
            "Handle": row['Name'].lower().replace(" ", "-"),
            "Title": row['Name'],
            "Body (HTML)": description,
            "Vendor": row['Brand'],
            "Variant SKU": row['EAN'],
            "Variant Price": row['Price'],
        })

    result_df = pd.DataFrame(output)
    st.download_button("Download Shopify CSV", result_df.to_csv(index=False), file_name="shopify.csv")
