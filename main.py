from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_="sentence-transformers/all-distilroberta-v1"):
        self.model_ = model_
        self.embedder_ = SentenceTransformer()

    def run_(self):


from multiprocessing import Process, Queue
import time

import pytchat
# from IPython.display import clear_output
import time
from collections import deque

video_id = "oZg0RgUaGb8"
cnt_ = 0
time_s = time.time()


que_for_embed = deque()


ist_pc = pytchat.create(video_id=video_id)
while ist_pc.is_alive():
    clear_output(wait=True)
    print(cnt_, time.time() - time_s)
    try:
        for each_c in ist_pc.get().sync_items():
            time_, id_, mes_original = each_c.datetime, each_c.author.channelId , each_c.message
            cnt_ += 1



def data_source(que_origin):
    video_id = "oZg0RgUaGb8"
    ist_pc = pytchat.create(video_id=video_id)
    while ist_pc.is_alive():
        for each_c in ist_pc.get().sync_items():
            d_time, d_uid, d_mes = each_c.datetime, each_c.author.channelId, each_c.message
            que_origin.put([d_time, d_uid, d_mes])
    que_origin.put([-1,0,0])
    return


def embedder(que_origin, que_embedded):
    model_ = SentenceTransformer('sentence-transformers/all-distilroberta-v1')
    t_last_u = time.time()
    is_run = True
    while is_run:
        if 1.0 <= (time.time() - t_last_u) or 32 <= len(que_origin):
            t_last_u = time.time()
            lst_time = []
            lst_uid = []
            lst_mes_o = []
            for _ in range(32):
                if not que_origin:
                    break
                else:
                    s_time, s_uid, s_mes_o = que_origin.get()
                    if s_time == -1:
                        is_run = False
                        break
                    lst_time.append(s_time)
                    lst_uid.append(s_uid)
                    lst_mes_o.append(s_mes_o)
            lst_mes_e = model_.encode(lst_mes_o, convert_to_numpy=True)

            for p_time, p_uid, p_mes_o, p_mes_e in zip(lst_time,lst_uid,lst_mes_o,lst_mes_e):
                que_embedded.put([p_time, p_uid, p_mes_o, p_mes_e])
        else:
            time.sleep(.1)
    que_embedded.put([-1,0,0,0])
    return

def printer(que_embedded):
    t_last_u = time.time()
    is_run = True

    while is_run:
        if 1.0 <= (time.time() - t_last_u):
            t_last_u = time.time()

        else:
            time.sleep(.1)

if __name__ == "__main__":
    que_origin = Queue()
    que_embedded = Queue()

    p_dts = Process(target=data_source, args=())
    p_emb = Process(target=data_source, args=())
    p_prt = Process(target=data_source, args=())

    p_dts.start()
    p_emb.start()
    p_prt.start()

    p_dts.join()
    p_emb.join()
    p_prt.join()

    exit()