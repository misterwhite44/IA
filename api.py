import google.generativeai as genai

genai.configure(api_key="AIzaSyDlag4KG1IKuMUuuWjFtLP91cF6O_B6ZGQ")
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("write an html code plz ")
print(response.text)