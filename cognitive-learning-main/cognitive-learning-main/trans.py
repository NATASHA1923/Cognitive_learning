from deep_translator import GoogleTranslator

# proxies_example = {
#     "http": "172.31.98.222:5000"
# }
translated_text = GoogleTranslator(source='auto', target='de').translate("keep it up, you are awesome")  
# output -> Weiter so, du bist großartig
print(translated_text.text)