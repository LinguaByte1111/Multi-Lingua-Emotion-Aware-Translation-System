# Multi-Lingua Emotion Aware Translation System

**Status:** Done

The **Multi-Lingua Emotion Aware Translation System** is an intelligent translation platform supporting 30 languages — including the top 20 Indian and top 10 global languages.


## 🔍 Table of Contents

* [About the Project](#About-the-Project)
* [Project Architecture](#Project-Architecture)
* [Dataset and Preprocessing](#dataset-and-preprocessing)
* [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
* [Model Development](#model-development)

  * [Emotion Recognition Models](#emotion-recognition-models)
  * [Gesture Recognition Model](#gesture-recognition-model)
* [Performance](#performance)
* [Code Overview](#code-overview)
* [How to Run](#how-to-run)
* [Dependencies](#dependencies)
* [License](#license)
* [Contribution](#Contribution)

---

### 1️⃣ About the Project

The Multi-Lingua Emotion Aware Translation System is an intelligent multilingual translation platform that not only translates text across 30 languages (including the top 20 Indian and top 10 global languages) but also integrates emotion awareness for richer communication.

✨ Key Highlights:

🌐 Multilingual Translation: Seamless translation across 30 languages.

😃 Emotion Recognition: Detects emotions in text and speech for emotion-matched text-to-speech output.

🧐 Sarcasm Detection: A rule-based sarcasm detection system ensures contextually accurate translations.

This system bridges the gap between linguistic accuracy and emotional intelligence, making conversations more natural, expressive, and human-like.

---

### 2️⃣ Project Architecture

The system is designed as a modular pipeline with clearly defined components:

flowchart TD
    A[Input Text / Speech] --> B[Language Detection]
    B --> C[Translation Engine]
    C --> D[Emotion Recognition Module]
    D --> E[Sarcasm Detection Rules]
    E --> F[Emotion-Matched Text-to-Speech]
    F --> G[Output in Target Language]

🔧 Components

Language Detection: Identifies source language among 30 supported ones.

Translation Engine: Handles multilingual translation tasks.

Emotion Recognition: Detects emotions (happy, sad, angry, neutral, etc.) from text/speech.

Sarcasm Detection: Rule-based approach for refining contextual meaning.

Speech Synthesis: Produces emotion-aware speech output.
