import requests
from bs4 import BeautifulSoup
import os

URLS = [
    "https://www.kseebsolutions.com/2nd-puc-maths-model-question-paper-1/",
    "https://www.kseebsolutions.com/2nd-puc-maths-model-question-paper-2/",
    "https://www.kseebsolutions.com/2nd-puc-maths-model-question-paper-3/",
    "https://www.kseebsolutions.com/2nd-puc-maths-model-question-paper-4/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-march-2020/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-march-2019/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-march-2018/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-june-2019/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-june-2018/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-march-2017/",
    "https://www.kseebsolutions.com/2nd-puc-maths-previous-year-question-paper-june-2017/"
]

output_folder = "data/solutions_kseeb"
os.makedirs(output_folder, exist_ok=True)

print("Scraping ONLY KSEEB Maths Model + Previous Year Papers...")

for url in URLS:
    try:
        print("Fetching:", url)
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")

        content = soup.get_text("\n")

        name = url.rstrip("/").split("/")[-1]
        filename = f"{name}.txt"

        filepath = os.path.join(output_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print("Saved:", filename)

    except Exception as e:
        print("Error:", e)

print("✅ KSEEB scraping COMPLETE")
