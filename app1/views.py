

from django.shortcuts import render, redirect
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

def chat_view(request):

    if "conversation" not in request.session:
        request.session["conversation"] = []

    conversation = request.session["conversation"]

    if request.method == "POST":

        if "clear" in request.POST:
            request.session["conversation"] = []
            request.session.modified = True
            return redirect("/")

        question = request.POST.get("question")

        if question:
            conversation.append({"role": "user", "content": question})

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    *conversation
                ]
            )

            answer = response.output_text

            conversation.append({"role": "assistant", "content": answer})
            request.session.modified = True

    return render(request, "chat.html", {"conversation": conversation})
