import requests 
import pandas as pd

from utils.header import get_headers
from config import FETCHURL, SENDURL, REPORTURL, CASHURL, ADDURL

headers = get_headers()

def fetch_json():
    url = FETCHURL

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    return f"⚠️ Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

                return data
            except Exception as e:
                return f"❌ Ошибка при разборе JSON: {str(e)}\n\nОтвет от 1С:\n{response.text}"
        else:
            return f"❌ Ошибка от 1С: {response.status_code}\n\n{response.text}"
    except Exception as e:
        return f"🚫 Ошибка при подключении к 1С:\n{str(e)}"

def send_stock(stock_name):
    url = SENDURL

    response = requests.post(url, headers=headers, json={"Наименование": stock_name})
    if response.status_code == 200:
        try:
            data = response.json()
            if isinstance(data, dict):
                data = [data]
            elif not isinstance(data, list):
                return f"⚠️ Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

            df = pd.DataFrame(data)

            required_columns = ["Организация", "Номенклатура", "Количество", "Сумма"]
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


def get_report1c():
    url = REPORTURL

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
    url = CASHURL

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
    
#add stock
def add_stock():
    url = ADDURL

    try:
        response = requests.post(url, headers=headers)
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, dict):
                    data = [data]
                elif not isinstance(data, list):
                    return f"⚠️ Ожидался список, но получено: `{type(data).__name__}`\n\n```{data}```"

                df = pd.DataFrame(data)

                required_columns = ["Контрагент", "СтруктурнаяЕдиница", "Номенклатура", "Количество", "Цена", "Сумма"]
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