from collections import deque
import heapq
import tkinter as tk
from PIL import ImageTk, Image
import pandas as pd
from tkinter import ttk
import tkinter.font
import json

# =====================[초성 리스트 및 추출 함수]=====================
CHOSUNG_LIST = ['ㄱ','ㄲ','ㄴ','ㄷ','ㄸ','ㄹ','ㅁ','ㅂ','ㅃ','ㅅ','ㅆ',
                'ㅇ','ㅈ','ㅉ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

def get_initials(word):
    initials = ""
    for char in word:
        if '가' <= char <= '힣':
            ch_code = ord(char) - ord('가')
            cho = ch_code // 588
            initials += CHOSUNG_LIST[cho]
        else:
            initials += char
    return initials

# =====================[노선 정보 불러오기]=====================
df = pd.read_excel("노선도좌표.xlsx")
stations = df[['호선', '역이름', 'x', 'y', '기타']].values
station_coords = {name: (int(x), int(y)) for _, name, x, y, _ in stations}
station_names = [name for _, name, _, _, _ in stations]

# =====================[노선 정보 - dictionary 구성 예시]=====================
landscape ={
      "신창": [
    {
      "station": "온양온천",
      "line": "1호선",
      "distance": 5.1
    }
  ],
  "온양온천" : [
    {
      "station":"배방",
      "line": "1호선",
      "distance": 4.9
    },
    {
      "station":"신창",
      "line": "1호선",
      "distance": 5.1
    }
],
  "배방": [
    {
      "station": "온양온천",
      "line": "1호선",
      "distance": 4.9
    },
    {
      "station": "탕정",
      "line": "1호선",
      "distance": 3.1
    }
  ],
  "탕정": [
    {
      "station": "배방",
      "line": "1호선",
      "distance": 3.1
    },
    {
      "station": "아산",
      "line": "1호선",
      "distance": 1.8
    }
  ],
  "아산": [
    {
      "station": "탕정",
      "line": "1호선",
      "distance": 1.8
    },
    {
      "station": "쌍용",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "쌍용": [
    {
      "station": "아산",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "봉명",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "봉명": [
    {
      "station": "쌍용",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "천안",
      "line": "1호선",
      "distance": 1.3
    }
  ],
  "천안": [
    {
      "station": "봉명",
      "line": "1호선",
      "distance": 1.3
    },
    {
      "station": "두정",
      "line": "1호선",
      "distance": 3.8
    }
  ],
  "두정": [
    {
      "station": "천안",
      "line": "1호선",
      "distance": 3.8
    },
    {
      "station": "직산",
      "line": "1호선",
      "distance": 3.8
    }
  ],
  "직산": [
    {
      "station": "두정",
      "line": "1호선",
      "distance": 3.8
    },
    {
      "station": "성환",
      "line": "1호선",
      "distance": 5.4
    }
  ],
  "성환": [
    {
      "station": "직산",
      "line": "1호선",
      "distance": 5.4
    },
    {
      "station": "평택",
      "line": "1호선",
      "distance": 9.4
    }
  ],
  "평택": [
    {
      "station": "성환",
      "line": "1호선",
      "distance": 9.4
    },
    {
      "station": "평택지제",
      "line": "1호선",
      "distance": 3.7
    }
  ],
  "평택지제": [
    {
      "station": "평택",
      "line": "1호선",
      "distance": 3.7
    },
    {
      "station": "서정리",
      "line": "1호선",
      "distance": 4.8
    }
  ],
  "서정리": [
    {
      "station": "평택지제",
      "line": "1호선",
      "distance": 4.8
    },
    {
      "station": "송탄",
      "line": "1호선",
      "distance": 2.2
    }
  ],
  "송탄": [
    {
      "station": "서정리",
      "line": "1호선",
      "distance": 2.2
    },
    {
      "station": "진위",
      "line": "1호선",
      "distance": 3.8
    }
  ],
  "진위": [
    {
      "station": "송탄",
      "line": "1호선",
      "distance": 3.8
    },
    {
      "station": "오산",
      "line": "1호선",
      "distance": 4
    }
  ],
  "오산": [
    {
      "station": "진위",
      "line": "1호선",
      "distance": 4
    },
    {
      "station": "오산대",
      "line": "1호선",
      "distance": 2.7
    }
  ],
  "오산대": [
    {
      "station": "오산",
      "line": "1호선",
      "distance": 2.7
    },
    {
      "station": "세마",
      "line": "1호선",
      "distance": 2.7
    }
  ],
  "세마": [
    {
      "station": "오산대",
      "line": "1호선",
      "distance": 2.7
    },
    {
      "station": "병점",
      "line": "1호선",
      "distance": 2.4
    }
  ],
  "병점": [
    {
      "station": "세마",
      "line": "1호선",
      "distance": 2.4
    },
    {
      "station": "세류",
      "line": "1호선",
      "distance": 4.3
    },
    {
      "station": "서동탄",
      "line": "1호선",
      "distance": 2.2
    }
  ],
  "서동탄": [
    {
      "station": "병점",
      "line": "1호선",
      "distance": 2.2
    }
  ],
  "세류": [
    {
      "station": "병점",
      "line": "1호선",
      "distance": 4.3
    },
    {
      "station": "수원",
      "line": "1호선",
      "distance": 2.9
    }

  ],
  "수원": [
    {
      "station": "세류",
      "line": "1호선",
      "distance": 2.9
    },
    {
      "station": "화서",
      "line": "1호선",
      "distance": 2.1
    }
  ],
  "화서": [
    {
      "station": "수원",
      "line": "1호선",
      "distance": 2.1
    },
    {
      "station": "성균관대",
      "line": "1호선",
      "distance": 2.6
    }
  ],
  "성균관대": [
    {
      "station": "화서",
      "line": "1호선",
      "distance": 2.6
    },
    {
      "station": "의왕",
      "line": "1호선",
      "distance": 2.9
    }
  ],
  "의왕": [
    {
      "station": "성균관대",
      "line": "1호선",
      "distance": 2.9
    },
    {
      "station": "당정",
      "line": "1호선",
      "distance": 2.6
    }
  ],
  "당정": [
    {
      "station": "의왕",
      "line": "1호선",
      "distance": 2.6
    },
    {
      "station": "군포",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "군포": [
    {
      "station": "당정",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "금정",
      "line": "1호선",
      "distance": 2.6
    }
  ],
  "금정": [
    {
      "station": "군포",
      "line": "1호선",
      "distance": 2.6
    },
    {
      "station": "명학",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "산본",
      "line": "4호선",
      "distance": 1.1
    },
    {
      "station": "범계",
      "line": "4호선",
      "distance": 2.3
    }
  ],
  "명학": [
    {
      "station": "금정",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "안양",
      "line": "1호선",
      "distance": 2.2
    }
  ],
  "안양": [
    {
      "station": "명학",
      "line": "1호선",
      "distance": 2.2
    },
    {
      "station": "관악",
      "line": "1호선",
      "distance": 2.4
    }
  ],
  "관악": [
    {
      "station": "안양",
      "line": "1호선",
      "distance": 2.4
    },
    {
      "station": "석수",
      "line": "1호선",
      "distance": 1.9
    }
  ],
  "석수": [
    {
      "station": "관악",
      "line": "1호선",
      "distance": 1.9
    },
    {
      "station": "금천구청",
      "line": "1호선",
      "distance": 1.9
    }
  ],
  "금천구청": [
    {
      "station": "석수",
      "line": "1호선",
      "distance": 1.9
    },
    {
      "station": "독산",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "광명",
      "line": "1호선",
      "distance": 4.8
    }
  ],
  "광명": [
    {
      "station": "금천구청",
      "line": "1호선",
      "distance": 4.8
    }
  ],
  "독산": [
    {
      "station": "금천구청",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "가산디지털단지",
      "line": "1호선",
      "distance": 2
    }
  ],
  "가산디지털단지": [
    {
      "station": "독산",
      "line": "1호선",
      "distance": 2
    },
    {
      "station": "구로",
      "line": "1호선",
      "distance": 2.4
    },
    {
      "station": "남구로",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "철산",
      "line": "7호선",
      "distance": 1.4
    }
  ],
  "구로": [
    {
      "station": "가산디지털단지",
      "line": "1호선",
      "distance": 2.4
    },
    {
      "station": "신도림",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "구일",
      "line": "1호선",
      "distance": 1
    }
  ],
  "신도림": [
    {
      "station": "구로",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "영등포",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "도림천",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "문래",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "대림",
      "line": "2호선",
      "distance": 1.8
    }
  ],
  "영등포": [
    {
      "station": "신도림",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "신길",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "신길": [
    {
      "station": "영등포",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "대방",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "영등포시장",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "여의도",
      "line": "5호선",
      "distance": 1
    }
  ],
  "대방": [
    {
      "station": "신길",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "노량진",
      "line": "1호선",
      "distance": 1.5
    }
  ],
  "노량진": [
    {
      "station": "대방",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "용산",
      "line": "1호선",
      "distance": 1.8
    }
  ],
  "용산": [
    {
      "station": "노량진",
      "line": "1호선",
      "distance": 1.8
    },
    {
      "station": "남영",
      "line": "1호선",
      "distance": 1.5
    }
  ],
  "남영": [
    {
      "station": "용산",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "서울역",
      "line": "1호선",
      "distance": 1.7
    }
  ],
  "서울역": [
    {
      "station": "남영",
      "line": "1호선",
      "distance": 1.7
    },
    {
      "station": "시청",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "회현",
      "line": "4호선",
      "distance": 0.9
    },
    {
      "station": "숙대입구",
      "line": "4호선",
      "distance": 1
    }
  ],
  "시청": [
    {
      "station": "서울역",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "종각",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "충정로",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "을지로입구",
      "line": "2호선",
      "distance": 0.7
    }
  ],
  "종각": [
    {
      "station": "시청",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "종로3가",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "종로5가": [
    {
      "station": "종로3가",
      "line": "1호선",
      "distance": 0.9
    },
    {
      "station": "동대문",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "동대문": [
    {
      "station": "종로5가",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "동묘앞",
      "line": "1호선",
      "distance": 0.6
    },
    {
      "station": "혜화",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "동대문역사문화공원",
      "line": "4호선",
      "distance": 0.7
    }
  ],
  "동묘앞": [
    {
      "station": "동대문",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "신설동",
      "line": "1호선",
      "distance": 0.7
    },
    {
      "station": "창신",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "신당",
      "line": "6호선",
      "distance": 0.6
    }
  ],
  "신설동": [
    {
      "station": "동묘앞",
      "line": "1호선",
      "distance": 0.7
    },
    {
      "station": "제기동",
      "line": "1호선",
      "distance": 0.9
    },
    {
      "station": "용두",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "제기동": [
    {
      "station": "신설동",
      "line": "1호선",
      "distance": 0.9
    },
    {
      "station": "청량리",
      "line": "1호선",
      "distance": 1
    }
  ],
  "청량리": [
    {
      "station": "제기동",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "회기",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "회기": [
    {
      "station": "청량리",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "외대앞",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "외대앞": [
    {
      "station": "회기",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "신이문",
      "line": "1호선",
      "distance": 0.8
    }
  ],
  "신이문": [
    {
      "station": "외대앞",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "석계",
      "line": "1호선",
      "distance": 1.4
    }
  ],
  "석계": [
    {
      "station": "신이문",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "광운대",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "돌곶이",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "태릉입구",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "광운대": [
    {
      "station": "석계",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "월계",
      "line": "1호선",
      "distance": 1.1
    }
  ],
  "월계": [
    {
      "station": "광운대",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "녹천",
      "line": "1호선",
      "distance": 1.4
    }
  ],
  "녹천": [
    {
      "station": "월계",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "창동",
      "line": "1호선",
      "distance": 1
    }
  ],
  "창동": [
    {
      "station": "녹천",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "방학",
      "line": "1호선",
      "distance": 1.7
    },
    {
      "station": "쌍문",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "노원",
      "line": "4호선",
      "distance": 1.4
    }
  ],
  "방학": [
    {
      "station": "창동",
      "line": "1호선",
      "distance": 1.7
    },
    {
      "station": "도봉",
      "line": "1호선",
      "distance": 1.3
    }
  ],
  "도봉": [
    {
      "station": "방학",
      "line": "1호선",
      "distance": 1.3
    },
    {
      "station": "도봉산",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "도봉산": [
    {
      "station": "도봉",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "망월사",
      "line": "1호선",
      "distance": 2.3
    },
    {
      "station": "장암",
      "line": "7호선",
      "distance": 1.4
    },
    {
      "station": "수락산",
      "line": "7호선",
      "distance": 1.6
    }
  ],
  "망월사": [
    {
      "station": "도봉산",
      "line": "1호선",
      "distance": 2.3
    },
    {
      "station": "회룡",
      "line": "1호선",
      "distance": 1.4
    }
  ],
  "회룡": [
    {
      "station": "망월사",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "의정부",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "의정부": [
    {
      "station": "회룡",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "가능",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "가능": [
    {
      "station": "의정부",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "녹양",
      "line": "1호선",
      "distance": 1.3
    }
  ],
  "녹양": [
    {
      "station": "가능",
      "line": "1호선",
      "distance": 1.3
    },
    {
      "station": "양주",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "양주": [
    {
      "station": "녹양",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "덕계",
      "line": "1호선",
      "distance": 5.3
    }
  ],
  "덕계": [
    {
      "station": "양주",
      "line": "1호선",
      "distance": 5.3
    },
    {
      "station": "덕정",
      "line": "1호선",
      "distance": 2.9
    }
  ],
  "덕정": [
    {
      "station": "덕계",
      "line": "1호선",
      "distance": 2.9
    },
    {
      "station": "지행",
      "line": "1호선",
      "distance": 5.6
    }
  ],
  "지행": [
    {
      "station": "덕정",
      "line": "1호선",
      "distance": 5.6
    },
    {
      "station": "동두천중앙",
      "line": "1호선",
      "distance": 1
    }
  ],
  "동두천중앙": [
    {
      "station": "지행",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "보산",
      "line": "1호선",
      "distance": 1.4
    }
  ],
  "보산": [
    {
      "station": "동두천중앙",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "동두천",
      "line": "1호선",
      "distance": 1.6
    }
  ],
  "동두천": [
    {
      "station": "보산",
      "line": "1호선",
      "distance": 1.6
    },
    {
      "station": "소요산",
      "line": "1호선",
      "distance": 2.5
    }
  ],
  "소요산": [
    {
      "station": "동두천",
      "line": "1호선",
      "distance": 2.5
    },
    {
      "station": "청산",
      "line": "1호선",
      "distance": 2.4
    }
  ],
  "청산": [
    {
      "station": "소요산",
      "line": "1호선",
      "distance": 2.4
    },
    {
      "station": "전곡",
      "line": "1호선",
      "distance": 3.3
    }
  ],
  "전곡": [
    {
      "station": "청산",
      "line": "1호선",
      "distance": 3.3
    },
    {
      "station": "연천",
      "line": "1호선",
      "distance": 8.7
    }
  ],
  "연천": [
    {
      "station": "전곡",
      "line": "1호선",
      "distance": 8.7
    }
  ],
  "구일": [
    {
      "station": "구로",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "개봉",
      "line": "1호선",
      "distance": 1.3
    }
  ],
  "개봉": [
    {
      "station": "구일",
      "line": "1호선",
      "distance": 1.3
    },
    {
      "station": "오류동",
      "line": "1호선",
      "distance": 1.9
    }
  ],
  "오류동": [
    {
      "station": "개봉",
      "line": "1호선",
      "distance": 1.9
    },
    {
      "station": "온수",
      "line": "1호선",
      "distance": 1.3
    }
  ],
  "온수": [
    {
      "station": "오류동",
      "line": "1호선",
      "distance": 1.3
    },
    {
      "station": "역곡",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "까치울",
      "line": "7호선",
      "distance": 2.2
    },
    {
      "station": "천왕",
      "line": "7호선",
      "distance": 1.5
    }
  ],
  "역곡": [
    {
      "station": "온수",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "소사",
      "line": "1호선",
      "distance": 1.1
    }
  ],
  "소사": [
    {
      "station": "역곡",
      "line": "1호선",
      "distance": 1.1
    },
    {
      "station": "부천",
      "line": "1호선",
      "distance": 1.7
    }
  ],
  "부천": [
    {
      "station": "소사",
      "line": "1호선",
      "distance": 1.7
    },
    {
      "station": "중동",
      "line": "1호선",
      "distance": 1
    }
  ],
  "중동": [
    {
      "station": "부천",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "송내",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "송내": [
    {
      "station": "중동",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "부개",
      "line": "1호선",
      "distance": 1.5
    }
  ],
  "부개": [
    {
      "station": "송내",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "부평",
      "line": "1호선",
      "distance": 1.7
    }
  ],
  "부평": [
    {
      "station": "부개",
      "line": "1호선",
      "distance": 1.7
    },
    {
      "station": "백운",
      "line": "1호선",
      "distance": 1.5
    }
  ],
  "백운": [
    {
      "station": "부평",
      "line": "1호선",
      "distance": 1.5
    },
    {
      "station": "동암",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "동암": [
    {
      "station": "백운",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "간석",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "간석": [
    {
      "station": "동암",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "주안",
      "line": "1호선",
      "distance": 1
    }
  ],
  "주안": [
    {
      "station": "간석",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "도화",
      "line": "1호선",
      "distance": 1
    }
  ],
  "도화": [
    {
      "station": "주안",
      "line": "1호선",
      "distance": 1
    },
    {
      "station": "제물포",
      "line": "1호선",
      "distance": 1.4
    }
  ],
  "제물포": [
    {
      "station": "도화",
      "line": "1호선",
      "distance": 1.4
    },
    {
      "station": "도원",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "도원": [
    {
      "station": "제물포",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "동인천",
      "line": "1호선",
      "distance": 1.2
    }
  ],
  "동인천": [
    {
      "station": "도원",
      "line": "1호선",
      "distance": 1.2
    },
    {
      "station": "인천",
      "line": "1호선",
      "distance": 1.9
    }
  ],
  "인천": [
    {
      "station": "동인천",
      "line": "1호선",
      "distance": 1.9
    }
  ],
  "을지로입구": [
    {
      "station": "시청",
      "line": "2호선",
      "distance": 0.7
    },
    {
      "station": "을지로3가",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "을지로3가": [
    {
      "station": "을지로입구",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "을지로4가",
      "line": "2호선",
      "distance": 0.6
    },
    {
      "station": "종로3가",
      "line": "3호선",
      "distance": 0.6
    },
    {
      "station": "충무로",
      "line": "3호선",
      "distance": 0.7
    }
  ],
  "을지로4가": [
    {
      "station": "을지로3가",
      "line": "2호선",
      "distance": 0.6
    },
    {
      "station": "동대문역사문화공원",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "동대문역사문화공원",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "종로3가",
      "line": "5호선",
      "distance": 1
    }
  ],
  "동대문역사문화공원": [
    {
      "station": "을지로4가",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "신당",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "동대문",
      "line": "4호선",
      "distance": 0.7
    },
    {
      "station": "충무로",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "을지로4가",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "청구",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "충청로":[
    {
      "station": "아현",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "시청",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "서대문",
      "line": "5호선",
      "distance": 0.7
    },
    {
      "station": "애오개",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "신당": [
    {
      "station": "동대문역사문화공원",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "상왕십리",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "동묘앞",
      "line": "6호선",
      "distance": 0.6
    },
    {
      "station": "청구",
      "line": "6호선",
      "distance": 0.7
    }
  ],
  "상왕십리": [
    {
      "station": "신당",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "왕십리",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "왕십리": [
    {
      "station": "상왕십리",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "한양대",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "행당",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "마장",
      "line": "5호선",
      "distance": 0.7
    }
  ],
  "한양대": [
    {
      "station": "왕십리",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "뚝섬",
      "line": "2호선",
      "distance": 1.1
    }
  ],
  "뚝섬": [
    {
      "station": "한양대",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "성수",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "성수": [
    {
      "station": "뚝섬",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "건대입구",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "용답",
      "line": "2호선",
      "distance": 2.3
    }
  ],
  "건대입구": [
    {
      "station": "성수",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "구의",
      "line": "2호선",
      "distance": 1.6
    },
    {
      "station": "어린이대공원",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "자양",
      "line": "7호선",
      "distance": 1
    }
  ],
  "구의": [
    {
      "station": "건대입구",
      "line": "2호선",
      "distance": 1.6
    },
    {
      "station": "강변",
      "line": "2호선",
      "distance": 0.9
    }
  ],
  "강변": [
    {
      "station": "구의",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "잠실나루",
      "line": "2호선",
      "distance": 1.8
    }
  ],
  "잠실나루": [
    {
      "station": "강변",
      "line": "2호선",
      "distance": 1.8
    },
    {
      "station": "잠실",
      "line": "2호선",
      "distance": 1
    }
  ],
  "잠실": [
    {
      "station": "잠실나루",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "잠실새내",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "몽촌토성",
      "line": "8호선",
      "distance": 0.8
    },
    {
      "station": "석촌",
      "line": "8호선",
      "distance": 1.2
    }
  ],
  "잠실새내": [
    {
      "station": "잠실",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "종합운동장",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "종합운동장": [
    {
      "station": "잠실새내",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "삼성",
      "line": "2호선",
      "distance": 1
    }
  ],
  "삼성": [
    {
      "station": "종합운동장",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "선릉",
      "line": "2호선",
      "distance": 1.3
    }
  ],
  "선릉": [
    {
      "station": "삼성",
      "line": "2호선",
      "distance": 1.3
    },
    {
      "station": "역삼",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "역삼": [
    {
      "station": "선릉",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "강남",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "강남": [
    {
      "station": "역삼",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "교대",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "교대": [
    {
      "station": "고속터미널",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "남부터미널",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "서초",
      "line": "2호선",
      "distance": 0.7
    },
    {
      "station": "강남",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "서초": [
    {
      "station": "교대",
      "line": "2호선",
      "distance": 0.7
    },
    {
      "station": "방배",
      "line": "2호선",
      "distance": 1.7
    }
  ],
  "방배": [
    {
      "station": "서초",
      "line": "2호선",
      "distance": 1.7
    },
    {
      "station": "사당",
      "line": "2호선",
      "distance": 1.6
    }
  ],
  "사당": [
    {
      "station": "방배",
      "line": "2호선",
      "distance": 1.6
    },
    {
      "station": "낙성대",
      "line": "2호선",
      "distance": 1.7
    },
    {
      "station": "이수",
      "line": "4호선",
      "distance": 1.1
    },
    {
      "station": "남태령",
      "line": "4호선",
      "distance": 1.6
    }
  ],
  "낙성대": [
    {
      "station": "사당",
      "line": "2호선",
      "distance": 1.7
    },
    {
      "station": "서울대입구",
      "line": "2호선",
      "distance": 1
    }
  ],
  "서울대입구": [
    {
      "station": "낙성대",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "봉천",
      "line": "2호선",
      "distance": 1
    }
  ],
  "봉천": [
    {
      "station": "서울대입구",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "신림",
      "line": "2호선",
      "distance": 1.1
    }
  ],
  "신림": [
    {
      "station": "봉천",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "신대방",
      "line": "2호선",
      "distance": 1.8
    }
  ],
  "신대방": [
    {
      "station": "신림",
      "line": "2호선",
      "distance": 1.8
    },
    {
      "station": "구로디지털단지",
      "line": "2호선",
      "distance": 1.1
    }
  ],
  "구로디지털단지": [
    {
      "station": "신대방",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "대림",
      "line": "2호선",
      "distance": 1.1
    }
  ],
  "대림": [
    {
      "station": "구로디지털단지",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "신도림",
      "line": "2호선",
      "distance": 1.8
    },
    {
      "station": "남구로",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "신풍",
      "line": "7호선",
      "distance": 1
    }
  ],
  "문래": [
    {
      "station": "신도림",
      "line": "2호선",
      "distance": 1.2
    },
    {
      "station": "영등포구청",
      "line": "2호선",
      "distance": 0.9
    }
  ],
  "영등포구청": [
    {
      "station": "문래",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "당산",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "양평",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "영등포시장",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "당산": [
    {
      "station": "영등포구청",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "합정",
      "line": "2호선",
      "distance": 2
    }
  ],
  "합정": [
    {
      "station": "당산",
      "line": "2호선",
      "distance": 2
    },
    {
      "station": "홍대입구",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "망원",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "상수",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "홍대입구": [
    {
      "station": "합정",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "신촌",
      "line": "2호선",
      "distance": 1.3
    }
  ],
  "신촌": [
    {
      "station": "홍대입구",
      "line": "2호선",
      "distance": 1.3
    },
    {
      "station": "이대",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "이대": [
    {
      "station": "신촌",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "아현",
      "line": "2호선",
      "distance": 0.9
    }
  ],
  "아현": [
    {
      "station": "이대",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "충정로",
      "line": "2호선",
      "distance": 0.8
    }
  ],
  "충정로": [
    {
      "station": "아현",
      "line": "2호선",
      "distance": 0.8
    },
    {
      "station": "시청",
      "line": "2호선",
      "distance": 1.1
    },
    {
      "station": "서대문",
      "line": "5호선",
      "distance": 0.7
    },
    {
      "station": "애오개",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "용답": [
    {
      "station": "성수",
      "line": "2호선",
      "distance": 2.3
    },
    {
      "station": "신답",
      "line": "2호선",
      "distance": 1
    }
  ],
  "신답": [
    {
      "station": "용답",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "용두",
      "line": "2호선",
      "distance": 0.9
    }
  ],
  "용두": [
    {
      "station": "신답",
      "line": "2호선",
      "distance": 0.9
    },
    {
      "station": "신설동",
      "line": "2호선",
      "distance": 1.2
    }
  ],
  "도림천": [
    {
      "station": "신도림",
      "line": "2호선",
      "distance": 1
    },
    {
      "station": "양천구청",
      "line": "2호선",
      "distance": 1.7
    }
  ],
  "양천구청": [
    {
      "station": "도림천",
      "line": "2호선",
      "distance": 1.7
    },
    {
      "station": "신정네거리",
      "line": "2호선",
      "distance": 1.9
    }
  ],
  "신정네거리": [
    {
      "station": "양천구청",
      "line": "2호선",
      "distance": 1.9
    },
    {
      "station": "까치산",
      "line": "2호선",
      "distance": 1.4
    }
  ],
  "까치산": [
    {
      "station": "신정네거리",
      "line": "2호선",
      "distance": 1.4
    },
    {
      "station": "화곡",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "신정",
      "line": "5호선",
      "distance": 1.3
    }
  ],
  "대화": [
    {
      "station": "주엽",
      "line": "3호선",
      "distance": 1.4
    }
  ],
  "주엽": [
    {
      "station": "대화",
      "line": "3호선",
      "distance": 1.4
    },
    {
      "station": "정발산",
      "line": "3호선",
      "distance": 1.6
    }
  ],
  "정발산": [
    {
      "station": "주엽",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "마두",
      "line": "3호선",
      "distance": 0.9
    }
  ],
  "마두": [
    {
      "station": "정발산",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "백석",
      "line": "3호선",
      "distance": 1.4
    }
  ],
  "백석": [
    {
      "station": "마두",
      "line": "3호선",
      "distance": 1.4
    },
    {
      "station": "대곡",
      "line": "3호선",
      "distance": 2.5
    }
  ],
  "대곡": [
    {
      "station": "백석",
      "line": "3호선",
      "distance": 2.5
    },
    {
      "station": "화정",
      "line": "3호선",
      "distance": 2.1
    }
  ],
  "화정": [
    {
      "station": "대곡",
      "line": "3호선",
      "distance": 2.1
    },
    {
      "station": "원당",
      "line": "3호선",
      "distance": 2.6
    }
  ],
  "원당": [
    {
      "station": "화정",
      "line": "3호선",
      "distance": 2.6
    },
    {
      "station": "원흥",
      "line": "3호선",
      "distance": 2.9
    }
  ],
  "원흥": [
    {
      "station": "원당",
      "line": "3호선",
      "distance": 2.9
    },
    {
      "station": "삼송",
      "line": "3호선",
      "distance": 2.1
    }
  ],
  "삼송": [
    {
      "station": "원흥",
      "line": "3호선",
      "distance": 2.1
    },
    {
      "station": "지축",
      "line": "3호선",
      "distance": 1.7
    }
  ],
  "지축": [
    {
      "station": "삼송",
      "line": "3호선",
      "distance": 1.7
    },
    {
      "station": "구파발",
      "line": "3호선",
      "distance": 1.5
    }
  ],
  "구파발": [
    {
      "station": "지축",
      "line": "3호선",
      "distance": 1.5
    },
    {
      "station": "연신내",
      "line": "3호선",
      "distance": 2
    }
  ],
  "연신내": [
    {
      "station": "구파발",
      "line": "3호선",
      "distance": 2
    },
    {
      "station": "불광",
      "line": "3호선",
      "distance": 1.3
    },
    {
      "station": "구산",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "불광": [
    {
      "station": "연신내",
      "line": "3호선",
      "distance": 1.3
    },
    {
      "station": "녹번",
      "line": "3호선",
      "distance": 1.1
    },
    {
      "station": "독바위",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "녹번": [
    {
      "station": "불광",
      "line": "3호선",
      "distance": 1.1
    },
    {
      "station": "홍제",
      "line": "3호선",
      "distance": 1.6
    }
  ],
  "홍제": [
    {
      "station": "녹번",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "무악재",
      "line": "3호선",
      "distance": 0.9
    }
  ],
  "무악재": [
    {
      "station": "홍제",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "독립문",
      "line": "3호선",
      "distance": 1.1
    }
  ],
  "독립문": [
    {
      "station": "무악재",
      "line": "3호선",
      "distance": 1.1
    },
    {
      "station": "경복궁",
      "line": "3호선",
      "distance": 1.6
    }
  ],
  "경복궁": [
    {
      "station": "독립문",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "안국",
      "line": "3호선",
      "distance": 1.1
    }
  ],
  "안국": [
    {
      "station": "경복궁",
      "line": "3호선",
      "distance": 1.1
    },
    {
      "station": "종로3가",
      "line": "3호선",
      "distance": 1
    }
  ],
  "종로3가": [
    {
      "station": "종각",
      "line": "1호선",
      "distance": 0.8
    },
    {
      "station": "종로5가",
      "line": "1호선",
      "distance": 0.9
    },
    {
      "station": "안국",
      "line": "3호선",
      "distance": 1
    },
    {
      "station": "을지로3가",
      "line": "3호선",
      "distance": 0.6
    },
    {
      "station": "광화문",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "을지로4가",
      "line": "5호선",
      "distance": 1
    }
  ],
  "충무로": [
    {
      "station": "을지로3가",
      "line": "3호선",
      "distance": 0.7
    },
    {
      "station": "동대입구",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "명동",
      "line": "4호선",
      "distance": 0.7
    },
    {
      "station": "동대문역사문화공원",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "동대입구": [
    {
      "station": "충무로",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "약수",
      "line": "3호선",
      "distance": 0.7
    }
  ],
  "약수": [
    {
      "station": "동대입구",
      "line": "3호선",
      "distance": 0.7
    },
    {
      "station": "금호",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "버티고개",
      "line": "6호선",
      "distance": 0.7
    },
    {
      "station": "청구",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "금호": [
    {
      "station": "약수",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "옥수",
      "line": "3호선",
      "distance": 0.8
    }
  ],
  "옥수": [
    {
      "station": "금호",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "압구정",
      "line": "3호선",
      "distance": 2.1
    }
  ],
  "압구정": [
    {
      "station": "옥수",
      "line": "3호선",
      "distance": 2.1
    },
    {
      "station": "신사",
      "line": "3호선",
      "distance": 1.5
    }
  ],
  "신사": [
    {
      "station": "압구정",
      "line": "3호선",
      "distance": 1.5
    },
    {
      "station": "잠원",
      "line": "3호선",
      "distance": 0.9
    }
  ],
  "잠원": [
    {
      "station": "신사",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "고속터미널",
      "line": "3호선",
      "distance": 1.2
    }
  ],
  "고속터미널": [
    {
      "station": "잠원",
      "line": "3호선",
      "distance": 1.2
    },
    {
      "station": "교대",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "반포",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "내방",
      "line": "7호선",
      "distance": 2.2
    }
  ],
  "남부터미널": [
    {
      "station": "교대",
      "line": "3호선",
      "distance": 1.6
    },
    {
      "station": "양재",
      "line": "3호선",
      "distance": 1.8
    }
  ],
  "양재": [
    {
      "station": "남부터미널",
      "line": "3호선",
      "distance": 1.8
    },
    {
      "station": "매봉",
      "line": "3호선",
      "distance": 1.2
    }
  ],
  "매봉": [
    {
      "station": "양재",
      "line": "3호선",
      "distance": 1.2
    },
    {
      "station": "도곡",
      "line": "3호선",
      "distance": 0.8
    }
  ],
  "도곡": [
    {
      "station": "매봉",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "대치",
      "line": "3호선",
      "distance": 0.8
    }
  ],
  "대치": [
    {
      "station": "도곡",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "학여울",
      "line": "3호선",
      "distance": 0.8
    }
  ],
  "학여울": [
    {
      "station": "대치",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "대청",
      "line": "3호선",
      "distance": 0.9
    }
  ],
  "대청": [
    {
      "station": "학여울",
      "line": "3호선",
      "distance": 0.9
    },
    {
      "station": "일원",
      "line": "3호선",
      "distance": 1.2
    }
  ],
  "일원": [
    {
      "station": "대청",
      "line": "3호선",
      "distance": 1.2
    },
    {
      "station": "수서",
      "line": "3호선",
      "distance": 1.8
    }
  ],
  "수서": [
    {
      "station": "일원",
      "line": "3호선",
      "distance": 1.8
    },
    {
      "station": "가락시장",
      "line": "3호선",
      "distance": 1.4
    }
  ],
  "가락시장": [
    {
      "station": "수서",
      "line": "3호선",
      "distance": 1.4
    },
    {
      "station": "경찰병원",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "송파",
      "line": "8호선",
      "distance": 0.8
    },
    {
      "station": "문정",
      "line": "8호선",
      "distance": 0.9
    }
  ],
  "경찰병원": [
    {
      "station": "가락시장",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "오금",
      "line": "3호선",
      "distance": 0.8
    }
  ],
  "오금": [
    {
      "station": "경찰병원",
      "line": "3호선",
      "distance": 0.8
    },
    {
      "station": "방이",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "개롱",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "오이도": [
    {
      "station": "정왕",
      "line": "4호선",
      "distance": 2.1
    }
  ],
  "정왕": [
    {
      "station": "오이도",
      "line": "4호선",
      "distance": 2.1
    },
    {
      "station": "신길온천",
      "line": "4호선",
      "distance": 1.4
    }
  ],
  "신길온천": [
    {
      "station": "정왕",
      "line": "4호선",
      "distance": 1.4
    },
    {
      "station": "안산",
      "line": "4호선",
      "distance": 2.9
    }
  ],
  "안산": [
    {
      "station": "신길온천",
      "line": "4호선",
      "distance": 2.9
    },
    {
      "station": "초지",
      "line": "4호선",
      "distance": 2.2
    }
  ],
  "초지": [
    {
      "station": "안산",
      "line": "4호선",
      "distance": 2.2
    },
    {
      "station": "고잔",
      "line": "4호선",
      "distance": 1.5
    }
  ],
  "고잔": [
    {
      "station": "초지",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "중앙",
      "line": "4호선",
      "distance": 1
    }
  ],
  "중앙": [
    {
      "station": "고잔",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "한대앞",
      "line": "4호선",
      "distance": 1.4
    }
  ],
  "한대앞": [
    {
      "station": "중앙",
      "line": "4호선",
      "distance": 1.4
    },
    {
      "station": "상록수",
      "line": "4호선",
      "distance": 7.2
    }
  ],
  "상록수": [
    {
      "station": "한대앞",
      "line": "4호선",
      "distance": 7.2
    },
    {
      "station": "반월",
      "line": "4호선",
      "distance": 1.5
    }
  ],
  "반월": [
    {
      "station": "상록수",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "대야미",
      "line": "4호선",
      "distance": 3.6
    }
  ],
  "대야미": [
    {
      "station": "반월",
      "line": "4호선",
      "distance": 3.6
    },
    {
      "station": "수리산",
      "line": "4호선",
      "distance": 2
    }
  ],
  "수리산": [
    {
      "station": "대야미",
      "line": "4호선",
      "distance": 2
    },
    {
      "station": "산본",
      "line": "4호선",
      "distance": 2.6
    }
  ],
  "산본": [
    {
      "station": "수리산",
      "line": "4호선",
      "distance": 2.6
    },
    {
      "station": "금정",
      "line": "4호선",
      "distance": 1.1
    }
  ],
  "범계": [
    {
      "station": "금정",
      "line": "4호선",
      "distance": 2.3
    },
    {
      "station": "평촌",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "평촌": [
    {
      "station": "범계",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "인덕원",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "인덕원": [
    {
      "station": "평촌",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "정부과천청사",
      "line": "4호선",
      "distance": 1.6
    }
  ],
  "정부과천청사": [
    {
      "station": "인덕원",
      "line": "4호선",
      "distance": 1.6
    },
    {
      "station": "과천",
      "line": "4호선",
      "distance": 1
    }
  ],
  "과천": [
    {
      "station": "정부과천청사",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "대공원",
      "line": "4호선",
      "distance": 1
    }
  ],
  "대공원": [
    {
      "station": "과천",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "경마공원",
      "line": "4호선",
      "distance": 0.9
    }
  ],
  "경마공원": [
    {
      "station": "대공원",
      "line": "4호선",
      "distance": 0.9
    },
    {
      "station": "선바위",
      "line": "4호선",
      "distance": 1
    }
  ],
  "선바위": [
    {
      "station": "경마공원",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "남태령",
      "line": "4호선",
      "distance": 1
    }
  ],
  "남태령": [
    {
      "station": "선바위",
      "line": "4호선",
      "distance": 2
    },
    {
      "station": "사당",
      "line": "4호선",
      "distance": 1.6
    }
  ],
  "이수": [
    {
      "station": "사당",
      "line": "4호선",
      "distance": 1.1
    },
    {
      "station": "동작",
      "line": "4호선",
      "distance": 1.8
    },
    {
      "station": "남성",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "내방",
      "line": "7호선",
      "distance": 1
    }
  ],
  "동작": [
    {
      "station": "이수",
      "line": "4호선",
      "distance": 1.8
    },
    {
      "station": "이촌",
      "line": "4호선",
      "distance": 2.7
    }
  ],
  "이촌": [
    {
      "station": "동작",
      "line": "4호선",
      "distance": 2.7
    },
    {
      "station": "신용산",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "신용산": [
    {
      "station": "이촌",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "삼각지",
      "line": "4호선",
      "distance": 0.7
    }
  ],
  "삼각지": [
    {
      "station": "신용산",
      "line": "4호선",
      "distance": 0.7
    },
    {
      "station": "숙대입구",
      "line": "4호선",
      "distance": 1.2
    },
    {
      "station": "효창공원앞",
      "line": "6호선",
      "distance": 1.2
    },
    {
      "station": "녹사평",
      "line": "6호선",
      "distance": 1.1
    }
  ],
  "숙대입구": [
    {
      "station": "삼각지",
      "line": "4호선",
      "distance": 1.2
    },
    {
      "station": "서울역",
      "line": "4호선",
      "distance": 1
    }
  ],
  "회현": [
    {
      "station": "서울역",
      "line": "4호선",
      "distance": 0.9
    },
    {
      "station": "명동",
      "line": "4호선",
      "distance": 0.7
    }
  ],
  "명동": [
    {
      "station": "회현",
      "line": "4호선",
      "distance": 0.7
    },
    {
      "station": "충무로",
      "line": "4호선",
      "distance": 0.7
    }
  ],
  "혜화": [
    {
      "station": "동대문",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "한성대입구",
      "line": "4호선",
      "distance": 0.9
    }
  ],
  "한성대입구": [
    {
      "station": "혜화",
      "line": "4호선",
      "distance": 0.9
    },
    {
      "station": "성신여대입구",
      "line": "4호선",
      "distance": 1
    }
  ],
  "성신여대입구": [
    {
      "station": "한성대입구",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "길음",
      "line": "4호선",
      "distance": 1.4
    }
  ],
  "길음": [
    {
      "station": "성신여대입구",
      "line": "4호선",
      "distance": 1.4
    },
    {
      "station": "미아사거리",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "미아사거리": [
    {
      "station": "길음",
      "line": "4호선",
      "distance": 1.3
    },
    {
      "station": "미아",
      "line": "4호선",
      "distance": 1.5
    }
  ],
  "미아": [
    {
      "station": "미아사거리",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "수유",
      "line": "4호선",
      "distance": 1.4
    }
  ],
  "수유": [
    {
      "station": "미아",
      "line": "4호선",
      "distance": 1.4
    },
    {
      "station": "쌍문",
      "line": "4호선",
      "distance": 1.5
    }
  ],
  "쌍문": [
    {
      "station": "수유",
      "line": "4호선",
      "distance": 1.5
    },
    {
      "station": "창동",
      "line": "4호선",
      "distance": 1.3
    }
  ],
  "노원": [
    {
      "station": "창동",
      "line": "4호선",
      "distance": 1.4
    },
    {
      "station": "상계",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "중계",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "마들",
      "line": "7호선",
      "distance": 1.2
    }
  ],
  "상계": [
    {
      "station": "노원",
      "line": "4호선",
      "distance": 1
    },
    {
      "station": "당고개",
      "line": "4호선",
      "distance": 1.2
    }
  ],
  "당고개": [
    {
      "station": "상계",
      "line": "4호선",
      "distance": 1.2
    },
    {
      "station": "별내별가람",
      "line": "4호선",
      "distance": 4.4
    }
  ],
  "별내별가람": [
    {
      "station": "당고개",
      "line": "4호선",
      "distance": 4.4
    },
    {
      "station": "오남",
      "line": "4호선",
      "distance": 4.4
    }
  ],
  "오남": [
    {
      "station": "별내별가람",
      "line": "4호선",
      "distance": 4.4
    },
    {
      "station": "진접",
      "line": "4호선",
      "distance": 2.1
    }
  ],
  "진접": [
    {
      "station": "오남",
      "line": "4호선",
      "distance": 2.1
    }
  ],
  "방화": [
    {
      "station": "개화산",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "개화산": [
    {
      "station": "방화",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "김포공항",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "김포공항": [
    {
      "station": "개화산",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "송정",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "송정": [
    {
      "station": "김포공항",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "마곡",
      "line": "5호선",
      "distance": 1.1
    }
  ],
  "마곡": [
    {
      "station": "송정",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "발산",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "발산": [
    {
      "station": "마곡",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "우장산",
      "line": "5호선",
      "distance": 1.1
    }
  ],
  "우장산": [
    {
      "station": "발산",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "화곡",
      "line": "5호선",
      "distance": 1
    }
  ],
  "화곡": [
    {
      "station": "우장산",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "까치산",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "신정": [
    {
      "station": "까치산",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "목동",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "목동": [
    {
      "station": "신정",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "오목교",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "오목교": [
    {
      "station": "목동",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "양평",
      "line": "5호선",
      "distance": 1
    }
  ],
  "양평": [
    {
      "station": "오목교",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "영등포구청",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "영등포시장": [
    {
      "station": "영등포구청",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "신길",
      "line": "5호선",
      "distance": 1
    }
  ],
  "여의도": [
    {
      "station": "신길",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "여의나루",
      "line": "5호선",
      "distance": 1
    }
  ],
  "여의나루": [
    {
      "station": "여의도",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "마포",
      "line": "5호선",
      "distance": 1.8
    }
  ],
  "마포": [
    {
      "station": "여의나루",
      "line": "5호선",
      "distance": 1.8
    },
    {
      "station": "공덕",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "공덕": [
    {
      "station": "마포",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "애오개",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "대흥",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "효창공원앞",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "애오개": [
    {
      "station": "공덕",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "충정로",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "서대문": [
    {
      "station": "충정로",
      "line": "5호선",
      "distance": 0.7
    },
    {
      "station": "광화문",
      "line": "5호선",
      "distance": 1.1
    }
  ],
  "광화문": [
    {
      "station": "서대문",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "종로3가",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "청구": [
    {
      "station": "동대문역사문화공원",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "신금호",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "신당",
      "line": "6호선",
      "distance": 0.7
    },
    {
      "station": "약수",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "신금호": [
    {
      "station": "청구",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "행당",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "행당": [
    {
      "station": "신금호",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "왕십리",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "마장": [
    {
      "station": "왕십리",
      "line": "5호선",
      "distance": 0.7
    },
    {
      "station": "답십리",
      "line": "5호선",
      "distance": 1
    }
  ],
  "답십리": [
    {
      "station": "마장",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "장한평",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "장한평": [
    {
      "station": "답십리",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "군자",
      "line": "5호선",
      "distance": 1.5
    }
  ],
  "군자": [
    {
      "station": "장한평",
      "line": "5호선",
      "distance": 1.5
    },
    {
      "station": "아차산",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "어린이대공원",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "중곡",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "아차산": [
    {
      "station": "군자",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "광나루",
      "line": "5호선",
      "distance": 1.5
    }
  ],
  "광나루": [
    {
      "station": "아차산",
      "line": "5호선",
      "distance": 1.5
    },
    {
      "station": "천호",
      "line": "5호선",
      "distance": 2
    }
  ],
  "천호": [
    {
      "station": "광나루",
      "line": "5호선",
      "distance": 2
    },
    {
      "station": "강동",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "강동구청",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "암사",
      "line": "8호선",
      "distance": 1.3
    }
  ],
  "강동": [
    {
      "station": "천호",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "길동",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "둔촌동",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "길동": [
    {
      "station": "강동",
      "line": "5호선",
      "distance": 1
    },
    {
      "station": "굽은다리",
      "line": "5호선",
      "distance": 1
    }
  ],
  "굽은다리": [
    {
      "station": "길동",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "명일",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "명일": [
    {
      "station": "굽은다리",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "고덕",
      "line": "5호선",
      "distance": 1.2
    }
  ],
  "고덕": [
    {
      "station": "명일",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "상일동",
      "line": "5호선",
      "distance": 1.1
    }
  ],
  "상일동": [
    {
      "station": "고덕",
      "line": "5호선",
      "distance": 1.1
    },
    {
      "station": "강일",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "강일": [
    {
      "station": "상일동",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "미사",
      "line": "5호선",
      "distance": 1.7
    }
  ],
  "미사": [
    {
      "station": "강일",
      "line": "5호선",
      "distance": 1.7
    },
    {
      "station": "하남풍산",
      "line": "5호선",
      "distance": 2.1
    }
  ],
  "하남풍산": [
    {
      "station": "미사",
      "line": "5호선",
      "distance": 2.1
    },
    {
      "station": "하남시청",
      "line": "5호선",
      "distance": 1.3
    }
  ],
  "하남시청": [
    {
      "station": "하남풍산",
      "line": "5호선",
      "distance": 1.3
    },
    {
      "station": "하남검단산",
      "line": "5호선",
      "distance": 1.6
    }
  ],
  "하남검단산": [
    {
      "station": "하남시청",
      "line": "5호선",
      "distance": 1.6
    }
  ],
  "둔촌동": [
    {
      "station": "강동",
      "line": "5호선",
      "distance": 1.2
    },
    {
      "station": "올림픽공원",
      "line": "5호선",
      "distance": 1.4
    }
  ],
  "올림픽공원": [
    {
      "station": "둔촌동",
      "line": "5호선",
      "distance": 1.4
    },
    {
      "station": "방이",
      "line": "5호선",
      "distance": 0.8
    }
  ],
  "방이": [
    {
      "station": "올림픽공원",
      "line": "5호선",
      "distance": 0.8
    },
    {
      "station": "오금",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "개롱": [
    {
      "station": "오금",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "거여",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "거여": [
    {
      "station": "개롱",
      "line": "5호선",
      "distance": 0.9
    },
    {
      "station": "마천",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "마천": [
    {
      "station": "거여",
      "line": "5호선",
      "distance": 0.9
    }
  ],
  "신내": [
    {
      "station": "봉화산",
      "line": "6호선",
      "distance": 1.3
    }
  ],
  "봉화산": [
    {
      "station": "신내",
      "line": "6호선",
      "distance": 1.3
    },
    {
      "station": "화랑대",
      "line": "6호선",
      "distance": 0.7
    }
  ],
  "화랑대": [
    {
      "station": "봉화산",
      "line": "6호선",
      "distance": 0.7
    },
    {
      "station": "태릉입구",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "태릉입구": [
    {
      "station": "화랑대",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "석계",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "공릉",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "먹골",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "돌곶이": [
    {
      "station": "석계",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "상월곡",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "상월곡": [
    {
      "station": "돌곶이",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "월곡",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "월곡": [
    {
      "station": "상월곡",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "고려대",
      "line": "6호선",
      "distance": 1.4
    }
  ],
  "고려대": [
    {
      "station": "월곡",
      "line": "6호선",
      "distance": 1.4
    },
    {
      "station": "안암",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "안암": [
    {
      "station": "고려대",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "보문",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "보문": [
    {
      "station": "안암",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "창신",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "창신": [
    {
      "station": "보문",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "동묘앞",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "버티고개": [
    {
      "station": "약수",
      "line": "6호선",
      "distance": 0.7
    },
    {
      "station": "한강진",
      "line": "6호선",
      "distance": 1
    }
  ],
  "한강진": [
    {
      "station": "버티고개",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "이태원",
      "line": "6호선",
      "distance": 1
    }
  ],
  "이태원": [
    {
      "station": "한강진",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "녹사평",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "녹사평": [
    {
      "station": "이태원",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "삼각지",
      "line": "6호선",
      "distance": 1.1
    }
  ],
  "효창공원앞": [
    {
      "station": "삼각지",
      "line": "6호선",
      "distance": 1.2
    },
    {
      "station": "공덕",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "대흥": [
    {
      "station": "공덕",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "광흥창",
      "line": "6호선",
      "distance": 1
    }
  ],
  "광흥창": [
    {
      "station": "대흥",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "상수",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "상수": [
    {
      "station": "광흥창",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "합정",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "망원": [
    {
      "station": "합정",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "마포구청",
      "line": "6호선",
      "distance": 1
    }
  ],
  "마포구청": [
    {
      "station": "망원",
      "line": "6호선",
      "distance": 1
    },
    {
      "station": "월드컵경기장",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "월드컵경기장": [
    {
      "station": "마포구청",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "디지털미디어시티",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "디지털미디어시티": [
    {
      "station": "월드컵경기장",
      "line": "6호선",
      "distance": 0.8
    },
    {
      "station": "증산",
      "line": "6호선",
      "distance": 1.1
    }
  ],
  "증산": [
    {
      "station": "디지털미디어시티",
      "line": "6호선",
      "distance": 1.1
    },
    {
      "station": "새절",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "새절": [
    {
      "station": "증산",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "응암",
      "line": "6호선",
      "distance": 0.9
    }
  ],
  "응암": [
    {
      "station": "새절",
      "line": "6호선",
      "distance": 0.9
    },
    {
      "station": "역촌",
      "line": "6호선",
      "distance": 1.1
    }
  ],
  "역촌": [
    {
      "station": "불광",
      "line": "6호선",
      "distance": 0.8
    }
  ],
  "독바위": [
    {
      "station": "연신내",
      "line": "6호선",
      "distance": 1.4
    }
  ],
  "구산": [
    {
      "station": "응암",
      "line": "6호선",
      "distance": 1.5
    }
  ],
  "석남": [
    {
      "station": "산곡",
      "line": "7호선",
      "distance": 2.6
    }
  ],
  "산곡": [
    {
      "station": "석남",
      "line": "7호선",
      "distance": 2.6
    },
    {
      "station": "부평구청",
      "line": "7호선",
      "distance": 1.6
    }
  ],
  "부평구청": [
    {
      "station": "산곡",
      "line": "7호선",
      "distance": 1.6
    },
    {
      "station": "굴포천",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "굴포천": [
    {
      "station": "부평구청",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "삼산체육관",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "삼산체육관": [
    {
      "station": "굴포천",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "상동",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "상동": [
    {
      "station": "삼산체육관",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "부천시청",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "부천시청": [
    {
      "station": "상동",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "신중동",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "신중동": [
    {
      "station": "부천시청",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "춘의",
      "line": "7호선",
      "distance": 1
    }
  ],
  "춘의": [
    {
      "station": "신중동",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "부천종합운동장",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "부천종합운동장": [
    {
      "station": "춘의",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "까치울",
      "line": "7호선",
      "distance": 1.2
    }
  ],
  "까치울": [
    {
      "station": "부천종합운동장",
      "line": "7호선",
      "distance": 1.2
    },
    {
      "station": "온수",
      "line": "7호선",
      "distance": 2.2
    }
  ],
  "천왕": [
    {
      "station": "온수",
      "line": "7호선",
      "distance": 1.5
    },
    {
      "station": "광명사거리",
      "line": "7호선",
      "distance": 1.7
    }
  ],
  "광명사거리": [
    {
      "station": "천왕",
      "line": "7호선",
      "distance": 1.7
    },
    {
      "station": "철산",
      "line": "7호선",
      "distance": 1.3
    }
  ],
  "철산": [
    {
      "station": "광명사거리",
      "line": "7호선",
      "distance": 1.3
    },
    {
      "station": "가산디지털단지",
      "line": "7호선",
      "distance": 1.4
    }
  ],
  "남구로": [
    {
      "station": "가산디지털단지",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "대림",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "신풍": [
    {
      "station": "대림",
      "line": "7호선",
      "distance": 1.4
    },
    {
      "station": "보라매",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "보라매": [
    {
      "station": "신풍",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "신대방삼거리",
      "line": "7호선",
      "distance": 0.8
    }
  ],
  "신대방삼거리": [
    {
      "station": "보라매",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "장승배기",
      "line": "7호선",
      "distance": 1.2
    }
  ],
  "장승배기": [
    {
      "station": "신대방삼거리",
      "line": "7호선",
      "distance": 1.2
    },
    {
      "station": "상도",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "상도": [
    {
      "station": "장승배기",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "숭실대입구",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "숭실대입구": [
    {
      "station": "상도",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "남성",
      "line": "7호선",
      "distance": 2
    }
  ],
  "남성": [
    {
      "station": "숭실대입구",
      "line": "7호선",
      "distance": 2
    },
    {
      "station": "이수",
      "line": "7호선",
      "distance": 1
    }
  ],
  "내방": [
    {
      "station": "이수",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "고속터미널",
      "line": "7호선",
      "distance": 2.2
    }
  ],
  "반포": [
    {
      "station": "고속터미널",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "논현",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "논현": [
    {
      "station": "반포",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "학동",
      "line": "7호선",
      "distance": 1
    }
  ],
  "학동": [
    {
      "station": "논현",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "강남구청",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "강남구청": [
    {
      "station": "학동",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "청담",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "청담": [
    {
      "station": "강남구청",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "자양",
      "line": "7호선",
      "distance": 2
    }
  ],
  "자양": [
    {
      "station": "청담",
      "line": "7호선",
      "distance": 2
    },
    {
      "station": "건대입구",
      "line": "7호선",
      "distance": 1
    }
  ],
  "어린이대공원": [
    {
      "station": "건대입구",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "군자",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "중곡": [
    {
      "station": "군자",
      "line": "7호선",
      "distance": 1.1
    },
    {
      "station": "용마산",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "용마산": [
    {
      "station": "중곡",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "사가정",
      "line": "7호선",
      "distance": 0.8
    }
  ],
  "사가정": [
    {
      "station": "용마산",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "면목",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "면목": [
    {
      "station": "사가정",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "상봉",
      "line": "7호선",
      "distance": 0.8
    }
  ],
  "상봉": [
    {
      "station": "면목",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "중화",
      "line": "7호선",
      "distance": 1
    }
  ],
  "중화": [
    {
      "station": "상봉",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "먹골",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "먹골": [
    {
      "station": "중화",
      "line": "7호선",
      "distance": 0.9
    },
    {
      "station": "태릉입구",
      "line": "7호선",
      "distance": 0.9
    }
  ],
  "공릉": [
    {
      "station": "태릉입구",
      "line": "7호선",
      "distance": 0.8
    },
    {
      "station": "하계",
      "line": "7호선",
      "distance": 1.3
    }
  ],
  "하계": [
    {
      "station": "공릉",
      "line": "7호선",
      "distance": 1.3
    },
    {
      "station": "중계",
      "line": "7호선",
      "distance": 1
    }
  ],
  "중계": [
    {
      "station": "하계",
      "line": "7호선",
      "distance": 1
    },
    {
      "station": "노원",
      "line": "7호선",
      "distance": 1.1
    }
  ],
  "마들": [
    {
      "station": "노원",
      "line": "7호선",
      "distance": 1.2
    },
    {
      "station": "수락산",
      "line": "7호선",
      "distance": 1.4
    }
  ],
  "수락산": [
    {
      "station": "마들",
      "line": "7호선",
      "distance": 1.4
    },
    {
      "station": "도봉산",
      "line": "7호선",
      "distance": 1.6
    }
  ],
  "장암": [
    {
      "station": "도봉산",
      "line": "7호선",
      "distance": 1.4
    }
  ],
  "별내": [
    {
      "station": "다산",
      "line": "8호선",
      "distance": 3
    }
  ],
  "다산": [
    {
      "station": "별내",
      "line": "8호선",
      "distance": 3
    },
    {
      "station": "동구릉",
      "line": "8호선",
      "distance": 1.8
    }
  ],
  "동구릉": [
    {
      "station": "다산",
      "line": "8호선",
      "distance": 1.8
    },
    {
      "station": "구리",
      "line": "8호선",
      "distance": 1.2
    }
  ],
  "구리": [
    {
      "station": "동구릉",
      "line": "8호선",
      "distance": 1.2
    },
    {
      "station": "장자호수공원",
      "line": "8호선",
      "distance": 1.8
    }
  ],
  "장자호수공원": [
    {
      "station": "구리",
      "line": "8호선",
      "distance": 1.8
    },
    {
      "station": "암사역사공원",
      "line": "8호선",
      "distance": 3.6
    }
  ],
  "암사역사공원": [
    {
      "station": "장자호수공원",
      "line": "8호선",
      "distance": 3.6
    },
    {
      "station": "암사",
      "line": "8호선",
      "distance": 1.1
    }
  ],
  "암사": [
    {
      "station": "암사역사공원",
      "line": "8호선",
      "distance": 1.1
    },
    {
      "station": "천호",
      "line": "8호선",
      "distance": 1.3
    }
  ],
  "강동구청": [
    {
      "station": "천호",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "몽촌토성",
      "line": "8호선",
      "distance": 1.6
    }
  ],
  "몽촌토성": [
    {
      "station": "강동구청",
      "line": "8호선",
      "distance": 1.6
    },
    {
      "station": "잠실",
      "line": "8호선",
      "distance": 0.8
    }
  ],
  "석촌": [
    {
      "station": "잠실",
      "line": "8호선",
      "distance": 1.2
    },
    {
      "station": "송파",
      "line": "8호선",
      "distance": 0.9
    }
  ],
  "송파": [
    {
      "station": "석촌",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "가락시장",
      "line": "8호선",
      "distance": 0.8
    }
  ],
  "문정": [
    {
      "station": "가락시장",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "장지",
      "line": "8호선",
      "distance": 0.9
    }
  ],
  "장지": [
    {
      "station": "문정",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "복정",
      "line": "8호선",
      "distance": 0.9
    }
  ],
  "복정": [
    {
      "station": "장지",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "남위례",
      "line": "8호선",
      "distance": 1.5
    }
  ],
  "남위례": [
    {
      "station": "복정",
      "line": "8호선",
      "distance": 1.5
    },
    {
      "station": "산성",
      "line": "8호선",
      "distance": 1.2
    }
  ],
  "산성": [
    {
      "station": "남위례",
      "line": "8호선",
      "distance": 1.2
    },
    {
      "station": "남한산성입구",
      "line": "8호선",
      "distance": 1.3
    }
  ],
  "남한산성입구": [
    {
      "station": "산성",
      "line": "8호선",
      "distance": 1.3
    },
    {
      "station": "단대오거리",
      "line": "8호선",
      "distance": 0.8
    }
  ],
  "단대오거리": [
    {
      "station": "남한산성입구",
      "line": "8호선",
      "distance": 0.8
    },
    {
      "station": "신흥",
      "line": "8호선",
      "distance": 0.8
    }
  ],
  "신흥": [
    {
      "station": "단대오거리",
      "line": "8호선",
      "distance": 0.8
    },
    {
      "station": "수진",
      "line": "8호선",
      "distance": 0.9
    }
  ],
  "수진": [
    {
      "station": "신흥",
      "line": "8호선",
      "distance": 0.9
    },
    {
      "station": "모란",
      "line": "8호선",
      "distance": 1
    }
  ],
  "모란": [
    {
      "station": "수진",
      "line": "8호선",
      "distance": 1
    }
  ]
}
# =====================[경로 알고리즘]=====================
def calculate_total_distance(route, landscape):
    total = 0
    for i in range(len(route) - 1):
        current = route[i]
        next_station = route[i + 1]
        connections = landscape.get(current, [])
        for conn in connections:
            if conn['station'] == next_station:
                total += conn['distance']
                break
    return total

def min_transfer(landscape, start, end):
    queue = deque([(start, None)])
    visited = set()
    routing = {(start, None): {"route": [start], "transfers": 0}}

    while queue:
        current_station, current_line = queue.popleft()
        visited.add((current_station, current_line))

        for near in landscape.get(current_station, []):
            next_station = near['station']
            next_line = near['line']
            if current_line is not None and current_line != next_line:
                continue
            state = (next_station, next_line)
            if state not in routing:
                routing[state] = {
                    "route": routing[(current_station, current_line)]['route'] + [next_station],
                    "transfers": routing[(current_station, current_line)]['transfers']
                }
                queue.append(state)

    results = [v for (station, _), v in routing.items() if station == end]
    if results:
        best = min(results, key=lambda x: x['transfers'])
        best['dist'] = len(best['route']) - 1
        best['stations'] = len(best['route'])
        return best
    else:
        return None

def min_distance(landscape, start, end):
    heap = []
    heapq.heappush(heap, (0, 0, start, None, [start]))
    visited = dict()

    while heap:
        dist, transfers, station, line, path = heapq.heappop(heap)
        if (station, line) in visited and visited[(station, line)] <= transfers:
            continue
        visited[(station, line)] = transfers

        if station == end:
            return {
                "dist": dist,
                "transfers": transfers,
                "stations": len(path),
                "route": path
            }

        for near in landscape.get(station, []):
            next_station = near['station']
            next_line = near['line']
            distance = near['distance']
            new_transfers = transfers + (0 if line is None or line == next_line else 1)

            heapq.heappush(heap, (
                dist + distance,
                new_transfers,
                next_station,
                next_line,
                path + [next_station]
            ))

    return None

def print_path_with_lines(route, landscape):
    result = []
    prev_line = None
    current_segment = []

    for i in range(len(route) - 1):
        current = route[i]
        next_station = route[i + 1]
        connections = [conn for conn in landscape[current] if conn['station'] == next_station]
        if not connections:
            continue
        connection = next((conn for conn in connections if conn['line'] == prev_line), connections[0])
        line = connection['line']
        if prev_line is not None and line != prev_line:
            current_segment.append(current)
            result.append(f"[{prev_line}]\n {' → '.join(current_segment)}")
            current_segment = []
        current_segment.append(current)
        prev_line = line

    current_segment.append(route[-1])
    result.append(f"[{prev_line}]\n {' → '.join(current_segment)}")
    return "\n".join(result)

# =====================[GUI 설정]=====================
win = tk.Tk()
win.geometry("1900x1000")
win.resizable(False, False)
win.config(bg="white")
win.title("지하철 노선도")

bg_img = Image.open("전체노선도.png").resize((1500, 1000))
bg_photo = ImageTk.PhotoImage(bg_img)

canvas = tk.Canvas(win, width=1500, height=1000)
canvas.place(x=400, y=0)
canvas.create_image(0, 0, image=bg_photo, anchor=tk.NW)
    
menubar=tk.Menu(win)
menu1=tk.Menu(menubar,tearoff=False)
menu1.add_command(label="종료", command=win.quit)
menubar.add_cascade(label="메뉴",menu=menu1)
win.config(menu=menubar)

start_station = None
destination_station = None
marker_items = []

def draw_marker(x, y, color):
    r = 7
    marker = canvas.create_oval(x - r, y - r, x + r, y + r, fill=color, outline='black', width=2)
    marker_items.append(marker)

def clear_markers():
    for item in marker_items:
        canvas.delete(item)
    marker_items.clear()

def update_markers():
    clear_markers()
    if start_station in station_coords:
        x, y = station_coords[start_station]
        draw_marker(x, y, 'red')
    if destination_station in station_coords:
        x, y = station_coords[destination_station]
        draw_marker(x, y, 'blue')

def draw_route_markers(route):
       for station in route[1:-1]:
        if station in station_coords:
            x, y = station_coords[station]
            draw_marker(x, y, 'green')

def select_station(name):
    global start_station, destination_station
    if start_station is None or (start_station and destination_station):
        start_station = name
        destination_station = None
        print(f'출발역 선택: {start_station}')
    elif destination_station is None and name != start_station:
        destination_station = name
        print(f'도착역 선택: {destination_station}')
        run_pathfinding()
    update_markers()
    update_entries()

def search_station(entry, is_start=True):
    global start_station, destination_station
    name = entry.get().strip()
    if name in station_coords:
        if is_start:
            start_station = name
            result_label.config(text=f"출발역 설정: {name}", fg="green")
        else:
            destination_station = name
            result_label.config(text=f"도착역 설정: {name}", fg="blue")
        update_markers()
        if start_station and destination_station:
            run_pathfinding()
    else:
        result_label.config(text=f"'{name}' 역을 찾을 수 없습니다.", fg="red")

def update_entries():
    start_entry.delete(0, tk.END)
    if start_station:
        start_entry.insert(0, start_station)
    dest_entry.delete(0, tk.END)
    if destination_station:
        dest_entry.insert(0, destination_station)

def run_pathfinding():
    bfs_result = min_transfer(landscape, start_station, destination_station)
    dijkstra_result = min_distance(landscape, start_station, destination_station)

    print(f"\n---------------------[ {start_station} --> {destination_station} ]-----------------")

    route_to_draw = None
    bfs_text = ""
    dijkstra_text = ""

    if bfs_result and dijkstra_result:
        if bfs_result['route'] != dijkstra_result['route']:
            # 최소 환승 경로
            bfs_text += "[최소 환승 경로]\n"
            bfs_text += print_path_with_lines(bfs_result['route'], landscape) + "\n"
            bfs_text += f"총 거리: {int(calculate_total_distance(bfs_result['route'], landscape))} km\n"
            bfs_text += f"역 개수: {bfs_result['stations']}\n"
            bfs_text += f"환승 수: {bfs_result['transfers']}"

            # 최단 거리 경로
            dijkstra_text += "[최단 거리 경로]\n"
            dijkstra_text += print_path_with_lines(dijkstra_result['route'], landscape) + "\n"
            dijkstra_text += f"총 거리: {int(dijkstra_result['dist'])} km\n"
            dijkstra_text += f"역 개수: {dijkstra_result['stations']}\n"
            dijkstra_text += f"환승 수: {dijkstra_result['transfers']}"

            route_to_draw = dijkstra_result['route']
        else:
            # 동일한 경우 하나만 출력
            bfs_text += "[최소 환승 및 최단 거리 경로]\n"
            bfs_text += print_path_with_lines(bfs_result['route'], landscape) + "\n"
            bfs_text += f"총 거리: {int(calculate_total_distance(bfs_result['route'], landscape))} km\n"
            bfs_text += f"역 개수: {bfs_result['stations']}\n"
            bfs_text += f"환승 수: {bfs_result['transfers']}"

            route_to_draw = bfs_result['route']
            dijkstra_text = bfs_text
    elif bfs_result:
        bfs_text += "[최소 환승 경로]\n"
        bfs_text += print_path_with_lines(bfs_result['route'], landscape) + "\n"
        bfs_text += f"총 거리: {int(calculate_total_distance(bfs_result['route'], landscape))} km\n"
        bfs_text += f"역 개수: {bfs_result['stations']}\n"
        bfs_text += f"환승 수: {bfs_result['transfers']}"

        route_to_draw = bfs_result['route']
    elif dijkstra_result:
        dijkstra_text += "[최단 거리 경로]\n"
        dijkstra_text += print_path_with_lines(dijkstra_result['route'], landscape) + "\n"
        dijkstra_text += f"총 거리: {int(dijkstra_result['dist'])} km\n"
        dijkstra_text += f"역 개수: {dijkstra_result['stations']}\n"
        dijkstra_text += f"환승 수: {dijkstra_result['transfers']}"

        route_to_draw = dijkstra_result['route']
    else:
        bfs_text = "경로를 찾을 수 없습니다."
        dijkstra_text = "경로를 찾을 수 없습니다."

    # 결과를 라벨에 업데이트
    min_transfer_label.config(text=bfs_text)
    min_distance_label.config(text=dijkstra_text)

    # 경로 마커 표시
    if route_to_draw:
        update_markers()
        draw_route_markers(route_to_draw)
        
#=======================역 정보=============================
close_img = Image.open("닫기.png")
close_img = close_img.resize((30, 30))
close_img_tk = ImageTk.PhotoImage(close_img)

image_label = tkinter.Label(win)
image_label.place(x=400, y=0)
close_button = tkinter.Button(win, image=close_img_tk, command=lambda: hide_table(), borderwidth=0)
close_button.image = close_img_tk 

storage_df = pd.read_excel("수도권_물품보관소.xlsx")
restroom_df = pd.read_excel("수도권_화장실.xlsx")
tree = ttk.Treeview(win,height=32)

info_win = True
style = ttk.Style(win)
style.configure('Treeview',font=('맑은고딕',14))
def station_info(name):
    global info_win
    if info_win == False:
        hide_table()
    json_file = "KTX_SRT_시간표.json" 
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if name in data:
            KTX_SRT_timelist(data[name],name)
    img_path = f"지하철역/{name}.png" 
    img = Image.open(img_path)
    station_image = ImageTk.PhotoImage(img)
    image_label.config(image=station_image)
    image_label.image = station_image 
    image_label.place(x=400, y=132)
    image_label.lift()
    
    close_button.place(x=400, y=100)
    close_button.lift()
    
    station_storage_detail= storage_df['상세위치'].to_numpy()
    station_name_label.config(text=name)
    station_storage = list(storage_df['역'].to_numpy())
    if name in station_storage:
        idx = station_storage.index(name)
        storage_detile_label.config(text=station_storage_detail[idx])
    else :
        storage_detile_label.config(text="없음")
    station_restroom_detail= restroom_df['상세위치'].to_numpy()
    station_restroom = list(restroom_df['역'].to_numpy())
    if name in station_restroom:
        idx = station_restroom.index(name)
        restroom_detile_label.config(text=station_restroom_detail[idx])
    else:
        restroom_detile_label.config(text="없음")
    if info_win:
        info_frame.place(x=400,y=396)
        info_win = False
        
def KTX_SRT_timelist(values,name):
    global tree
    global info_win
    tree = ttk.Treeview(win,height=32)
    tree['columns']=("one")
    tree.heading("#0", text=name)
    tree.heading("#1", text="시간표")
    tree.column("#0", width=80,anchor='center')
    tree.column("#1", width=80,anchor='center')
    num = 1
    for train_type in values:
        if train_type == "KTX":
            tree.insert("","end", text="KTX")
            for line in values['KTX']:
                tree.insert("","end", values=line)
                tree.insert("",'end',iid=num,text='시간표')
                for j in values['KTX'][line]['출발시간']:
                    tree.insert(num,'end',values=j)
                num+=1
        if train_type == "SRT":
            tree.insert("","end", text="SRT")
            for line in values['SRT']:
                tree.insert("","end", values=line)
                tree.insert("",'end',iid=num,text='시간표')
                for j in values['SRT'][line]['출발시간']:
                    tree.insert(num,'end',values=j)
                num+=1
    if info_win:
        tree.place(x=1120,y=396)

def hide_table():
    global tree
    global info_win
    info_win = True
    tree.place_forget()
    close_button.place_forget()
    info_frame.place_forget()
    image_label.place_forget()

info_font = tkinter.font.Font(family='맑은고딕',size=30)
detail_font = tkinter.font.Font(family='맑은고딕',size=25)
info_frame = tkinter.Frame(win,bg='white',width=300,relief="flat")

station_name_label = tkinter.Label(info_frame,font=info_font,width=32,bg='white')
storage_room_label = tkinter.Label(info_frame,text="물품보관소",font=info_font,width=16,bg='white')
storage_detile_label = tkinter.Label(info_frame,font=detail_font,width=16,wraplength='270',bg='white')
restroom_label = tkinter.Label(info_frame,text="화장실",font=info_font,width=16,bg='white')
restroom_detile_label = tkinter.Label(info_frame,font=detail_font,width=16,wraplength='270',bg='white')
# storage_label = tkinter.Label(info_frame,font=info_font,width=16,height=100,bg='white')
# restroom_bin_label = tkinter.Label(info_frame,font=info_font,width=16,height=100,bg='white')

station_name_label.grid(row=0,column=0,columnspan=4,sticky='ew')
storage_room_label.grid(row=1,column=0,columnspan=2,sticky='ew')
restroom_label.grid(row=1,column=2,columnspan=2,sticky='ew')
storage_detile_label.grid(row=2,column=0,columnspan=2,sticky='ew')
restroom_detile_label.grid(row=2,column=2,columnspan=2,sticky='ew')
# storage_label.grid(row=3,column=0,columnspan=2)
# restroom_bin_label.grid(row=3,column=2,columnspan=2)

# =====================[자동완성 함수]=====================
def create_autocomplete(entry, is_start=True):
    listbox = tk.Listbox(win, height=5, font=("Segoe UI", 14))
    listbox.place_forget()
    listbox_is_visible = [False]

    def update_autocomplete(event=None):
        typed = entry.get().strip()
        listbox.delete(0, tk.END)
        if typed == "":
            listbox.place_forget()
            listbox_is_visible[0] = False
            return
        typed_initials = get_initials(typed)
        matches = [name for name in station_names if typed in name or typed_initials in get_initials(name)]
        if matches:
            for name in matches:
                listbox.insert(tk.END, name)
            listbox.place(x=entry.winfo_rootx() - win.winfo_rootx(),
                          y=entry.winfo_rooty() - win.winfo_rooty() + entry.winfo_height(),
                          width=entry.winfo_width())
            listbox.select_set(0)
            listbox.activate(0)
            listbox_is_visible[0] = True
        else:
            listbox.place_forget()
            listbox_is_visible[0] = False

    def select_from_list(event=None):
        if listbox_is_visible[0]:
            selection = listbox.curselection()
            if selection:
                chosen = listbox.get(selection[0])
                entry.delete(0, tk.END)
                entry.insert(0, chosen)
                listbox.place_forget()
                listbox_is_visible[0] = False
                search_station(entry, is_start)

    def move_up(event):
        if listbox_is_visible[0] and listbox.size() > 0:
            index = listbox.curselection()
            if index:
                new_index = max(0, index[0] - 1)
                listbox.select_clear(0, tk.END)
                listbox.select_set(new_index)
                listbox.activate(new_index)
            return "break"

    def move_down(event):
        if listbox_is_visible[0] and listbox.size() > 0:
            index = listbox.curselection()
            if index:
                new_index = min(listbox.size() - 1, index[0] + 1)
                listbox.select_clear(0, tk.END)
                listbox.select_set(new_index)
                listbox.activate(new_index)
            return "break"

    def close_listbox(event=None):
        listbox.place_forget()
        listbox_is_visible[0] = False

    entry.bind("<KeyRelease>", update_autocomplete)
    entry.bind("<Return>", select_from_list)
    entry.bind("<Up>", move_up)
    entry.bind("<Down>", move_down)
    entry.bind("<Escape>", close_listbox)
    listbox.bind("<Double-Button-1>", select_from_list)
    listbox.bind("<Return>", select_from_list)

# =====================[역 마커 생성 및 클릭 이벤트]=====================
r = 5
for _, name, x, y, _ in stations:
    x = int(x)
    y = int(y)
    canvas.create_oval(x - r, y - r, x + r, y + r, fill='white', outline='black', width=2, tags=name)
    canvas.tag_bind(name, "<Button-1>", lambda event, n=name: select_station(n))

# =====================[검색 UI 구성 - 통합 검색 버튼]=====================
search_frame = tk.Frame(win, bg="white")
search_frame.place(x=20, y=20)

tk.Label(search_frame, text="출발역:", bg="white", font=("Segoe UI", 14)).grid(row=0, column=0, sticky='e', padx=5, pady=10)
start_entry = tk.Entry(search_frame, width=20, font=("Segoe UI", 14), bd=1, relief="solid")
start_entry.grid(row=0, column=1, padx=5)

tk.Label(search_frame, text="도착역:", bg="white", font=("Segoe UI", 14)).grid(row=1, column=0, sticky='e', padx=5, pady=10)
dest_entry = tk.Entry(search_frame, width=20, font=("Segoe UI", 14), bd=1, relief="solid")
dest_entry.grid(row=1, column=1, padx=5)

# 통합 검색 함수 정의
def unified_search():
    global start_station, destination_station
    start_input = start_entry.get().strip()
    dest_input = dest_entry.get().strip()

    if start_input not in station_coords:
        result_label.config(text=f"출발역 '{start_input}'을(를) 찾을 수 없습니다.", fg="red")
        return
    if dest_input not in station_coords:
        result_label.config(text=f"도착역 '{dest_input}'을(를) 찾을 수 없습니다.", fg="red")
        return

    start_station = start_input
    destination_station = dest_input
    result_label.config(text=f"{start_station} → {destination_station} 경로 검색", fg="black")

    update_markers()
    run_pathfinding()
    
    st_button.config(text=start_input,command=lambda:station_info(start_input))
    ed_button.config(text=dest_input,command=lambda:station_info(dest_input))
    
    if start_station and destination_station:       
        button_frame.place(x=20, y=900)

tk.Button(search_frame, text="검색", command=unified_search, font=("Segoe UI", 14), height=3).grid(row=0, column=2, rowspan=2, padx=10, pady=5, sticky='ns')

result_label = tk.Label(win, text="", font=("Segoe UI", 15), bg="white")
result_label.place(x=20, y=130)

create_autocomplete(start_entry, True)
create_autocomplete(dest_entry, False)

# =====================[아코디언 UI 구성 - 최소환승 / 최단거리 경로]=====================
accordion_frame = tk.Frame(win, bg="white")
accordion_frame.place(x=20, y=180, width=360)

def toggle_frame(frame, button, title):
    if frame.winfo_ismapped():
        frame.pack_forget()
        button.config(text=f"▶ {title}")
    else:
        frame.pack(fill="x")
        button.config(text=f"▼ {title}")

# ▶ 첫 번째 아코디언: 최소 환승 경로
accordion1_container = tk.Frame(accordion_frame, bg="white")
accordion1_container.pack(fill="x", pady=(0, 10))

accordion1_btn = tk.Button(
    accordion1_container,
    text="▶ 최소 환승 경로",
    font=("Segoe UI", 13),
    anchor="w",
    relief="flat",
    bg="white",         # <-- 버튼 배경색 설정
    activebackground="white",
    command=lambda: toggle_frame(accordion1_content, accordion1_btn, "최소 환승 경로")
)
accordion1_btn.pack(fill="x")

accordion1_content = tk.Frame(accordion1_container, bg="#f8f8f8", bd=1, relief="solid")
tk.Label(accordion1_content)

# ▶ 두 번째 아코디언: 최단 거리 경로
accordion2_container = tk.Frame(accordion_frame, bg="white")
accordion2_container.pack(fill="x")

accordion2_btn = tk.Button(
    accordion2_container,
    text="▶ 최단 거리 경로",
    font=("Segoe UI", 13),
    anchor="w",
    relief="flat",
    bg="white",         # <-- 버튼 배경색 설정
    activebackground="white",
    command=lambda: toggle_frame(accordion2_content, accordion2_btn, "최단 거리 경로")
)
accordion2_btn.pack(fill="x")

accordion2_content = tk.Frame(accordion2_container, bg="#f8f8f8", bd=1, relief="solid")
tk.Label(accordion2_content)

# 결과 출력용 라벨 (경로 표시)
min_transfer_label = tk.Label(accordion1_content, text="", bg="#f8f8f8", justify="left", font=("Segoe UI", 11), anchor="w", wraplength=330)
min_transfer_label.pack(anchor="w", padx=10, pady=(0, 10))

min_distance_label = tk.Label(accordion2_content, text="", bg="#f8f8f8", justify="left", font=("Segoe UI", 11), anchor="w", wraplength=330)
min_distance_label.pack(anchor="w", padx=10, pady=(0, 10))

# =====================[UI-역 정보 버튼]=====================
    
button_frame = tk.Frame(win, bg="white")
st_button = tk.Button(button_frame, font=("Segoe UI", 14))
ed_button = tk.Button(button_frame, font=("Segoe UI", 14))
st_button.grid(row=0, column=0, padx=10, pady=10)
ed_button.grid(row=0, column=1, padx=10, pady=10)
    
# =====================[GUI 실행]=====================
win.mainloop()