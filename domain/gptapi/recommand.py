from openai import OpenAI
from config import settings
from database import get_db
from sqlalchemy import desc
from models import *

API_KEY = settings.GPT_API_KEY

client = OpenAI(api_key=API_KEY)

class GptAPI():
    def __init__(self, model, client):
        self.messages = []
        self.model = model
        self.client = client
    
    def get_message(self, prompt):
        self.messages.append({"role": "user", "content": prompt})

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
        )

        result = ''
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                string = chunk.choices[0].delta.content
                # print(string, end="")
                result = ''.join([result, string])

        # return self.messages.append({"role": "system", "content": result})
        return result

def start_recommand_job(data):
    db = get_db
    model = "gpt-4o-mini"

    job_list = ["건물 청소원(공공건물,아파트,사무실,병원,상가,공장 등)",
                "기타 보건·의료 서비스 종사원",
                "사무 보조원(일반사업체)",
                "사업체 구내식당 급식 조리사",
                "사회복지사",
                "상담 전문가",
                "웹 디자이너",
                "재가 요양보호사"]
    

    text = f"{data}\n"
    text += "위에는 취업을 원하는 장애인에 대한 데이터야. 이 사람에게 맞는 직무 3개를 아래 리스트 값들 중에서 추천해줘.\n"
    text += f"{job_list}"
    text += "결과는 리스트만 반환해줘."

    # 답변 요청
    gpt = GptAPI(model, client)
    msg = gpt.get_message(text)
    result_msg = msg[1:-1].replace("'", "").split(", ")
    # print(result_msg)
    return result_msg


def recommand_cover_letter(type, user, answer):
    question_list = [
        {
            "1": "드림님은 앞으로 어떤 일을 하고 싶으세요?",
            "2": "혹시 그 일에 대한 경험이 있으신가요? 경험이 있다면 저에게 자세히 말씀해주세요.",
            "3": "그 일을 하면서 나중에는 어떤 사람이 되고 싶으세요?",
            "4": "혹시 그것을 위해 드림님이 가지고 계신 계획이 있나요?",
            "5": "그렇다면 드림님이 일에 대해 가장 중요하게 생각하는 것은 무엇인가요?"
        },
        {
            "1": "저에게 드림님의 장애에 대해 설명해주실 수 있나요?",
            "2": "장애에 대한 드림님만의 극복 방법이 있으세요?",
            "3": "저에게 그에 대한 경험을 한가지 말씀해주실 수 있나요?",
            "4": "갑자기 당황스러운 상황이 생겼을 때, 드림님은 어떻게 하실 건가요?",
            "5": "비슷한 경험이 있다면 말씀해주세요."
        },
        {
            "1": "드림님은 다른 사람들과 함께 일하는 것에 대해 어떻게 생각하세요?",
            "2": "드림님의 성격 중 장점이 무엇이라고 생각하세요?",
            "3": "혹시 그 장점이 도움이 된 적이 있나요?",
            "4": "장점이 도움이 된 경험을 저에게 한가지 말씀해주세요.",
            "5": "다른 사람들은 드림님의 성격에 대해 어떻게 얘기하곤 하나요?",
            "6": "드림님이 생각하시는 스스로의 단점은 무엇인가요?",
            "7": "혹시 그 단점을 극복하기 위한 드림님만의 계획이 있을까요?"
        }
    ]

    question = {}
    if type == "지원동기":
        question = question_list[0]
    elif type == "성장배경":
        question = question_list[1]
    elif type == "성격의장단점":
        question = question_list[2]

    model = "gpt-4o-mini"
    
    text = "user_info, question, answer 변수는 각각 취업을 원하는 장애인의 정보, 취업 준비생에게 질문한 내용, 취업 준비생이 답변 내용이 있어."
    text += f"지원서에 제출에 사용 할 {type}을 띄어쓰기를 제외하고 450글자 이상 500글자 이하로 한국어로만 작성해주고, 결과는 {type}만 반환해줘.\n"

    text += f"user_info={user}\n"
    text += f"questio={question}\n"
    text += f"answer={answer}"

    # 답변 요청
    gpt = GptAPI(model, client)
    msg = gpt.get_message(f"{text}\n")
    # print(msg)
    return msg
