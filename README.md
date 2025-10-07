# 📰🔎 Summarization + Question Answering App

This project is a **Streamlit web application** that allows you to:

* Paste any article or long text.
* Generate a **summary** using a pretrained Hugging Face model.
* Ask **questions** about the article or the summary and get answers instantly.

---

## 🌐 Live Demo

Try it out here 👉 [Text Summarization App](https://summarization-question-answering-app.streamlit.app/)

---

## 🚀 Features

* Text summarization using **facebook/bart-large-cnn**.
* Question answering using **deepset/roberta-base-squad2**.
* Option to choose whether the question should be answered from the **full text** or the **generated summary**.
* Simple, clean Streamlit interface.

---

## 📂 Project Structure

```
project/
│
├── merged_streamlit_app.py   # Main Streamlit app
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## ⚙️ Installation

1. Clone this repository or download the files.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:

   ```bash
   streamlit run merged_streamlit_app.py
   ```

---

## 📦 Requirements

* Python 3.8+
* [Streamlit](https://streamlit.io/)
* [Transformers](https://huggingface.co/transformers/)
* [Torch](https://pytorch.org/)

Contents of **requirements.txt**:

```
streamlit
transformers
torch
```

---

## 🧠 Models Used

* **Summarization**: [`facebook/bart-large-cnn`](https://huggingface.co/facebook/bart-large-cnn)
* **Question Answering**: [`deepset/roberta-base-squad2`](https://huggingface.co/deepset/roberta-base-squad2)

> ⚠️ These models are large and may take time to download the first time.

---

## 💡 Future Improvements

* Add file upload support (PDF/TXT).
* Save Q&A history to CSV.
* Allow model selection from the UI.

---

## 👨‍💻 Author

**Muhammad Al-Aasar**  
🎓 B.Sc. in Computer Science, Tanta University  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/muhammad-al-aasar-455b78329)  
📞 +20 1015088811

