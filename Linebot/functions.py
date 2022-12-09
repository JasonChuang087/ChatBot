import requests
from bs4 import BeautifulSoup


def Chat(text):
    # ptt文章搜尋
    URL = "https://www.ptt.cc/bbs/Tech_Job/search?q="+text
    response = requests.get(URL)
    content = ""
    if response.status_code != 200:
        content = "連結錯誤"
        return content
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        # 搜尋特定html標籤
        titles = soup.find_all('div', 'title', 'a')
        # 若沒有該公司內容 則return
        if not titles:
            content = "沒有相關新聞"
            return content
        for title in titles:
            # 擷取新聞分類 移除回文
            if "新聞" in title.text and "Re:" not in title.text:
                content += title.text.replace('\n', '') + '\n'
    return content
