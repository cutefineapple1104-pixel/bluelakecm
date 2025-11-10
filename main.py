import streamlit as st
import os
import json
from datetime import datetime
from PIL import Image

UPLOAD_DIR = "uploads"
DB_FILE = "data.json"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def delete_entry(target):
    data = load_data()
    new_data = [d for d in data if d["path"] != target["path"]]
    save_data(new_data)
    if os.path.exists(target["path"]):
        os.remove(target["path"])
    st.success("🗑️ 삭제 완료!")
    if "selected" in st.session_state:
        del st.session_state["selected"]
    st.rerun()

def rename_entry(target, new_name):
    ext = os.path.splitext(target["path"])[1]
    new_filename = f"{new_name}{ext}"
    new_path = os.path.join(UPLOAD_DIR, new_filename)
    os.rename(target["path"], new_path)

    data = load_data()
    for d in data:
        if d["path"] == target["path"]:
            d["filename"] = new_filename
            d["path"] = new_path
            break
    save_data(data)
    st.success("✏️ 이름 변경 완료!")
    if "selected" in st.session_state:
        del st.session_state["selected"]
    st.rerun()

st.set_page_config(page_title="사진 갤러리", layout="wide")

data = load_data()
st.title("📸 사진 갤러리")

tabs = st.tabs(["📂 갤러리 보기", "🖼 새 사진 올리기"])

# -------------------------------------
# 📂 갤러리 보기
# -------------------------------------
with tabs[0]:
    if not data:
        st.info("아직 업로드된 사진이 없습니다.")
    else:
        cols = st.columns(4)
        for idx, item in enumerate(reversed(data)):
            col = cols[idx % 4]
            with col:
                img = Image.open(item["path"])
                if st.button(f"🖼 {item['filename']}", key=f"btn_{idx}"):
                    st.session_state["selected"] = item
                st.image(img, use_column_width=True)

        # 선택 항목 확인
        if "selected" in st.session_state:
            sel = st.session_state["selected"]

            # 안전검사: 실제 파일이 존재하지 않거나 데이터가 사라진 경우
            if not sel or not os.path.exists(sel["path"]):
                st.warning("⚠️ 선택한 파일이 더 이상 존재하지 않습니다.")
                del st.session_state["selected"]
                st.rerun()
            else:
                st.markdown("---")
                st.subheader(sel["filename"])
                st.image(sel["path"], use_column_width=True)
                st.write(f"🕓 업로드 시각: {sel['timestamp']}")
                st.markdown(f"{sel['text']}")

                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("🔙 닫기"):
                        del st.session_state["selected"]
                        st.rerun()
                with col2:
                    if st.button("🗑️ 삭제하기"):
                        delete_entry(sel)
                with col3:
                    if "renaming" not in st.session_state:
                        if st.button("✏️ 이름 변경"):
                            st.session_state["renaming"] = True
                    else:
                        new_name = st.text_input(
                            "새 파일 이름 (확장자 제외)",
                            value=os.path.splitext(sel["filename"])[0]
                        )
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button("✅ 변경 저장"):
                                rename_entry(sel, new_name)
                        with c2:
                            if st.button("❌ 취소"):
                                del st.session_state["renaming"]
                                st.rerun()

# -------------------------------------
# 🖼 업로드 탭
# -------------------------------------
with tabs[1]:
    uploaded = st.file_uploader("사진 파일을 업로드하세요", type=["png", "jpg", "jpeg"])
    text = st.text_area("짧은 글을 입력하세요")

    if st.button("업로드"):
        if uploaded and text.strip():
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uploaded.name}"
            filepath = os.path.join(UPLOAD_DIR, filename)
            with open(filepath, "wb") as f:
                f.write(uploaded.getbuffer())

            entry = {
                "filename": filename,
                "path": filepath,
                "text": text.strip(),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            data.append(entry)
            save_data(data)
            st.success("✅ 업로드 완료!")
            st.rerun()
        else:
            st.warning("사진과 글을 모두 입력해주세요.")
