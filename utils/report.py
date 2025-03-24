import base64
import requests

def get_report1c():
    url = "http://localhost/telegram/hs/tg/report"
    username = "Админ"
    password = ""

    credentials = f"{username}:{password}".encode("utf-8")
    encoded_credentials = base64.b64encode(credentials).decode("utf-8")

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if not isinstance(data, list):
                    return f"⚠️ Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

                table = "📋 *Отчёт из 1С:*\n"
                table += "```\n{:25} {:10}\n".format("Клиент", "Сумма")
                table += "-" * 38 + "\n"

                for row in data:
                    table += "{:25} {:10.2f}\n".format(
                        row.get("Клиент", ""), row.get("Сумма", 0)
                    )

                table += "```"
                return table

            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"

    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"
