import base64
import requests 
import pandas as pd

def fetch_json():
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
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"
    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"


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

                required_columns = ["Организация", "БанковскийСчет", "Сумма", "СуммаВал"]
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = ""
                
                df = df[required_columns]

                table = "📋 *Отчёт из 1С:*\n"
                table += "```\n"
                table += df.to_string(index=False)
                table += "\n```"

                return table

            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"

    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"


def get_cash1c():
    url = "http://localhost/telegram/hs/tg/cash"
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

                required_columns = ["Организация", "Касса", "Сумма", "СуммаВал"]
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = ""
                
                df = df[required_columns]

                table = "📋 *Отчёт из 1С:*\n"
                table += "```\n"
                table += df.to_string(index=False)
                table += "\n```"

                return table

            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"

    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"


def get_stock1c():
    url = "http://localhost/telegram/hs/tg/stock"
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

                required_columns = ["Организация", "Наименование"]
                for col in required_columns:
                    if col not in df.columns:
                        df[col] = ""
                
                df = df[required_columns]

                table = "📋 *Отчёт из 1С:*\n"
                table += "```\n"
                table += df.to_string(index=False)
                table += "\n```"

                return table

            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"

    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"