# dc-know-it-all - College Website Expert System
The College Website Expert System is an application that uses a large language model to provide answers to user queries related to college websites. The system is based on the central concepts of website pages, the text on those pages, and the questions and answers generated from the text.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)]()

# Architecture
The system uses a large language model, specifically Databricks Dolly v2, with 3 billion parameters and BERT-based question similarity. The reasoning process works by retrieving the relevant webpage from the dataset based on the user's input question, then providing this webpage and the user input as context and input to the language model to generate a response. The system does not require a detailed conceptual model as it relies on the large language model to handle the complexity of the reasoning process.

# User Interface
Since the system uses a large language model, there are computational limitations for deployment. If funded, we aim to use a Flask application to render a front-end that creates a conversation with users.

# Implementation
We use Spacy's "en_core_web_md" model to encode every question in our dataset. We then use cosine similarity to match this question and retrieve the web page corresponding to it. We then input this webpage as "context" parameter to the "databricks/dolly-v2-3b" model imported through the Hugging Face API. The model reads the context and the appended user input (question) to give us results. The Langchain library is used to feed the model context and the question in conversational style.

In the future, we can improve performance by using strong question similarity matching, keyword match or a direct input to webpage match. This part of our system is a performance bottleneck but can be improved drastically through additional research.

# Deployment
This solution is deployed on Google Colab using Python input statement as the interface.

# Conclusion
The College Website Expert System is a promising application that can be used to provide quick and efficient answers to user queries related to college websites. With additional research and development, the system can be improved to handle more complex questions and provide even better results.