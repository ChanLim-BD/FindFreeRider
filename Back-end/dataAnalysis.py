import pandas as pd
import re
import numpy as np


class DataAnalasis:

    # txt 파일 읽어오기
    # 첫 두 줄(필요없는 정보: 파일명, 저장한 날짜) 제거
    # \n(줄바꿈만 있는 라인) 제거

    def __init__(self, filename):
        self.filename = '.' + filename

    # 모든 실행코드는 runModule로 옮겨주세요

    def runModule(self):
        msg_list = self.read_msg()

        # 채팅만 남긴 list
        self.deleteUseless(msg_list)

        # 줄바꿈까지 처리한 list
        self.combineLinebreak(msg_list)

        # 데이터프레임 형태의 채팅 내역
        df = self.createDF(msg_list)

        member = list(df['name'].unique())

        lengthMean = self.calChatLength(member, df)

        df2 = self.analyzeChat(df, lengthMean)

        # 비율 계산

        percentList = []
        total = df2['score'].sum()

        for i in range(len(df2)):
            percent = df2.iloc[i, 6] / total
            percentList.append(percent)

        df2['percent'] = percentList

        # json 형식으로 변환
        js = df2.to_json(orient='index', force_ascii=False)

        return js



    def read_msg(self):
        with open(self.filename, encoding='utf-8') as f:
            chatMsg_list = f.readlines()
            del chatMsg_list[0:2]
            chatMsg_list = list(filter(lambda x: x != '\n', chatMsg_list))
        return chatMsg_list



    # 쓸데없는 라인 삭제
    # 초대했습니다 or 나갔습니다 있는 라인
    # 날짜 구분 라인

    def deleteUseless(self, chatlist):
        imsg = '님을 초대했습니다.'
        lmsg = '님이 나갔습니다.'
        division_line = []

        # 초대/퇴장 메시지 삭제
        for i in reversed(range(len(chatlist))):
            if imsg in chatlist[i] or lmsg in chatlist[i]:
                del chatlist[i]
            else:
                pass

        # 날짜 구분 삭제
        for msg in chatlist:
            dateline = re.match(r"(\d{4}. \d{1,2}. \d{1,2}).\s((\w요일)|((오후|오전)\s(\d{1,2}:\d{2}))\n)", msg)
            division_line.append(dateline)

        d_index = list(filter(lambda x: division_line[x] != None, range(len(division_line))))
        d_index.reverse()

        for i in d_index:
            del chatlist[i]



    def combineLinebreak(self, chatlist):
        # 1개의 채팅 내에 줄바꿈이 있는 경우 처리
        line_break = []

        for msg in chatlist:
            line = re.match(r"(\d{4}. \d{1,2}. \d{1,2}).\s(오후|오전)\s(\d{1,2}:\d{2})", msg)
            line_break.append(line)

        b_index = list(filter(lambda x: line_break[x] == None, range(len(line_break))))
        b_index.reverse()

        for i in b_index:
            chatlist[i - 1] = chatlist[i - 1] + chatlist[i]
            del chatlist[i]



    def createDF(self, chatlist):
        # 날짜, 이름, 채팅 내용 각각 리스트로 만들기

        date_list = []
        name = []
        content = []

        for msg in chatlist:
            contentFull = msg[:-1].split(',', 1)

            try:
                name_and_chat = contentFull[1].split(':', 1)
                date_list.append(contentFull[0])
                name.append(name_and_chat[0][1:-1])
                content.append(name_and_chat[1][1:])

            except:
                continue

        dataFrame = pd.DataFrame(data=date_list, columns=['date'])
        dataFrame['name'] = name
        dataFrame['message'] = content

        return dataFrame

    def calChatLength(self, memList, df):
        # 메시지 평균 길이 계산
        chatLen = []

        for i in range(len(memList)):
            chatBymem = list(df.loc[df['name'] == memList[i]]['message'])
            tmp = []
            for j in range(len(chatBymem)):
                tmp.append(len(chatBymem[j]))

            avg = np.mean(tmp)
            chatLen.append(avg)

        return chatLen

    # 여기서부터 분석
    def analyzeChat(self, dataframe, lengthMean):
        freq = dataframe.groupby(['name']).count()
        freq = freq.drop(['date'], axis=1)
        freq.rename(columns={'message': 'count'}, inplace=True)
        freq['Msg Length'] = lengthMean

        dataframe['Apology_count'] = dataframe['message'].apply(lambda x: 1 if '죄송' in x or '미안' in x else 0)
        dataframe['Fileshare_count'] = dataframe['message'].apply(lambda x: 1 if '파일: ' in x else 0)
        dataframe['AM_count'] = dataframe['date'].apply(lambda x: 1 if '오전' in x else 0)
        dataframe['PM_count'] = dataframe['date'].apply(lambda x: 1 if '오후' in x else 0)

        count_df = dataframe[['name', 'Apology_count', 'Fileshare_count', 'AM_count', 'PM_count']]
        count_df.set_index('name')

        freq_count = count_df.groupby(['name']).sum()

        contribution_df = pd.concat([freq, freq_count], axis=1)

        contribution_df['score'] = contribution_df.apply(lambda x: (
                    0.35 * x['count'] + 0.25 * x['Msg Length'] - 0.15 * x['Apology_count'] + 0.25 * x[
                'Fileshare_count']), axis=1)

        return contribution_df



