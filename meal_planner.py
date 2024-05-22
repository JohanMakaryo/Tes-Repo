import streamlit as st
from streamlit_tags import st_tags
import openai

# flake8: noqa
# Set the OpenAI API key
openai.api_key = st.secrets["openai_key"]


# Define the function to call GPT-3.5-turbo API
def ask_gpt3_turbo(message, chat_log=None):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "Anda adalah AI agent yang bertindak sebagai event planner andal yang bisa memikirikan jadwal dan susunan acara. Anda adalah event planner yang sangat ahli dalam acara casual,semi formal, dan formal.",
            },
            {"role": "user", "content": message},
        ],
    )
    # Returning the response
    return response.choices[0].message.content


# Streamlit app
def main():
    st.title("Event Planner")

    tipe = st_tags(label="Tipe Acara")
    acara = st_tags(
        label="(optional) Sebutkan acara yang sudah pernah dirancang"
    )
    gaya_acara = st.text_input(
        "(optional) Anda ingin gaya acara seperti apa? (Misalnya: casual, semi formal, formal)"
    )
    tempat_acara = st.radio("Opsi tempat acara", ("Outdoor", "Indoor"))
    agama_budaya = st.text_input(
        "(optional) Apakah Anda memiliki batasan seperti alkohol atau non alkohol?"
    )
    durasi_acara = st.radio(
        "Anda mencari acara dengan durasi kurang dari 4 jam atau maksimal 4 jam?",
        ("kurang dari 4 jam", "maksimal 4 jam"),
    )
    metode = st.multiselect("Preferensi kostum / dresscode", ["casual", "semi formal", "formal"])
    jenis = st.radio(
        "Anda mencari konsep acara seperti?", ("casual", "semi formal", "formal")
    )
    partisipan = st.number_input(
        "Berapa banyak orang yang akan menghadiri acara Anda?", min_value=1, max_value=100, step=1
    )

    if st.button("Kirim"):

        prompt = f"""
                Buatkan saya 3 jadwal dan susunan acara sesuai kriteria berikut ini, perlu dicatat anda tidak perlu memakai semua konsep, anda bisa menambahkan hal lain yang diperlukan untuk acara ini, dan anda bisa mengatur acaranya nanti akan seperti apa.

                Konsep acara: {konsep}
                Tipe acara yang sudah saya bikin: {acara}
                Jenis acara: {jenis_acara}
                Opsi alkohol / non alkohol: {alkohol_non_alkohol}
                Gaya acara: {gaya_acara}
                Suasana acara: {suasana_acara}
                Kostum: {kostum}
                Jumlah partisipan: {jumlah_partisipan}
        
                Format output:
                #[Tipe acara]
                ##Suasana acara:
                [konten]

                ##Jenis acara:
                [konten]

                ##Jadwal acara:
                [konten]
        """

        # user_input += additional_prompt
        ai_response = ask_gpt3_turbo(prompt)

        # print(ai_response)
        st.markdown(f"{ai_response}", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
