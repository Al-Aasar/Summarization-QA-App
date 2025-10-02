import streamlit as st
from transformers import pipeline
from docx import Document


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
st.markdown("Paste your article or upload a file (TXT/DOCX).")

# ----------------- Upload or paste -----------------
uploaded_file = st.file_uploader("Upload a TXT or DOCX file", type=["txt", "docx"])
context = ""

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        context = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        full_text = [para.text for para in doc.paragraphs]
        context = "\n".join(full_text)

st.subheader("Article (Context)")
text_area_content = st.text_area("Paste article here or use uploaded file...", value=context, height=350)

if text_area_content.strip() == "":
    st.info("Paste the article or upload a file to enable summarization and Q&A.")

st.subheader("Summarization Settings")
min_len, max_len = st.slider(
    "Select min and max length (approx. chars)",
    min_value=10,
    max_value=2000,
    value=(30, 130),
    step=10
)
do_sample = st.checkbox("Use sampling (do_sample)", value=False)

# ----------------- Summarization -----------------
if st.button("📝 Summarize"):
    if text_area_content.strip() == "":
        st.warning("Please provide article text first.")
    elif summarizer is None:
        st.error("Summarizer model not available.")
    else:
        with st.spinner("Summarizing... ⏳"):
            try:
                summary_output = summarizer(
                    text_area_content, max_length=int(max_len),
                    min_length=int(min_len), do_sample=do_sample
                )
                summary_text = summary_output[0]["summary_text"]
                st.session_state["last_summary"] = summary_text
            except Exception as e:
                st.error(f"Error during summarization: {e}")

# Always show summary if exists
if "last_summary" in st.session_state:
    st.subheader("📝 Summary")
    st.write(st.session_state["last_summary"])

# ----------------- Question Answering -----------------
st.markdown("---")
st.subheader("Ask a Question")
question = st.text_input("Type your question here...")
context_source = st.radio("Which text to use for answering?", ("Full text", "Summary"))

if st.button("❓ Get Answer"):
    if question.strip() == "" or text_area_content.strip() == "":
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
                    ctx = text_area_content

                result = qa_model(question=question, context=ctx)
                answer = result.get("answer", "")
                score = result.get("score", None)

                st.subheader("✅ Answer")
                st.write(answer)
                if score is not None:
                    st.caption(f"Confidence score: {round(score, 3)}")

            except Exception as e:
                st.error(f"Error during QA: {e}")


