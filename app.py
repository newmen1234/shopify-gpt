
import streamlit as st
import pandas as pd
from openai import OpenAI

st.set_page_config(page_title="Shopify GPT (ENV mode)", layout="centered")
st.title("📦 Shopify CSV GPT (via Environment Variables)")

client = OpenAI()  # SDK берёт ключ и project из переменных окружения

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if not {"Name", "EAN", "Brand", "Price"}.issubset(df.columns):
        st.error("❌ CSV must include columns: Name, EAN, Brand, Price")
    else:
        output = []
        with st.spinner("Generating product descriptions..."):
            for _, row in df.iterrows():
                prompt = f"Сделай краткое описание товара: {row['Name']}"
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": prompt}]
                )
                description = response.choices[0].message.content.strip()
                output.append({
                    "Handle": row['Name'].lower().replace(" ", "-"),
                    "Title": row['Name'],
                    "Body (HTML)": description,
                    "Vendor": row['Brand'],
                    "Variant SKU": row['EAN'],
                    "Variant Price": row['Price'],
                })

        result_df = pd.DataFrame(output)
        st.success("✅ Done! Download your Shopify CSV below.")
        st.download_button("⬇️ Download CSV", result_df.to_csv(index=False), file_name="shopify_ready.csv")
