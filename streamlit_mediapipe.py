import streamlit as st
import mediapipe as mp
from PIL import Image
import cv2
import numpy as np
import time

# Set the page to wide mode
st.set_page_config(layout="wide")

# Fungsi untuk mendeteksi arah hadap wajah menggunakan MediaPipe
def detect_face_direction(image):
    # Inisialisasi model MediaPipe Face Detection
    face_detection = mp.solutions.face_detection
    mp_face_detection = face_detection.FaceDetection(min_detection_confidence=0.3)

    # Konversi gambar PIL ke format OpenCV
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Deteksi wajah pada gambar
    results = mp_face_detection.process(image_cv)

    # Menggambar kotak di sekitar wajah dan menampilkan hasil prediksi
    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = image_cv.shape
            bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                   int(bboxC.width * iw), int(bboxC.height * ih)

            # Mendapatkan landmark wajah
            landmarks = detection.location_data.relative_keypoints
            left_eye = landmarks[1].x, landmarks[1].y
            right_eye = landmarks[0].x, landmarks[0].y
            nose = landmarks[2].x, landmarks[2].y

            # Menghitung persentase nilai berdasarkan posisi hidung di antara posisi mata
            percentage = calculate_percentage(left_eye, right_eye, nose)

            # Mendapatkan nilai confidence (persentase kepercayaan)
            confidence = detection.score[0]

            # Menampilkan arah hadap wajah, confidence score, dan label
            direction_label = determine_face_direction(left_eye, right_eye, nose)
            st.write(f'Arah Wajah Terdeksi: {direction_label}')
            st.write(f'Confidence Score: {confidence*100:.2f}%')

            # Menampilkan hasil prediksi pada gambar
            cv2.rectangle(image_cv, bbox, (0, 255, 0), 2)
            cv2.putText(image_cv, f'Face Direction: {direction_label} - Confidence: {confidence*100:.2f}%',
                        (bbox[0], bbox[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image_cv, direction_label, confidence

# Fungsi untuk menentukan arah hadap wajah berdasarkan landmark
def determine_face_direction(left_eye, right_eye, nose):
    # Contoh implementasi sederhana
    # Di sini, kita bisa menggunakan perbandingan posisi mata dan hidung
    # untuk mendeteksi arah hadap kasar seperti "forward", "looking right", "looking left", dll.
    if right_eye[0] < nose[0] < left_eye[0]:
        return "Depan"
    elif nose[0] < right_eye[0]:
        return "Kanan"
    elif nose[0] > left_eye[0]:
        return "Kiri"
    else:
        return "Undetermined"

# Fungsi untuk menghitung persentase nilai berdasarkan posisi hidung di antara posisi mata
def calculate_percentage(left_eye, right_eye, nose):
    eye_distance = np.linalg.norm(np.array(left_eye) - np.array(right_eye))
    percentage = (nose[0] - right_eye[0]) / eye_distance
    return percentage * 100

# Fungsi utama aplikasi Streamlit
def main():
    # Menambahkan sidebar dengan logo
    st.sidebar.image("logo.png", use_column_width=True)

    # Judul dan deskripsi aplikasi
    st.title("Multi Factor Authentication with Face Recognition (Using Camera)")
    st.markdown("Fitur Rekognisi Wajah pada aplikasi ini menggunakan model yang disediakan oleh <strong>library Mediapipe yang menyediakan fitur untuk melakukan Face Detection.</strong> Untuk melakukan pengujian pada aplikasi ini, User bisa langsung menggunakan Foto Wajah User. User harus menjalankan serangkaian Alur Autentikasi agar User dapat masuk ke Sistem.", unsafe_allow_html=True)
    
    # autentikasi arah depan
    st.markdown("<br>", unsafe_allow_html = True)
    st.subheader("[Autentikasi 1] - Capture gambar menghadap Depan")
    # uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="auth_1")
    uploaded_image = st.camera_input("Take a picture", key="auth_1")
    if uploaded_image is not None:
        image = Image.open(uploaded_image)
        # st.image(image, caption="Uploaded Image - Depan", use_column_width=True)

        # Memproses deteksi arah hadap wajah
        result_image, direction_label, confidence = detect_face_direction(image)

        # Menampilkan hasil deteksi
        st.image(result_image, caption="Face Detection Result", use_column_width=True)
        
        # cek autentikasi arah depan
        if direction_label == "Depan" and confidence > 0.8:
            st.success("Autentikasi Pertama berhasil👌")
            
            # autentikasi arah kanan
            st.markdown("<br><br>", unsafe_allow_html = True)
            st.subheader("[Autentikasi 2] - Capture gambar menghadap Kanan")
            # uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="auth_2")
            uploaded_image = st.camera_input("Take a picture", key="auth_2")
            if uploaded_image is not None:
                image = Image.open(uploaded_image)
                # st.image(image, caption="Uploaded Image - Kanan", use_column_width=True)

                # Memproses deteksi arah hadap wajah
                result_image, direction_label, confidence = detect_face_direction(image)

                # Menampilkan hasil deteksi
                st.image(result_image, caption="Face Detection Result", use_column_width=True)

                # cek autentikasi arah kanan
                if direction_label == "Kanan" and confidence > 0.8:
                    st.success("Autentikasi Kedua berhasil👍")
                    
                    # autentikasi arah kiri
                    st.markdown("<br><br>", unsafe_allow_html = True)
                    st.subheader("[Autentikasi Terakhir] - Capture gambar menghadap Kiri")
                    # uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"], key="auth_3")
                    uploaded_image = st.camera_input("Take a picture", key="auth_3")
                    if uploaded_image is not None:
                        image = Image.open(uploaded_image)
                        # st.image(image, caption="Uploaded Image - Kiri", use_column_width=True)

                        # Memproses deteksi arah hadap wajah
                        result_image, direction_label, confidence = detect_face_direction(image)

                        # Menampilkan hasil deteksi
                        st.image(result_image, caption="Face Detection Result", use_column_width=True)

                        # cek autentikasi arah kiri
                        if direction_label == "Kiri" and confidence > 0.8:
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
                            st.warning("Autentikasi Kiri Gagal😑 Foto harus menghadap Kiri dan akurasi harus di atas 80%. Ulangi Capture Gambar")
                else:
                    st.warning("Autentikasi Kedua Gagal😢 Foto harus menghadap Kanan dan akurasi harus di atas 80%. Ulangi Capture Gambar")
        else:
            st.warning("Autentikasi Pertama Gagal😒 Foto harus menghadap Depan dan akurasi harus di atas 80%. Ulangi Capture Gambar")

if __name__ == "__main__":
    main()
