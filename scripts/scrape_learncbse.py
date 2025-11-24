import requests
from bs4 import BeautifulSoup
import os

# ONLY Class 12 Maths chapter-wise NCERT solution links
URLS = [
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-relations-and-functions/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-inverse-trigonometric-functions/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-3-matrices/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-4-determinants/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-continuity-and-differentiability/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-application-of-derivatives/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-integrals/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-8-application-of-integrals/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-differential-equations/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-10-vector-algebra/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-11-three-dimensional-geometry/",
    "https://www.learncbse.in/ncert-solutions-for-class-12th-maths-chapter-12-linear-programming/",
    "https://www.learncbse.in/ncert-solutions-for-class-12-maths-probability/"
]

output_folder = "data/solutions_learncbse"
os.makedirs(output_folder, exist_ok=True)

print("Scraping ONLY LearnCBSE Class 12 Maths...")

for url in URLS:
    try:
        print("Fetching:", url)
        page = requests.get(url).text
        soup = BeautifulSoup(page, "html.parser")

        # extract readable text
        content = soup.get_text("\n")

        # filename based on last part of URL
        name = url.rstrip("/").split("/")[-1]
        filename = f"{name}.txt"

        filepath = os.path.join(output_folder, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        print("Saved:", filename)

    except Exception as e:
        print("Error:", e)

print("✅ LearnCBSE Class 12 Maths scraping COMPLETE")
