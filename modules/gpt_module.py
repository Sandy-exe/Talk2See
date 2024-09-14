import openai

openai.api_key = "sk-proj-cXLhIgKLVWjY05X0EdPVT3BlbkFJcpOLCPa72OUdnpLOyI5r"

def chatgpt_api(input_text):
    messages = [
        {"role": "system", "content": "Process the given input by correcting and enhancing the information in the 'Image Captioning' section. If the text cannot be corrected or is unreadable, return 'Error'. Additionally, interpret the information provided in the 'OCR' and 'Object Distance' sections. Provide clear, concise responses that are accessible to a visually impaired individual. Use simple language to describe the scene, text, and distance details, ensuring the response is easy to understand."},
    ]

    if input_text:
        messages.append({"role": "user", "content": input_text})

    try:
        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        reply = chat_completion.choices[0].message['content']
        return reply
    except Exception as e:
        print("Error during OpenAI API call:", e)
        return "Error"
