import os
import requests
from bs4 import BeautifulSoup

# List of Apple Support article URLs
APPLE_SUPPORT_URLS = [
    "https://support.apple.com/en-us/120922",  # Table of content
    "https://support.apple.com/en-us/100350", # Intoduction 
    "https://support.apple.com/en-us/100353",  # Battery Safety
    "https://support.apple.com/en-us/102487", # Quick Checks
    "https://support.apple.com/en-us/102488", #  Dignostics for Self Service Repair
    "https://support.apple.com/en-us/102490", # Bluetooth Help
    "https://support.apple.com/en-us/102489#display2", # Camera and Sensor 
    "https://support.apple.com/en-us/102489#display1", # Display and Images 
    "https://support.apple.com/en-us/102492#input_output2", # Keyboard backlight issues
    "https://support.apple.com/en-us/102492#input_output1", # Keyboard functional issues 
    "https://support.apple.com/en-us/102492#input_output4", # Power button or Touch ID issues
    "https://support.apple.com/en-us/102492#input_output6", # SD Card issues 
    "https://support.apple.com/en-us/102492#input_output3", # Track Pad issues 
    "https://support.apple.com/en-us/102492#input_output5", # Usb-c, thunderbolt, and htmi issues
    "https://support.apple.com/en-us/102493", # Overheating hardware issues
    "https://support.apple.com/en-us/102494#power4", # Battery and power issues 
    "https://support.apple.com/en-us/102494#power2", # Intermittent shutdown or system instability
    "https://support.apple.com/en-us/102494#power1", # Sleep and wake issues
    "https://support.apple.com/en-us/102494#power3", # Startup issues
    "https://support.apple.com/en-us/102491#sound2", # Microphone issues
    "https://support.apple.com/en-us/102491#sound1", # Speaker or headphone issues 
    "https://support.apple.com/en-us/120927", # Exploded parts and orderable parts
    "https://support.apple.com/en-us/120926", # Screws 
    "https://support.apple.com/en-us/121157", # Tools
    "https://support.apple.com/en-us/100355", # First steps
    "https://support.apple.com/en-us/101268", # Key Overview
    "https://support.apple.com/en-us/120759", # Bottom Case
    "https://support.apple.com/en-us/120760", # Battery Management Unit Flex Case 
    "https://support.apple.com/en-us/120761", # Lid Angle cable 
    "https://support.apple.com/en-us/120762", # Trackpad Flex Cable
    "https://support.apple.com/en-us/120764", # Vent and Anthena Module
    "https://support.apple.com/en-us/120766", # Disply Hinge Cable
    "https://support.apple.com/en-us/120767", # Disply
    "https://support.apple.com/en-us/120929", # Speakers
    "https://support.apple.com/en-us/120769", # Logic Board
    "https://support.apple.com/en-us/120772", # Audio Board
    "https://support.apple.com/en-us/120750", # MagSafe Board
    "https://support.apple.com/en-us/120776", # Touch ID Board
    "https://support.apple.com/en-us/120778", # USB-C Board
    "https://support.apple.com/en-us/120779", # Top case Battery and Keyboard
]


OUTPUT_DIR = "Manuals/apple"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def find_article_content(soup):
    selectors = [
        "main",
        ".article-content",
        ".as-content",
        "article",
        "section",
        "div[class*=content]",  # divs with 'content' in class name
    ]
    
    for selector in selectors:
        container = soup.select_one(selector)
        if container:
            return container
    
    # Final fallback: entire body
    return soup.body


def scrape_article(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Get title
        title = soup.find("h1").get_text(strip=True) if soup.find("h1") else "Untitled"

        # Get article content from known containers
        container = find_article_content(soup)
        if not container:
            print(f"[WARN] No known content container found in {url}")
            return None

        paragraphs = container.find_all(["p", "li", "h2", "h3"])
        content = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        return {"title": title, "content": content}
    except Exception as e:
        print(f"[ERROR] Failed to scrape {url}: {e}")
        return None

def save_to_file(title, content, index):
    filename = f"apple_article_{index}.txt"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(title + "\n\n" + content)
    print(f"[SAVED] {filename}")

def main():
    for idx, url in enumerate(APPLE_SUPPORT_URLS):
        article = scrape_article(url)
        if article:
            save_to_file(article["title"], article["content"], idx)

if __name__ == "__main__":
    main()