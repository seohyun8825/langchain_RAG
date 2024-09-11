from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pyperclip
import time

def standardize_line_breaks(text):
    return text.replace('\r\n', '\n').replace('\r', '\n')

def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("대화 내용을 클립보드에 복사했습니다.")

def scroll_down_page(driver, timeout):
    """조금이따가 """
    scroll_pause_time = 2
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(scroll_pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def fetch_conversation_from_link(link):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(link)

    try:
        scroll_down_page(driver, 10)
        page_source = driver.page_source
        driver.quit()

        soup = BeautifulSoup(page_source, 'html.parser')

        conversation_data = []
        articles = soup.find_all('article')

        for article in articles:
            user_message_tag = article.find('h5', class_='sr-only')
            gpt_message_tag = article.find('h6', class_='sr-only')
            content_tag = article.find('div', class_="text-base")

            if user_message_tag and content_tag:
                conversation_data.append({
                    'author': 'user',
                    'content': content_tag.get_text(strip=True)
                })
            if gpt_message_tag and content_tag:
                conversation_data.append({
                    'author': 'assistant',
                    'content': content_tag.get_text(strip=True)
                })


        for entry in conversation_data:
            print(f"Author: {entry['author']}, Content: {entry['content'][:500]}")  

        return conversation_data

    except Exception as e:
        print(f"대화 내용을 가져오는 중 오류가 발생했습니다: {e}")
        driver.quit()
        return None


def transform_conversation_to_text(conversation_data):
    """
    return: 변환된 텍스트
    """
    output_text = []
    for entry in conversation_data:
        if entry['author'] == 'user':
            output_text.append(f"You:\n{entry['content']}")
        elif entry['author'] == 'assistant':
            output_text.append(f"ChatGPT:\n{entry['content']}")

    return "\n\n".join(output_text)

def export_to_text(conversation_link):
    conversation_data = fetch_conversation_from_link(conversation_link)
    if conversation_data:
        text_output = transform_conversation_to_text(conversation_data)
        standardized_text = standardize_line_breaks(text_output)
        copy_to_clipboard(standardized_text)
    else:
        print("대화 내용을 변환하지 못했습니다.")

if __name__ == "__main__":
    link = "https://chatgpt.com/share/68e6ee7c-23ee-4527-bf3d-7d4d4f4e98f8"  
    export_to_text(link)