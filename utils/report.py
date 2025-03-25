import base64
import requests
import pandas as pd

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
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    return f"⚠️ Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

                df = pd.DataFrame(data)

                if "Клиент" not in df.columns or "Сумма" not in df.columns:
                    return f"❌ Отсутствуют поля 'Клиент' и 'Сумма' в данных:\n\n```{df.head().to_string()}```"

                df["Сумма"] = pd.to_numeric(df["Сумма"], errors="coerce").fillna(0)
                df_formatted = df[["Клиент", "Сумма"]]

                table = "📋 *Отчёт из 1С:*\n"
                table += "```\n" + df_formatted.to_string(index=False, justify='left', col_space=15, float_format="%.2f") + "\n```"

                return table

            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"

    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"
