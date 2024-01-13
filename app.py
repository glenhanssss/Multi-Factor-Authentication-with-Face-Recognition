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
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
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
    st.markdown("<h6 style='color: red;'> It should be noted that the Developer of this project aims to offer a multi-factor Authentication algorithm and feature that is different from previous authentications, so that the application is made in such a way as to be simple. It is very possible that in the future, this MFA feature will be developed not only based on facial recognition but also other recognitions such as voice, facial landmarks, and others. </h6>", unsafe_allow_html=True)
    st.markdown("This Web Application allows the User to carry out a series of Facial Authentications based on the direction the User's Face is facing, starting from facing Front-Right-Left so that the User can enter the System. If one authentication is unsuccessful, the user will not be able to continue with the next authentication, and the user will not be able to successfully enter the system. <strong>[TRY this APP with a CAMERA using the MEDIAPIPE Face Detection model.](https://4uth-with-mediapipe.streamlit.app/)</strong>", unsafe_allow_html=True)
    st.markdown("The Face Recognition feature in this application is only trained or developed through model training based on the faces of several members of our team, so to test this application, facial photos are needed from the validation data that our team provides. To test the Multi Factor Authentication feature in this application, users can upload photos from the General_DATAI_1/Source/Prototype/Validation folder or [Click Here](https://drive.google.com/drive/folders/1yItI63yETPxQjCGQ5de-KhHluHHxhVx9?usp=sharing)</strong> to view and download photos for application testing. After the user has test data or photos, they just have to select the photo that will be used to test the application's features.", unsafe_allow_html=True)
    st.markdown("Due to the limitations of the dataset we have, if this project is to be developed, we will re-train the data with a dataset based on the faces of all users (application users). Check out the [Application demo video](https://drive.google.com/drive/folders/1-3udJnphEkqAxB2DiEXvlR2jVzlRcwTF?usp=sharing)</strong> and Check the [Documentation or source code here.](https://github.com/glenhanssss/Multi-Factor-Authentication-with-Face-Recognition)", unsafe_allow_html=True)

    #auth_1
    st.markdown("<br><br>", unsafe_allow_html = True)
    st.subheader("[Autentikasi 1] - Masukkan foto menghadap Depan")
    uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_1")
    # uploaded_file = st.camera_input("Take a picture", key="auth_1")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")

        # Get prediction
        class_name, confidence_score = predict(uploaded_file)

        st.write(f"Class: {class_name}")
        st.write(f"Confidence Score: {confidence_score:.2%}")

        # cek kondisi pertama
        if class_name.strip().lower() == "depan" and confidence_score > 0.8:
            st.success("Autentikasi Pertama berhasil👌")
            
            # auth_2
            st.markdown("<br><br>", unsafe_allow_html = True)
            st.subheader("[Autentikasi 2] - Masukkan foto menghadap Kanan")
            uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_2")
            # uploaded_file = st.camera_input("Take a picture", key="auth_2")

            if uploaded_file is not None:
                st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
                st.write("")

                # Get prediction
                class_name, confidence_score = predict(uploaded_file)

                st.write(f"Class: {class_name}")
                st.write(f"Confidence Score: {confidence_score:.2%}")

                # cek kondisi kedua
                if class_name.strip().lower() == "kanan" and confidence_score > 0.8:
                    st.success("Autentikasi Kedua berhasil👍")

                    #auth_3
                    st.markdown("<br><br>", unsafe_allow_html = True)
                    st.subheader("[Autentikasi Terakhir] -Masukkan foto menghadap Kiri")
                    uploaded_file = st.file_uploader("Choose an image...", type="jpg", key="auth_3")
                    # uploaded_file = st.camera_input("Take a picture", key="auth_3")

                    if uploaded_file is not None:
                        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
                        st.write("")

                        # Get prediction
                        class_name, confidence_score = predict(uploaded_file)

                        st.write(f"Class: {class_name}")
                        st.write(f"Confidence Score: {confidence_score:.2%}")

                        # cek kondisi ketiga
                        if class_name.strip().lower() == "kiri" and confidence_score > 0.8:
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
                            st.warning("Autentikasi Ketiga Gagal😑 Foto harus menghadap Kiri dan akurasi harus diatas 80%. Ulangi Upload Foto")
                else:
                    st.warning("Autentikasi Kedua Gagal😢 Foto harus menghadap Kanan dan akurasi harus diatas 80%. Ulangi Upload Foto")
        else:
            st.warning("Autentikasi Pertama Gagal😒 Foto harus menghadap Depan dan akurasi harus diatas 80%. Ulangi Upload Foto")

    st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; height: 200px;">
        <a href="https://linktr.ee/glenhans" style="text-align: center; font-size: 24px;"> Kontak Kami 😄 </a>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
