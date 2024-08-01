from openai import OpenAI
from config import settings

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

def start_recommand_job(user_info):
    model = "gpt-3.5-turbo"

    job_list = ["건물 청소원(공공건물,아파트,사무실,병원,상가,공장 등)",
                "기타 보건·의료 서비스 종사원",
                "사무 보조원(일반사업체)",
                "사업체 구내식당 급식 조리사",
                "사회복지사",
                "상담 전문가",
                "웹 디자이너",
                "재가 요양보호사"]

    text = "아래 취업을 원하는 장애인 정보가 user_info 변수에 json 형식으로 있어. 이 사람에게 맞는 직무 3개를 job_list 변수 값들 중 추천해줘."
    text += "결과는 리스트만 반환해줘."
    
    user_info = {
        "email": "ryeon@dreamup.com",
        "content": {
            "personal_info": {
                "gender": "여자",
                "birth": "1997-02-18",
                "disabled_type": "지체장애",
                "disabled_level": "1급"
            },
            "residence": "경기도 수원시",
            "school": {
                "school_name": "경기대학교",
                "enrollment_period": "21.03 ~ 재학중"
            },
            "work_experience": [
                {
                    "company_name": "CJ ENM",
                    "employment_period": "23.06 ~ 23.12"
                }
            ]
        }
    }

    # 답변 요청
    gpt = GptAPI(model, client)
    msg = gpt.get_message(f"{text}\nuser_info={user_info}\njob_list={job_list}")
    result_msg = msg[1:-1].replace("'", "").split(", ")
    print(result_msg)


