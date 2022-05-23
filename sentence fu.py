import re

def get_sentence():
    pass

def refine_sentence(sentence_):
    return sentence_

class Chatsort:
    def __init__(self):
        pass
    def get_sentence(self):
        pass
    def refine_sentence(self):
        pass
    def run_(self):
        pass
    def print_(self):

if __name__ == "__main__":
    cs_ = Chatsort()

while True:

    import pytchat  # 실시간 댓글 크롤링
    import pafy  # 유튜브 정보
    import pandas as pd

    api_key = '<api_key>'  # gcp youtube data api 에서 api key 생성
    pafy.set_api_key(api_key)

    video_id = 'GoXPbGQl-uQ'  # [LIVE] 대한민국 24시간 뉴스채널 YTN
    file_path = './news_ytn_youtube.csv'

    empty_frame = pd.DataFrame(columns=['제목', '채널 명', '스트리밍 시작 시간', '댓글 작성자', '댓글 내용', '댓글 작성 시간'])
    chat = pytchat.create(video_id=video_id)

    while chat.is_alive():
        cnt = 0
        try:
            data = chat.get()
            items = data.items
            for c in items:
                print(f"{c.datetime} [{c.author.name}]- {c.message}")
                data.tick()
                data2 = {'제목': [title], '채널 명': [author], '스트리밍 시작 시간': [published], '댓글 작성자': [c.author.name],
                         '댓글 내용': [c.datetime], '댓글 작성 시간': [c.message]}
                result = pd.DataFrame(data2)
                result.to_csv(file_path, mode='a', header=False)
            cnt += 1
            if cnt == 5: break
        except KeyboardInterrupt:
            chat.terminate()
            break

    df = pd.read_csv(file_path, names=['제목', '채널명', '스트리밍 시작 시간', '댓글 작성자', '댓글 작성시간', '댓글내용'])
    df.head(30)