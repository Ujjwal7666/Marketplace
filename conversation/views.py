import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from item.models import Items
from .models import Conversation, ConversationMessage

logger = logging.getLogger('django')
@login_required
def new_conversation(request, pk):
    try:
        item = Items.objects.get(pk=pk)

        if item.created_by == request.user:
            return redirect('userdashboard')  # Prevent users from messaging themselves

        conversation = Conversation.objects.filter(item=item).filter(members__in=[request.user.id])

        if conversation.exists():
            return redirect('conversation_detail', pk=conversation.first().id)  # Redirect to existing conversation

        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                conversation = Conversation.objects.create(item=item)
                conversation.members.add(request.user)
                conversation.members.add(item.created_by)
                conversation.save()

                conversation_message = ConversationMessage.objects.create(
                    conversation=conversation,
                    content=content,
                    created_by=request.user
                )

                return redirect('detail-pk', pk=item.pk)  # Redirect to item detail or another relevant page

        return render(request, 'conversation/new.html', {'item': item})
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'conversation/new.html', {'item': item})

@login_required
def inbox(request):
    try:
        conversations = Conversation.objects.filter(members__in=[request.user.id])
        return render(request, 'conversation/inbox.html', {'conversations': conversations})
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'conversation/inbox.html', {'conversations': conversations})
    
@login_required
def conversation_detail(request, pk):
    try:
        conversation = get_object_or_404(Conversation, pk=pk)

        if request.user not in conversation.members.all():
            return redirect('inbox')

        if request.method == 'POST':
            content = request.POST.get('content')
            if content:
                ConversationMessage.objects.create(
                    conversation=conversation,
                    content=content,
                    created_by=request.user
                )
                return redirect('conversation_detail', pk=pk)

        messages = conversation.message.all()
        return render(request, 'conversation/conversation_detail.html', {'conversation': conversation, 'messages': messages})
    
    except Exception as exe:
        logger.error(str(exe), exc_info=True)
        return render(request, 'conversation/conversation_detail.html', {'conversation': conversation, 'messages': messages})