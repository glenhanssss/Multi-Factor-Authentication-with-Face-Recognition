import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
import time

# Set the page to wide mode
st.set_page_config(layout="wide")

# Load the model
model = load_model("trained_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def predict(image_path):
    # Create the array of the right shape to feed into the keras model
    data = np.ndarray(shape=(1, 128, 128, 3), dtype=np.float32)

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    size = (128, 128)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array

    # Make prediction
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index][2:]
    confidence_score = prediction[0][index]

    return class_name, confidence_score

def main():
    # Menambahkan sidebar dengan logo
    st.sidebar.image("logo.png", use_column_width=True)

    # Judul dan deskripsi aplikasi
    st.title("Multi Factor Authentication with Face Recognition")
    st.markdown("<h6 style='color: red;'> Perlu diperhatikan bahwa Developer dari proyek ini mempunyai maksud untuk menawarkan Algoritma/Fitur Autentikasi multi faktor yang berbeda dari autentikasi-autentikasi sebelumnya, sehingga aplikasi memang dibuat sedemikian rupa agar menjadi sederhana. Sangat dimungkinkan jika fitur MFA ini kedepannya ingin dikembangkan tidak hanya berdasarkan pengenalan Wajah, tetapi pengenalan lain juga seperti suara, landmark wajah, dan lainnya. </h6>", unsafe_allow_html=True)
    st.markdown("Aplikasi Web ini memungkinkan User untuk menjalankan serangkaian Autentikasi Wajah berdasarkan arah menghadap Wajah User, yaitu dimulai dari menghadap Depan-Kanan-Kiri agar User dapat masuk ke Sistem. Jika salah satu Autentikasi tidak berhasil maka User tidak akan bisa melanjutkan Autentikasi berikutnya dan User tidak akan berhasil masuk kedalam Sistem.", unsafe_allow_html=True)
    st.markdown("Fitur Rekognisi Wajah pada aplikasi ini hanya dilatih atau melalui <strong>model training berdasarkan Wajah dari salah satu anggota tim kami yaitu Amrina</strong> sehingga untuk melakukan uji coba aplikasi ini, diperlukan foto Wajah dari Amrina. <strong>Untuk melakukan uji coba fitur Multi Faktor Autentikasi pada aplikasi ini, User dapat melakukan upload foto dari folder Umum_DATAI_1/Source/Prototype/Validation</strong> atau [Klik Disini](https://drive.google.com/drive/folders/1yItI63yETPxQjCGQ5de-KhHluHHxhVx9?usp=sharing) untuk melihat dan download foto uji guna Pengujian Aplikasi. Setelah User memiliki Data/Foto uji, User tinggal memilih foto yang akan digunakan untuk menguji fitur Aplikasi.", unsafe_allow_html=True)
    st.markdown("<strong>Karena keterbatasan Dataset yang kami miliki, apabila project ini ingin dikembangkan, kami akan melakukan training data ulang dengan dataset berdasarkan Wajah dari seluruh User (pengguna aplikasi). [Cek Video Demo aplikasi](https://drive.google.com/file/d/1bx9cyzracMdTE9QuJo9uR5DfGwDE6Fqk/view)</strong>", unsafe_allow_html=True)

    #auth_1
    st.markdown("<br><br>", unsafe_allow_html = True)
    st.subheader("Masukkan foto menghadap Depan")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_1")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")

        # Get prediction
        class_name, confidence_score = predict(uploaded_file)

        st.write(f"Class: {class_name}")
        st.write(f"Confidence Score: {confidence_score:.2%}")

        # cek kondisi pertama
        if class_name.strip().lower() == "depan" and confidence_score > 0.9:
            st.success("Autentikasi Pertama berhasil👌")
            
            # auth_2
            st.markdown("<br><br>", unsafe_allow_html = True) 
            st.subheader("Masukkan foto menghadap Kanan")
            uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_2")

            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
                st.write("")

                # Get prediction
                class_name, confidence_score = predict(uploaded_file)

                st.write(f"Class: {class_name}")
                st.write(f"Confidence Score: {confidence_score:.2%}")

                # cek kondisi kedua
                if class_name.strip().lower() == "kanan" and confidence_score > 0.9:
                    st.success("Autentikasi Kedua berhasil👍")

                    #auth_3
                    st.markdown("<br><br>", unsafe_allow_html = True)
                    st.subheader("Masukkan foto menghadap Kiri")
                    uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_3")

                    if uploaded_file is not None:
                        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
                        st.write("")

                        # Get prediction
                        class_name, confidence_score = predict(uploaded_file)

                        st.write(f"Class: {class_name}")
                        st.write(f"Confidence Score: {confidence_score:.2%}")

                        # cek kondisi ketiga
                        if class_name.strip().lower() == "kiri" and confidence_score > 0.9:
                            st.success("Autentikasi Selesaiiii 😁")
                            st.balloons()
                            # setelah semua autentikasi brehasil, akan langsung redirect masuk ke sistem
                            with st.spinner('Mohon tunggu 5 detik, sedang menuju Sistem...'):
                                time.sleep(5)
                                image_path = "ceritanya_tampilan_Sistem.jpg"
                                image = Image.open(image_path)
                                st.image(image, use_column_width=True)
                                st.markdown("<h4 style='color: red;'> Perlu diperhatikan bahwa Developer dari proyek ini mempunyai maksud untuk menawarkan Algoritma/Fitur Autentikasi multi faktor yang berbeda dari autentikasi-autentikasi sebelumnya, sehingga aplikasi memang dibuat sedemikian rupa agar menjadi sederhana. Sangat dimungkinkan jika fitur MFA ini kedepannya ingin dikembangkan tidak hanya berdasarkan pengenalan Wajah, tetapi pengenalan lain juga seperti suara, landmark wajah, dan lainnya. </h4>", unsafe_allow_html=True)
                        else:
                            st.warning("Autentikasi Ketiga Gagal😑 Foto harus menghadap Kiri dan akurasi harus diatas 90%. Ulangi Upload Foto")
                else:
                    st.warning("Autentikasi Kedua Gagal😢 Foto harus menghadap Kanan dan akurasi harus diatas 90%. Ulangi Upload Foto")
        else:
            st.warning("Autentikasi Pertama Gagal😒 Foto harus menghadap Depan dan akurasi harus diatas 90%. Ulangi Upload Foto")

    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <a href="wa.me/6285778822048" style="text-align: center; font-size: 24px;"> Kontak Kami 😄 </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
