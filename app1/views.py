from django.shortcuts import render, redirect
from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = "You are an assistant that ALWAYS uses web search for latest and present information."
MAX_HISTORY = 6  # Keep only last 6 messages to speed up responses

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
            conversation.append({"role": "user", "content": question})

            # Only keep last MAX_HISTORY messages to reduce latency
            recent_messages = conversation[-MAX_HISTORY:]

            # gpt-4.1-nano (FAST) - do NOT use tools
            response = client.responses.create(
                model="gpt-4.1-nano",
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *recent_messages
                ]
            )

            answer = response.output_text

            conversation.append({"role": "assistant", "content": answer})

            # Save session
            request.session.modified = True

    return render(request, "chat.html", {"conversation": conversation})
