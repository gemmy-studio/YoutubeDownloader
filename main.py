import os
import glob
import streamlit as st
from streamlit.components.v1 import html
import yt_dlp as ydl


def main():
    st.set_page_config(page_title="Youtube 동영상 다운로더", page_icon="favicon.ico",
                       layout="centered", initial_sidebar_state="auto", menu_items=None)

    # button = """
    # <script data-name="BMC-Widget" data-cfasync="false" src="https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js" data-id="woojae" data-description="Support me on Buy me a coffee!" data-message="방문해주셔서 감사합니다 :)" data-color="#40DCA5" data-position="Right" data-x_margin="18" data-y_margin="18"></script>
    # """

    st.title('Youtube 동영상 다운로더')
    multi = '''
            1. 본 서비스를 통해 다운로드 받은 영상의 상업적 이용이나 무단 배포는 금지됩니다.
            2. 모든 영상의 저작권은 원작자에게 있으며, 영상 이용에 대한 책임은 사용자에게 있습니다.
            3. 자세한 내용은 YouTube 이용 정책 및 각 영상의 저작권 정보를 참고해주시기 바랍니다.
            '''
    st.markdown(multi)

    url = st.text_input(
        'Youtube URL을 입력해주세요. (예: https://www.youtube.com/watch?v=CoyQM_Zi0OM)')

    option = st.selectbox(
        '다운로드 타입 설정',
        ('video', 'audio'))

    if st.button('동영상 불러오기'):
        with st.spinner('불러오기 중'):
            # 이전에 다운로드 한 파일을 삭제
            files_to_remove = glob.glob('downloaded_*')
            for file in files_to_remove:
                os.remove(file)

            # 영상 임베드
            st.video(url)

            if option == 'video':
                # yt_dlp 옵션 설정
                ydl_opts = {
                    'format': 'bestvideo+bestaudio/best',
                    'outtmpl': 'downloaded_video.%(ext)s'  # 다운로드할 파일의 이름 설정
                }

                # YouTube 동영상 다운로드
                with ydl.YoutubeDL(ydl_opts) as ydl_instance:
                    # 영상 정보 추출
                    info_dict = ydl_instance.extract_info(url, download=False)
                    # 실제 파일 경로와 이름 가져오기
                    file_name = ydl_instance.prepare_filename(info_dict)

                    ydl_instance.download([url])

                    with open(file_name, 'rb') as f:
                        video_bytes = f.read()
                        st.download_button('다운로드', video_bytes, file_name=file_name.split(
                            '/')[-1], mime='video/{}'.format(file_name.split('.')[-1]))

            if option == 'audio':
                # yt_dlp 옵션 설정
                ydl_opts = {
                    'format': 'bestaudio/best',  # 오디오만 선택
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',  # FFmpeg를 사용하여 오디오 추출
                        'preferredcodec': 'wav',  # 추출할 오디오 형식을 wav로 설정
                        'preferredquality': '192',  # 오디오 품질 설정 (예: 192kbps)
                    }],
                    'outtmpl': 'downloaded_audio.%(ext)s'  # 다운로드할 파일의 이름 설정
                }

                # YouTube 오디오 다운로드
                with ydl.YoutubeDL(ydl_opts) as ydl_instance:
                    # 오디오 정보 추출
                    info_dict = ydl_instance.extract_info(url, download=False)
                    # 실제 파일 경로와 이름 가져오기
                    file_name = 'downloaded_audio.wav'

                    ydl_instance.download([url])

                    with open(file_name, 'rb') as f:
                        audio_bytes = f.read()
                        st.download_button(
                            '다운로드', audio_bytes, file_name=file_name, mime='audio/wav')

    # html(button, height=600, width=400)

    # st.markdown(
    #     """
    #     <style>
    #         iframe[width="400"] {
    #             position: fixed;
    #             bottom: 60px;
    #             right: 40px;
    #         }
    #     </style>
    #     """,
    #     unsafe_allow_html=True,
    # )


if __name__ == '__main__':
    main()
