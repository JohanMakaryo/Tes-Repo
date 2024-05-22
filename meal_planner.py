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
                "content": "Anda adalah AI agent yang bertindak sebagai chef andal yang bisa memikirikan resep makan dari bahan-bahan yang terbatas. Anda adalah chef yang sangat ahli dalam masakan Indonesia dan nusantara.",
            },
            {"role": "user", "content": message},
        ],
    )
    # Returning the response
    return response.choices[0].message.content


# Streamlit app
def main():
    st.title("Detikfood Meal Prep Planner")

    bahan = st_tags(label="Daftarkan bahan-bahan di dapur Anda")
    makanan = st_tags(
        label="(optional) Sebutkan makanan apa saja yang sudah Anda masak"
    )
    daerah = st.text_input(
        "(optional) Anda mencari resep khas daerah mana? (Misalnya: Jawa, Sumatera, Bali)"
    )
    ramah_anak = st.radio("Opsi makanan ramah anak", ("Tidak", "Ya"))
    agama_budaya = st.text_input(
        "(optional) Apakah Anda memiliki batasan seperti halal atau vegetarian?"
    )
    kompleks = st.radio(
        "Anda mencari resep yang sederhana dan cepat atau yang lebih kompleks?",
        ("Sederhana dan cepat", "Kompleks"),
    )
    metode = st.multiselect("Preferensi metode memasak", ["goreng", "rebus", "bakar"])
    jenis = st.radio(
        "Anda mencari resep untuk?", ("sarapan", "makan siang", "makan malam")
    )
    porsi = st.number_input(
        "Untuk berapa orang Anda akan memasak?", min_value=1, max_value=5, step=1
    )

    if st.button("Kirim"):

        prompt = f"""
                Buatkan saya 3 resep masakan berbeda berdasarkan kriteria berikut ini, perlu dicatat anda tidak perlu memakai semua bahan untuk satu resep, anda bisa menambahkan bumbu-bumbu dasar pada resep, dan anda bisa menggunakan alat dapur dasar dalam proses masak.

                Bahan-bahan: {bahan}
                Makanan yang sudah saya siapkan: {makanan}
                Jenis masakan daerah: {daerah}
                Opsi ramah anak: {ramah_anak}
                Pertimbangan agama/budaya: {agama_budaya}
                Kesederhanaan resep: {kompleks}
                metode memasak: {metode}
                jenis makanan: {jenis}
                porsi: {porsi} orang

                Format output:
                #[Nama Resep]
                ##Bahan-Bahan:
                [konten]

                ##Cara Memasak:
                [konten]

                ##Cara penyajian:
                [konten]
        """

        # user_input += additional_prompt
        ai_response = ask_gpt3_turbo(prompt)

        # print(ai_response)
        st.markdown(f"{ai_response}", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
