from sentence_transformers import SentenceTransformer
from multiprocessing import Process, Queue
import pytchat
import time


class chatsort:
    def __init__(self, chat_source, ):
        self.time_s = time.time()
        self.que_raw = Queue()
        self.que_emb = Queue()
        self.get_chat = self.get_chat_yt
        self.freq_print = 1.0
        self.model_ = 'sentence-transformers/all-distilroberta-v1'
        self.is_run = True

        self.opt_emb_t_l = 1.0
        self.opt_emb_s_b = 32
        pass

    def refine_message(self, mew_raw):
        mes_ref = mew_raw
        return mes_ref

    def get_chat_yt(self):
        i_pc = pytchat.create(video_id=video_id)
        while i_pc.is_alive():
            for each_chat in i_pc.get().sync_items():
                time_ = each_chat.datetime
                uid_ = each_chat.author.channelId
                mes_raw = each_chat.message
                mes_ref = self.refine_message(mes_raw)
                self.que_raw.put([time_, uid_, mes_raw, mes_ref])
        self.que_raw.put(-1)
        return

    def get_chat_tw(self):
        pass

    def get_chat_dm(self):
        pass

    def embed_message(self):
        st_ = SentenceTransformer(self.model_)
        is_run = True
        t_last_u = time.time()
        while is_run:
            if self.opt_emb_t_l <= (time.time() - t_last_u) \
                    or self.opt_emb_s_b <= self.que_raw.qsize():
                t_last_u = time.time()

                lst_time = []
                lst_uid = []
                lst_mes_raw = []
                lst_mes_ref = []

                for _ in range(self.opt_emb_s_b):
                    if self.que_raw.empty():
                        break
                    else:
                        temp_ = self.que_raw.get()
                        if temp_ == -1:
                            is_run = False
                        else:
                            time_, uid_, mes_raw, mes_ref = self.que_raw.get()
                            lst_time.append(time_)
                            lst_uid.append(uid_)
                            lst_mes_raw.append(mes_raw)
                            lst_mes_ref.append(mes_ref)
                lst_emb = st_.encode(lst_mes_ref)
                for time_, uid_, mes_raw, mes_ref, emb_ in zip(lst_time,lst_uid,lst_mes_raw,lst_mes_ref,lst_emb):
                    self.que_emb.put([time_, uid_, mes_raw, mes_ref, emb_])
            else:
                time.sleep(.1)
        self.que_emb.put(-1)
        return

    def print_(self):
        pass

    def run_(self):
        proc_gc = Process(target=self.get_chat)
        proc_ec = Process(target=self.embed_chat)

        proc_gc.start()
        while self.que_raw.empty(): time.sleep(.1)
        proc_ec.start()
        while self.que_emb.empty(): time.sleep(.1)

        is_run = True
        while is_run:


def data_source(video_id, que_origin):
    ist_pc = pytchat.create(video_id=video_id)
    while ist_pc.is_alive():
        for each_c in ist_pc.get().sync_items():
            d_time, d_uid, d_mes = each_c.datetime, each_c.author.channelId, each_c.message
            que_origin.put([d_time, d_uid, d_mes])
    que_origin.put([-1, 0, 0])
    return


def embedder(que_origin, que_embedded):
    model_ = SentenceTransformer()
    t_last_u = time.time()
    is_run = True
    while is_run:
        if 1.0 <= (time.time() - t_last_u) or 32 <= que_origin.qsize():
            t_last_u = time.time()
            lst_time = []
            lst_uid = []
            lst_mes_o = []
            for _ in range(32):
                if que_origin.empty():
                    break
                else:
                    s_time, s_uid, s_mes_o = que_origin.get()
                    if s_time == -1:
                        is_run = False
                        break
                    lst_time.append(s_time)
                    lst_uid.append(s_uid)
                    lst_mes_o.append(s_mes_o)
            t_s_sub = time.time()
            lst_mes_e = model_.encode(lst_mes_o, convert_to_numpy=True)
            print(len(lst_mes_e), time.time() - t_s_sub)

            for p_time, p_uid, p_mes_o, p_mes_e in zip(lst_time, lst_uid, lst_mes_o, lst_mes_e):
                que_embedded.put([p_time, p_uid, p_mes_o, p_mes_e])
        else:
            time.sleep(.1)
    que_embedded.put([-1, 0, 0, 0])
    return


def printer(que_embedded):
    t_last_u = time.time()
    is_run = True
    window_ = [0 for _ in range(10)]
    ptr_window = 0
    while is_run:
        if 1.0 <= (time.time() - t_last_u):
            t_last_u = time.time()
            print(window_)
        else:
            while not que_embedded.empty():
                c_time, c_uid, c_mes_o, c_mes_e = que_embedded.get()
                window_[ptr_window % 10] = c_mes_o[:3]
                ptr_window += 1
            time.sleep(.1)


if __name__ == "__main__":
    video_id = "Coo7CnC5c6E"

    que_origin = Queue()
    que_embedded = Queue()

    p_dts = Process(target=data_source, args=(video_id, que_origin))
    p_emb = Process(target=embedder, args=(que_origin, que_embedded))
    p_prt = Process(target=printer, args=(que_embedded,))

    p_dts.start()
    while que_origin.empty(): time.sleep(.25)
    p_emb.start()
    while que_embedded.empty(): time.sleep(.25)
    p_prt.start()

    p_dts.join()
    p_emb.join()
    p_prt.join()

    exit()
