# pip install tensorflow==2.15.0
# pip install torch==2.0.1
# pip install sentence_transformers==2.2.2
# pip install streamlit

# import libraries===================================
import streamlit as st
import torch
from sentence_transformers import util
import pickle
from tensorflow.keras.layers import TextVectorization
import numpy as np
from tensorflow import keras

# load save recommendation models===================================

embeddings = pickle.load(open('models/embeddings.pkl','rb'))
sentences = pickle.load(open('models/sentences.pkl','rb'))
rec_model = pickle.load(open('models/rec_model.pkl','rb'))



# Load the vocabulary
with open("models/vocab.pkl", "rb") as f:
    loaded_vocab = pickle.load(f)


# custom functions====================================
def recommendation(input_paper):
    # Calculate cosine similarity scores between the embeddings of input_paper and all papers in the dataset.
    cosine_scores = util.cos_sim(embeddings, rec_model.encode(input_paper))

    # Get the indices of the top-k most similar papers based on cosine similarity.
    top_similar_papers = torch.topk(cosine_scores, dim=0, k=5, sorted=True)

    # Retrieve the titles of the top similar papers.
    papers_list = []
    for i in top_similar_papers.indices:
        papers_list.append(sentences[i.item()])

    return papers_list




# create app=========================================
st.title('Research Papers Recommendation System')


input_paper = st.text_input("Enter Research Paper Title...")
new_abstract = st.text_area("Enter Research Paper Abstract...")
if st.button("Recommend"):
    # recommendation part
    recommend_papers = recommendation(input_paper)
    st.subheader("Recommended Papers...")
    st.write(recommend_papers)

