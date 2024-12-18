# 📰 NEWSimplify

**NEWSimplify** is a Python-based news assistant project that demonstrates the integration of custom tools and their invocation by the Llama 3.1-70B large language model. The assistant fetches and summarizes the latest news articles on any topic of interest using a chat-based interface.

## 🌟 Key Features
- **Custom Tools Integration**: Demonstrates custom functions for:
  - Fetching the top 3 relevant news articles using `search_web`.
  - Extracting and summarizing content from the selected article using `extract_article`.
- **AI-Powered Backend**: Powered by the **Llama 3.1-70B** model to generate responses and dynamically call tools when required.
- **Streamlit Web UI**: Simple and user-friendly chat interface for interacting with the assistant.
- **Real-Time News Fetching**: Utilizes `duckduckgo_search` to gather the latest articles.

## 🚀 How It Works
1. **User Query**: The user enters a topic of interest via the chat interface.
2. **Custom Tool Call (`search_web`)**:
   - The assistant fetches the top 3 relevant articles related to the topic.
3. **Article Selection**:
   - The user selects an article by providing its number or title.
4. **Custom Tool Call (`extract_article`)**:
   - The assistant extracts and summarizes the content of the selected article.
5. **Follow-Up Questions**:
   - Users can ask follow-up questions based on the content of the article.

## 🛠️ Installation

### Prerequisites
- **Python 3.12+**
- **Poetry** - Python dependency manager (`pip install poetry`)
- **Streamlit** - For the chat-based web UI.

### Steps to Install and Run
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Arnab1311/NewsSimplify.git
   cd NewsSimplify
   ```

2. **Install Dependencies Using Poetry**:
   ```bash
   poetry install
   ```

3. **Set Up Environment Variables**:
   - Create a `.env` file in the project directory and add your credentials:
     ```env
     GROQ_API_KEY=your_groq_api_key
     ```

4. **Run the Application**:
   Start the Streamlit interface:
   ```bash
   streamlit run newsimplify.py
   ```

5. **Interact with the Assistant**:
   Open [http://localhost:8501](http://localhost:8501) in your browser and start asking for news topics!

## 🧰 Dependencies
This project uses the following libraries:
- **streamlit**: To build the chat-based UI.
- **duckduckgo-search**: For fetching real-time news articles.
- **selenium**: For web scraping and article extraction.
- **python-dotenv**: To manage environment variables securely.
- **groq**: API library to interact with the Llama 3.1-70B model.

## 💡 Project Files Overview
- `newsimplify.py`: Main script handling the assistant logic and Streamlit UI.
- `websearch.py`: Custom tool for searching news articles.
- `article.py`: Custom tool for extracting and summarizing article content.
- `.gitignore`: Ignores unnecessary files like virtual environments and caches.
- `pyproject.toml`: Poetry configuration file for dependency management.

## 🧪 Example Usage


## 🎯 Objective
This project highlights tool-calling capabilities in LLMs where the assistant dynamically calls external functions based on user queries. It showcases practical applications of integrating large language models with real-world tools to automate tasks like:
- **Fetching Information**
- **Summarizing Content**
- **Providing Follow-Up Insights**

## 🤝 Contributing
Contributions are welcome! To get started:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add new feature"
   git push origin feature-name
   ```
4. Open a pull request.

## 📄 License
This project is licensed under the Apache-2.0 License. See `LICENSE` for details.

## 🧑‍💻 Author
- **Arnab Kumar Chand**
- **GitHub**: [Arnab1311](https://github.com/Arnab1311)

## 🚀 Future Enhancements
- Add advanced filtering options for news articles.
- Integrate more tools to fetch weather, sports stats, or stock data.
- Enhance the assistant’s ability to answer deeper analytical queries.


