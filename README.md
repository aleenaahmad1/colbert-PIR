# 🧠 ColBERT-Based User Profiles for Personalized Information Retrieval

### By **Aleena Ahmad**, Gibson Nkhata, Abdul Rafay Bajwa, Hannah Marsico, Bryan Le, and Susan Gauch  
Affiliations: NUST, LUMS, University of Arkansas  
📄 [Read the Published Paper (PDF)](link-to-your-paper-or-arXiv)

---

## 🌐 Overview

This project implements a **Personalized Information Retrieval (PIR)** system using **ColBERT (Contextual Late Interaction over BERT)** embeddings to model user interests based on their **query and click history**.

Unlike prior approaches that select only a few representative terms for query expansion, this method **encodes entire user profiles** as contextual embeddings and **re-ranks BM25-retrieved documents** for better personalization.  

Additionally, a **frequency–recency weighting mechanism** is tested to adjust query influence based on how recent and frequent a user’s searches are.

---

## 🚀 Key Features

- 🔍 **Full User Profile Representation**  
  Represents complete user profiles (queries + clicked documents) as contextual embeddings.

- ⚖️ **Frequency–Recency Weighting**  
  Combines exponential decay (recency) and logarithmic scaling (frequency) to balance long-term vs. recent interests.

- ⚙️ **Dual-Stage Retrieval**  
  Uses BM25 for initial retrieval and ColBERT embeddings for reranking.

- 📊 **Cross-Dataset Evaluation**  
  Tested on two public datasets:
  - **AOL4PS** – Processed AOL query logs  
  - **PRRB** – Personalized Results Reranking Benchmark (multi-domain dataset)

---

## 🧩 System Architecture

            ┌──────────────────────┐
            │  User Search History  │
            └──────────┬───────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │  Profile Generation   │
             │ (Queries + Documents) │
             └──────────┬───────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │ ColBERT Embeddings   │
             └──────────┬───────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │ BM25 Candidate Docs  │
             └──────────┬───────────┘
                       │
                       ▼
             ┌──────────────────────┐
             │   Reranking via      │
             │  ColBERT Similarity  │
             └──────────────────────┘


---

## 📚 Datasets

The project uses two **public datasets**:

1. **AOL4PS:**  
   Derived from AOL query logs. Each record includes:
   - `AnonID`, `QueryTime`, `SessionNo`, `Candidate URLs`, `Clicked URL`.
   - Text content retrieved via web scraping (Wayback Machine used for unavailable pages).  

2. **PRRB:**  
   A multi-domain dataset (Computer Science, Physics, Psychology, Political Science).  
   - Each “user” represents an author, queries are paper titles, and relevant documents are cited papers.

> ⚠️ **Note:** Due to dataset size and licensing, these are **not included** in this repository.  
> You can obtain them from:
> - [AOL4PS Dataset (MIT Press)](https://direct.mit.edu/dint/article/3/4/548/1968580)
> - [PRRB Dataset (ACM CIKM 2022)](https://doi.org/10.1145/3511808.3557688)

If you use this work, please cite:
@article{ahmad2025colbertuserprofiles,
  title={ColBERT-Based User Profiles for Personalized Information Retrieval},
  author={Ahmad, Aleena and Nkhata, Gibson and Bajwa, Abdul Rafay and Marsico, Hannah and Le, Bryan and Gauch, Susan},
  year={2025},
  institution={University of Arkansas, LUMS, NUST}
}


