import json
import xml.etree.ElementTree as ET
import requests
import google.auth
from google.auth.transport.requests import Request

# 1. ТАНЫ ВЭБСАЙТЫН ТОХИРГОО
BLOG_FEED_URL = "https://blogspot.com"
SCOPES = ["https://googleapis.com"]

def get_latest_post_url():
    """Blogger-оос хамгийн сүүлд орсон киноны линкийг автоматаар шүүж авах функц"""
    try:
        response = requests.get(BLOG_FEED_URL, timeout=20)
        if response.status_code != 200:
            print("❌ Blogger-оос дата татаж чадсангүй.")
            return None
        
        # XML бүтцийг унших
        root = ET.fromstring(response.content)
        
        # Atom feed-ийн namespace тохируулах
        ns = {'atom': 'http://w3.org'}
        
        # Хамгийн эхний постыг (entry) олох
        entry = root.find('atom:entry', ns)
        if entry is None:
            print("⚠ Блог дээр ямар нэгэн пост олдсонгүй.")
            return None
            
        # Постын жинхэнэ холбоосыг (link) шүүж авах
        for link in entry.findall('atom:link', ns):
            if link.attrib.get('rel') == 'alternate':
                return link.attrib.get('href')
                
    except Exception as e:
        print(f"❌ Холбоос илрүүлэх явцад алдаа гарлаа: {e}")
        return None

def get_credentials():
    """Google Cloud баталгаажуулалт хийх функц"""
    credentials, project = google.auth.default(scopes=SCOPES)
    if not credentials.valid:
        credentials.refresh(Request())
    return credentials

def send_to_google_indexing():
    """Шинэ линкийг Google Indexing API рүү шууд тушааж илгээх"""
    # Шинэ постын линкийг автоматаар илрүүлэх
    target_url = get_latest_post_url()
    
    if not target_url:
        print("❌ Илгээх идэвхтэй холбоос олдсонгүй. Программ зогслоо.")
        return

    print(f"🔍 Хамгийн сүүлийн шинэ кино олдлоо: {target_url}")
    print("⏳ Google рүү шууд индексжүүлэх хүсэлт илгээж байна...")

    # Google-ийн эрхийг шалгах
    credentials = get_credentials()
    endpoint = "https://googleapis.com"
    
    headers = {
        "Authorization": f"Bearer {credentials.token}",
        "Content-Type": "application/json"
    }
    
    # Албан ёсны Indexing API дата бүтэц
    data = json.dumps({
        "url": target_url,
        "type": "URL_UPDATED"  # Шинэ линк оруулах эсвэл шинэчилснийг илтгэнэ
    })
    
    response = requests.post(endpoint, headers=headers, data=data, timeout=30)
    
    if response.status_code == 200:
        print("🚀 АМЖИЛТТАЙ! Google энэ киноны линкийг дараалал харгалзахгүй уншихаар хүлээн авлаа.")
        print(response.json())
    else:
        print(f"❌ Google Indexing API алдаа заалаа: Status {response.status_code}")
        print(response.text)
        raise SystemExit(1)

if __name__ == "__main__":
    send_to_google_indexing()
