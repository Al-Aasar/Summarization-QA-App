import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="Summarization & QA App", page_icon="🧠", layout="wide")

@st.cache_resource
def load_summarizer():
    try:
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        st.error(f"Error loading summarization model: {e}")
        return None

@st.cache_resource
def load_qa():
    try:
        return pipeline("question-answering", model="deepset/roberta-base-squad2")
    except Exception as e:
        st.error(f"Error loading QA model: {e}")
        return None

summarizer = load_summarizer()
qa_model = load_qa()

st.title("📰🔎 Summarization + Question Answering")
st.markdown("Paste your article below. You can summarize it and then ask questions either on the original text or the summary.")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Article (Context)")
    context = st.text_area("Paste article here...", height=350)

    if context.strip() == "":
        st.info("Paste the article text above to enable summarization and Q&A.")

with col2:
    st.subheader("Summarization Settings")
    min_len = st.number_input("Min length (approx. chars)", min_value=10, max_value=1000, value=30, step=10)
    max_len = st.number_input("Max length (approx. chars)", min_value=20, max_value=2000, value=130, step=10)
    do_sample = st.checkbox("Use sampling (do_sample)", value=False)
    st.markdown("---")
    st.subheader("Ask a Question")
    question = st.text_input("Type your question here...")
    context_source = st.radio("Which text to use for answering?", ("Full text", "Summary"))

col_run1, col_run2 = st.columns(2)
with col_run1:
    if st.button("📝 Summarize"):
        if context.strip() == "":
            st.warning("Please paste the article text first.")
        elif summarizer is None:
            st.error("Summarizer model not available.")
        else:
            with st.spinner("Summarizing... ⏳"):
                try:
                    input_text = context
                    summary_output = summarizer(input_text, max_length=int(max_len), min_length=int(min_len), do_sample=do_sample)
                    summary_text = summary_output[0]["summary_text"]
                    st.subheader("📝 Summary")
                    st.write(summary_text)
                    st.session_state["last_summary"] = summary_text
                except Exception as e:
                    st.error(f"Error during summarization: {e}")

with col_run2:
    if st.button("❓ Get Answer"):
        if question.strip() == "" or context.strip() == "":
            st.warning("Please provide both the text and a question.")
        elif qa_model is None:
            st.error("QA model not available.")
        else:
            with st.spinner("Processing... ⏳"):
                try:
                    if context_source == "Summary":
                        ctx = st.session_state.get("last_summary", "")
                        if ctx == "":
                            st.warning("No summary generated yet. Please summarize first or select 'Full text'.")
                            st.stop()
                    else:
                        ctx = context

                    result = qa_model(question=question, context=ctx)
                    answer = result.get("answer", "")
                    score = result.get("score", None)

                    st.subheader("✅ Answer")
                    st.write(answer)
                    if score is not None:
                        st.caption(f"Confidence score: {round(score, 3)}")

                except Exception as e:
                    st.error(f"Error during QA: {e}")

st.markdown("---")
with st.expander("How to run locally"):
    st.markdown(
        "1. Install requirements: `pip install streamlit transformers torch`\n"
        "2. Save this file as `merged_streamlit_app.py`.\n"
        "3. Run: `streamlit run merged_streamlit_app.py`.\n"
        "4. Note: Hugging Face models are large, downloading them will take time and disk space."
    )

# ----------------- Footer -----------------
st.markdown("---")
st.caption("App combines text summarization and question answering in one interface.")
