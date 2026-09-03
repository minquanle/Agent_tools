import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage

# Nap cau hinh moi truong bao mat
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")


@tool
def calculator(a: float, b: float, operation: str) -> str:
    """Thuc hien phep tinh so hoc giua hai so a va b.
    Dung tool nay khi can ket qua tinh toan chinh xac.
    Tham so operation nhan mot trong bon gia tri:
    'add' (cong), 'subtract' (tru), 'multiply' (nhan), 'divide' (chia).
    """
    if operation == "add":
        ket_qua = a + b
    elif operation == "subtract":
        ket_qua = a - b
    elif operation == "multiply":
        ket_qua = a * b
    elif operation == "divide":
        if b == 0:
            return "Loi: khong the chia cho 0"
        ket_qua = a / b
    else:
        return f"Loi: operation '{operation}' khong hop le"
    return str(ket_qua)


@tool
def count_words(text: str) -> str:
    """Dem so tu trong mot doan van ban tieng Viet hoac tieng Anh.
    Dung tool nay khi nguoi dung muon biet so luong tu cua mot cau
    hoac mot doan van. Tham so text la chuoi van ban can dem.
    """
    so_tu = len(text.split())
    return f"Doan van co {so_tu} tu"

# Danh sach tool va tu dien tra cuu theo ten
tools = [calculator, count_words]
tool_map = {t.name: t for t in tools}

# Khoi tao mo hinh, dat temperature=0 de ket qua on dinh
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Gan bo tool vao mo hinh
llm_with_tools = llm.bind_tools(tools)

def run_agent(cau_hoi: str, max_buoc: int = 5) -> str:
    # Bat dau voi cau hoi cua nguoi dung
    messages = [HumanMessage(content=cau_hoi)]

    for _ in range(max_buoc):
        # 1. Goi mo hinh voi toan bo lich su tin nhan hien tai
        ai_msg = llm_with_tools.invoke(messages)
        messages.append(ai_msg)

        # 2. Neu mo hinh khong goi tool nao -> day la cau tra loi cuoi
        if not ai_msg.tool_calls:
            return ai_msg.content

        # 3. Mo hinh yeu cau goi mot hoac nhieu tool
        for tool_call in ai_msg.tool_calls:
            ten_tool = tool_call["name"]
            tham_so = tool_call["args"]
            print(f"[LOG] Model goi tool: {ten_tool} | Tham so: {tham_so}")

            # Tim dung ham Python va thuc thi voi tham so mo hinh de xuat
            selected_tool = tool_map[ten_tool]
            ket_qua = selected_tool.invoke(tham_so)
            print(f"[LOG] Ket qua tra ve: {ket_qua}")

            # 4. Dong goi ket qua vao ToolMessage de gui lai cho mo hinh
            messages.append(
                ToolMessage(content=str(ket_qua),
                            tool_call_id=tool_call["id"])
            )

    # Neu vuot qua so buoc cho phep ma van chua xong
    return "Da dat gioi han so buoc xu ly, vui long thu lai cau hoi don gian hon."

if __name__ == "__main__":
    print("=" * 60)
    print("Chatbot Agent Tool Calling đã sẵn sàng!")
    print("Gõ 'exit' hoặc 'quit' để thoát.")
    print("=" * 60)
    
    while True:
        cau_hoi = input("\nNguoi dung: ")
        if cau_hoi.lower() in ['exit', 'quit']:
            print("Tạm biệt!")
            break
            
        if not cau_hoi.strip():
            continue
            
        cau_tra_loi = run_agent(cau_hoi)
        print(f"Agent: {cau_tra_loi}")
