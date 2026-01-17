from django.shortcuts import render, redirect
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def chat_view(request):

    # Create session conversation if not exists
    if "conversation" not in request.session:
        request.session["conversation"] = []

    conversation = request.session["conversation"]

    if request.method == "POST":

        # Clear chat
        if "clear" in request.POST:
            request.session["conversation"] = []
            request.session.modified = True
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

            # IMPORTANT
            request.session.modified = True

    return render(request, "chat.html", {
        "conversation": conversation
    })
