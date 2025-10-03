from dotenv import load_dotenv
from graph.graph import app
load_dotenv()
import streamlit as st
import io
import contextlib
from datetime import datetime
from pathlib import Path


# Sayfa ayarları
st.set_page_config(layout="wide", page_title="note.py Arayüzü", page_icon="📝")

# -------------------
# Session state başlangıç
# -------------------
if "notes" not in st.session_state:
    st.session_state.notes = [
        {"title": "İlk Not", "markdown": "# Hoş geldiniz\nBurada markdown yazabilirsiniz.", "code": "print('Merhaba Dünya!')"}
    ]
if "selected_note_idx" not in st.session_state:
    st.session_state.selected_note_idx = 0

if "conversations" not in st.session_state:
    # Her sohbet: {"created_at": datetime, "messages": [{role, content}]}
    st.session_state.conversations = [
        {"created_at": datetime.now(), "messages": []}
    ]
if "current_conv_idx" not in st.session_state:
    st.session_state.current_conv_idx = 0

# Üst başlık alanı (logo + başlık)
with st.container():
    st.markdown("<h1 style='margin:0;text-align:center'>note.py</h1><p style='margin-top:4px;color:#64748B;text-align:center'>Notlar, Markdown, Python ve Sohbet</p>", unsafe_allow_html=True)
    st.markdown("---")

# Layout: üç sütun (sol, orta, sağ)
left_col, center_col, right_col = st.columns([1.2, 3, 1])

# -------------------
# Sol panel (Notlar)
# -------------------
with left_col:
    st.header("Notlar")
    st.markdown("<style>.stRadio > label{display:none}</style>", unsafe_allow_html=True)

    # Not ekleme
    with st.form("note_add_form", clear_on_submit=True):
        new_title = st.text_input("Yeni not başlığı")
        submitted = st.form_submit_button("Ekle")
        if submitted and new_title.strip():
            st.session_state.notes.append({"title": new_title.strip(), "markdown": "", "code": ""})
            st.session_state.selected_note_idx = len(st.session_state.notes) - 1

    # Arama/filtre
    filter_query = st.text_input("Ara", placeholder="Başlıkta ara…")
    filtered = [
        (i, note) for i, note in enumerate(st.session_state.notes)
        if not filter_query or filter_query.lower() in (note["title"] or "").lower()
    ]

    # Not listesi
    note_titles = [note["title"] or f"Not {i+1}" for i, note in filtered]
    default_index = 0
    for j, (orig_idx, _) in enumerate(filtered):
        if orig_idx == st.session_state.selected_note_idx:
            default_index = j
            break
    selected_title = st.radio("Notlar", note_titles, index=default_index if note_titles else 0, key="notes_radio") if note_titles else None
    if selected_title is not None:
        # Yeni seçimi gerçek indeksine çevir
        st.session_state.selected_note_idx = filtered[note_titles.index(selected_title)][0]

    # Seçili not işlemleri
    sel_idx = st.session_state.selected_note_idx
    if 0 <= sel_idx < len(st.session_state.notes):
        with st.expander("Seçili not işlemleri", expanded=True):
            new_name = st.text_input("Yeniden adlandır", value=st.session_state.notes[sel_idx]["title"], key=f"rename_input_{sel_idx}")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("Kaydet"):
                    st.session_state.notes[sel_idx]["title"] = new_name.strip() or st.session_state.notes[sel_idx]["title"]
            with col_b:
                confirm_delete = st.checkbox("Silmeyi onayla", key=f"confirm_del_{sel_idx}")
                if st.button("Sil") and confirm_delete:
                    del st.session_state.notes[sel_idx]
                    if not st.session_state.notes:
                        st.session_state.notes.append({"title": "Yeni Not", "markdown": "", "code": ""})
                    st.session_state.selected_note_idx = max(0, min(sel_idx, len(st.session_state.notes) - 1))
                    st.experimental_rerun()
            with col_c:
                # Önceki/sonraki kısayolları
                prev_disabled = sel_idx <= 0
                next_disabled = sel_idx >= len(st.session_state.notes) - 1
                if st.button("← Önceki", disabled=prev_disabled):
                    st.session_state.selected_note_idx -= 1
                    st.experimental_rerun()
                if st.button("Sonraki →", disabled=next_disabled):
                    st.session_state.selected_note_idx += 1
                    st.experimental_rerun()

# -------------------
# Orta panel (Başlık + Markdown/Python)
# -------------------
with center_col:
    sel_idx = st.session_state.selected_note_idx
    note = st.session_state.notes[sel_idx]

    st.header("Çalışma Alanı")
    note_title = st.text_input("Başlık", value=note["title"], key=f"center_title_input_{sel_idx}")
    if note_title != note["title"]:
        note["title"] = note_title

    tabs = st.tabs(["Markdown", "Python Kod"])

    # Markdown sekmesi
    with tabs[0]:
        col_edit, col_preview = st.columns(2)
        with col_edit:
            md_content = st.text_area("Markdown", value=note["markdown"], height=300, key=f"md_text_area_{sel_idx}")
            note["markdown"] = md_content
            st.download_button(
                label="Markdown'u indir",
                data=md_content,
                file_name=f"{note['title'] or 'not'}.md",
                mime="text/markdown"
            )
        with col_preview:
            st.markdown("Önizleme", help="Markdown içeriğinin canlı önizlemesi")
            st.markdown(md_content or "_Henüz içerik yok_", unsafe_allow_html=False)

    # Python sekmesi
    with tabs[1]:
        code_content = st.text_area("Python kodu", value=note["code"], height=300, key=f"py_text_area_{sel_idx}")
        note["code"] = code_content
        run = st.button("Kodu Çalıştır")
        if run:
            stdout_buffer = io.StringIO()
            exec_globals = {}
            try:
                with contextlib.redirect_stdout(stdout_buffer):
                    exec(code_content, exec_globals)
                output = stdout_buffer.getvalue()
                if not output:
                    output = "(Çıktı yok)"
                st.success("Çalıştırma tamamlandı")
                st.code(output)
            except Exception as ex:
                st.error(f"Hata: {ex}")

# -------------------
# Sağ panel (Sohbetler)
# -------------------
with right_col:
    st.header("Sohbetler")

    # Sohbet seçimi ve yeni konuşma
    conv_labels = [
        f"Sohbet {i+1} - {c['created_at'].strftime('%d.%m %H:%M')} ({len(c['messages'])} msj)"
        for i, c in enumerate(st.session_state.conversations)
    ]

    if conv_labels:
        current_label = conv_labels[st.session_state.current_conv_idx]
    else:
        current_label = None

    selected_conv = st.selectbox(
        "Önceki konuşmalar",
        options=conv_labels,
        index=st.session_state.current_conv_idx if conv_labels else 0,
        key="conv_select"
    ) if conv_labels else None

    if selected_conv is not None:
        st.session_state.current_conv_idx = conv_labels.index(selected_conv)

    if st.button("Yeni konuşma"):
        st.session_state.conversations.insert(0, {"created_at": datetime.now(), "messages": []})
        st.session_state.current_conv_idx = 0

    # Yeni mesaj girişi
    user_msg = st.chat_input("Mesaj yazın…", key="chat")
    conv = st.session_state.conversations[st.session_state.current_conv_idx]
    if user_msg and user_msg.strip():
        conv["messages"].append({"role": "user", "content": user_msg})
        try:
            result = app.invoke(input={"question": user_msg})
            reply = result.get("generation") or "(generation alanı boş)"
        except Exception as ex:
            reply = f"Hata: {ex}"
        conv["messages"].append({"role": "assistant", "content": reply})

    # Sohbet mesajlarını ekleme-sonrası render et
    for msg in conv["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

#    if __name__ == "__main__":
#        result = app.invoke(input={"question": f"{user_msg}"})
#        print("\n--- CEVAP ---\n")
#        print(result.get("generation", "(generation alanı boş)"))
