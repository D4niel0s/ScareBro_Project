from PIL import Image


cat = Image.open("cat.jpg")
cat2 = Image.open("cat2.jpg")

cat.save("cat2.jpg") # Saves cat image into cat2.jpg