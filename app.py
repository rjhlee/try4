import streamlit as st
import json
import difflib

st.set_page_config(page_title="어휘 확장 네트워크 앱", page_icon="🌐")

st.title("🌐 어휘 확장 네트워크 앱")
st.write("단어를 입력하면 의미 + 카테고리 기반으로 어휘가 확장됩니다!")

# -------------------------------
# 데이터 불러오기
# -------------------------------
with open("vocab.json", "r", encoding="utf-8") as f:
    vocab = json.load(f)

with open("categories.json", "r", encoding="utf-8") as f:
    categories = json.load(f)

# -------------------------------
# 형태 변환
# -------------------------------
def normalize(word):
    if word.endswith("파"):
        return word.replace("파", "픔")
    if word.endswith("러"):
        return word + "움"
    if word.endswith("려"):
        return word.replace("려", "림")
    if word.endswith("해"):
        return word.replace("해", "함")
    return word

# -------------------------------
# 연쇄 확장
# -------------------------------
def expand_word(word, vocab):
    result = set()

    if word in vocab:
        first = vocab[word]["관련어"]
        result.update(first)

        for w in first:
            if w in vocab:
                result.update(vocab[w]["관련어"])

    return list(result)

# -------------------------------
# 유사 단어 추천
# -------------------------------
def suggest_words(word, vocab):
    return difflib.get_close_matches(word, vocab.keys(), n=5, cutoff=0.5)

# -------------------------------
# 입력
# -------------------------------
word_input = st.text_input("단어를 입력하세요")
word = normalize(word_input)

# -------------------------------
# 카테고리 찾기
# -------------------------------
found_category = None
for category, words in categories.items():
    if word in words:
        found_category = category
        break

# -------------------------------
# 출력
# -------------------------------
if word:

    # 1️⃣ vocab 기반 확장
    if word in vocab:
        st.subheader(f"📘 '{word}' 어휘 확장")

        st.write("👉 유의어:", ", ".join(vocab[word]["유의어"]))
        st.write("👉 반의어:", ", ".join(vocab[word]["반의어"]))
        st.write("👉 관련어:", ", ".join(vocab[word]["관련어"]))
        st.write("👉 예문:", vocab[word]["예문"])

        st.divider()

        expanded = expand_word(word, vocab)

        st.subheader("🌐 확장된 어휘 네트워크")
        if expanded:
            st.write(", ".join(expanded))
        else:
            st.write("확장된 어휘가 없습니다.")

    # 2️⃣ 없는 단어 처리 + 추천
    else:
        st.warning("사전에 없는 단어예요 😢")

        suggestions = suggest_words(word, vocab)

        if suggestions:
            st.write("👉 혹시 이런 단어인가요?")
            for s in suggestions:
                st.write("-", s)

            st.divider()

            st.subheader("🌐 추천 단어 기반 확장")

            for s in suggestions:
                if s in vocab:
                    st.write(f"'{s}' 관련어:")
                    st.write(", ".join(vocab[s]["관련어"]))
        else:
            st.write("👉 비슷한 단어를 찾지 못했어요.")

    # 3️⃣ ⭐ 카테고리 확장 (핵심 추가 기능)
    if found_category:
        st.divider()
        st.subheader(f"📦 '{word}'는 '{found_category}'에 속해요!")

        st.write("👉 같은 카테고리 단어:")
        st.write(", ".join(categories[found_category]))
