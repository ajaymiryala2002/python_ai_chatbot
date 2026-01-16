from django.shortcuts import render, redirect
from openai import OpenAI
from python_ai_agent import settings


client = OpenAI(api_key=settings.OPENAI_API_KEY)

conversation = []

def chat_view(request):
    global conversation

    if request.method == "POST":

        # Clear chat
        if "clear" in request.POST:
            conversation.clear()
            return redirect("/")

        question = request.POST.get("question")

        if question:
            conversation.append({
                "role": "user",
                "content": question
            })

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": "You are an assistant that ALWAYS uses web search for latest and present information."
                    },
                    *conversation
                ],
                tools=[{"type": "web_search"}]
            )

            answer = response.output_text

            conversation.append({
                "role": "assistant",
                "content": answer
            })

    return render(request, "chat.html", {
        "conversation": conversation
    })