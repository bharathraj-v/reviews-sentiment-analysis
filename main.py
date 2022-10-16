from selenium import webdriver
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from transformers import pipeline
import csv

driver = webdriver.Chrome("/usr/bin/chromedriver")


driver.get("https://www.amazon.in/Apple-iPhone-13-Mini-256GB/dp/B09G99CW2C/ref=sr_1_6?keywords=iphone%2B13&qid=1665947049&qu=eyJxc2MiOiI0LjU4IiwicXNhIjoiNC4wNCIsInFzcCI6IjMuNDQifQ%3D%3D&sprefix=iphon%2Caps%2C267&sr=8-6&th=1")

driver.find_elements("xpath", "//a[@data-hook='see-all-reviews-link-foot']")[0].click()


next_page = driver.find_elements("xpath", "//li[@class='a-last']")
reviews = []
while next_page:
    reviews.extend([i.text for i in driver.find_elements("xpath","//div[@data-hook='review']")])
    next_page[0].click()
    driver.refresh()
    next_page = driver.find_elements("xpath", "//li[@class='a-last']")

print(len(reviews))
reviews = reviews[0:len(reviews)-1]

only_reviews = []
for i in reviews:
    only_reviews.append(i.split("\n")[4])

driver.close()

with open("reviews.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["Reviews"])
    writer.writerows(zip(only_reviews))


words = []
for i in only_reviews:
    words.extend(i.split(" "))

# stopwords = set(STOPWORDS)

# wordcloud = WordCloud(width = 800, height = 800,
#                 background_color ='white',
#                 stopwords = stopwords,
#                 min_font_size = 10).generate(" ".join(words))

# plt.figure(figsize = (8, 8), facecolor = None)
# plt.imshow(wordcloud)
# plt.axis("off")
# plt.tight_layout(pad = 0)

# plt.show()

sentiment_pipeline = pipeline("sentiment-analysis")
sentiments = sentiment_pipeline(only_reviews)

pos = []
neg = []

for i in sentiments:
    if i["label"] == "POSITIVE":
        pos.append(i["score"])
    else:
        neg.append(i["score"])
print(len(pos), len(neg))
