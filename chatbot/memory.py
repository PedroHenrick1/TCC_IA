from langchain.schema import HumanMessage, AIMessage, BaseChatMessageHistory
from .models import ConversationHistory

class DjangoDBChatMessageHistory(BaseChatMessageHistory):
    """Histórico de mensagens salvo no banco Django"""

    def __init__(self, session_id: str):
        self.session_id = session_id

    @property
    def messages(self):
        history = ConversationHistory.objects.filter(session_id=self.session_id).order_by("created_at")
        messages = []
        for chat in history:
            messages.append(HumanMessage(content=chat.human_message))
            messages.append(AIMessage(content=chat.ai_message))
        return messages

    def add_message(self, message):
        """Adiciona uma mensagem (Humano ou AI) no banco"""
        if isinstance(message, HumanMessage):
            ConversationHistory.objects.create(
                session_id=self.session_id,
                human_message=message.content,
                ai_message=""  # placeholder
            )
        elif isinstance(message, AIMessage):
            # Atualiza o último registro humano com a resposta da IA
            last = ConversationHistory.objects.filter(
                session_id=self.session_id
            ).order_by("-created_at").first()
            if last:
                last.ai_message = message.content
                last.save()

    def clear(self):
        ConversationHistory.objects.filter(session_id=self.session_id).delete()