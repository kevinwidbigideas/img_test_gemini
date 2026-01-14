# 라이브러리 가져오고 api key를 환경 변수에서 가져오기
import os
from PIL import Image
import google.genai as genai
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

# 1. 클라이언트 생성 (API 키 설정)
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# client 객체의 models.generate_content 사용
def classify_image(prompt, image, model):
    response = client.models.generate_content(
        model=model, 
        contents=[prompt, image]
    )
    return response.text
    

st.set_page_config(
    page_title="인종차별이 아닌, 분류입니다.",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)
# -1) model 선택하기 : st.sidebar / st.selectbox
st.title('인종 :red[~~차별~~]분류기 - Gemini')

with st.sidebar :
    model = st.selectbox('모델 선택',
                     options = ['gemini-2.0-flash', 'gemini-2.0'],
                     index=0)

prompt = """
사진을 보고 다음 보기 내용이 포함되면 '사람'으로, 포함되지 않으면 '탈락입니다.'로 출력해줘..
보기 = [황인종, 백인]
"""


st.text_area('프롬프트 입력', value=prompt, height=200)
# -3) 이미지 업로드하기 : st.file_uploader
uploaded_file = st.file_uploader('사진을 올려보세요. :red[어디 한 번].', type=['jpg', 'jpeg', 'png', 'white'])

# -4) 업로드한 이미지 보여주기 : st.image
if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img,caption='업로드된 이미지', width = 'stretch')
    
    
# -5) 분류 실행하기 : st.button /st.spinner
    if st.button('분류실행'):
        with st.spinner(':red[차ㅂ]..아니 분류 중...'):
            response = classify_image(prompt,img,model=model)
        

# -6) 결과 출력하기 : st.write / st.code
        st.header('이거지~')
        st.code(response)

