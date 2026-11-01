from langchain.tools import tool, ToolRuntime
from .services import send_email
from apps.accounts.models import User
from langgraph.types import interrupt
from .crag import get_agent
import logging

logger=logging.getLogger(__name__)

@tool
def send_report_email(
    subject: str,
    html_content: str,
    runtime: ToolRuntime,
) -> str:
    """
    Send a professionally designed HTML report email to the authenticated user.

    The recipient is automatically resolved using the authenticated user's
    ID stored in the LangGraph runtime state. The LLM cannot choose or
    override the recipient email address.

    The email body must contain well-structured, visually appealing HTML
    with a clean layout, attractive typography, appropriate spacing,
    clear headings, and properly formatted sections.

    Design the email to be responsive and readable across desktop and
    mobile email clients. Use inline CSS for styling and avoid unnecessary
    visual clutter. Ensure the HTML is complete and email-client friendly.

    Args:
        subject: A clear and descriptive email subject.
        html_content: A beautifully formatted, responsive HTML email body.
        runtime: LangGraph runtime containing the authenticated user's state.

    Returns:
        A confirmation message when the email is sent successfully.

    Security:
        - Only sends emails to the authenticated user's registered address.
        - Never accepts recipient addresses from the LLM.
        - Never accesses another user's email address.
    """
    

    user_id = runtime.state["user_id"]
    user = User.objects.get(id=user_id)
    print('EMAIL TOOL CALLED')
    decision = interrupt(
            {
                "type": "approval",
                "reason": "Send report email",
                "email": user.email,
                "subject": subject,
                "html_content": html_content,
                "instruction": "Approve sending this email?",
            }
        )
        
    try:
        if not isinstance(decision, dict) or decision.get("approved") is not True:
                return "Email sending rejected by the user."
        
        send_email(
                to_email=user.email,
                name=user.name,
                subject=subject,
                html_content=html_content,
            )
    except Exception :
         logger.exception("Email delivery failed for user_id=%s", user_id)
         return "Email delivery failed due to an internal error."
    

@tool
def knowladgebase(question: str, runtime: ToolRuntime):
    """
    Search the authenticated user's private knowledge base to answer a question.

    Args:
        question: The question to answer using the user's uploaded documents.
        runtime: Runtime context used to access the authenticated user's ID
            from the current LangGraph state.

    Returns:
        A concise answer grounded in the user's retrieved documents.
        If the documents do not contain enough relevant information, returns
        an appropriate insufficient-information response.
    """
    user_id = runtime.state["user_id"]
    crag = get_agent()
    initial_state = {
        "question": question,
        "user_id": user_id,
        "chunks": [],
        "context": "",
        "answer": "",
        "retrieval_good": False,
        "grounded": False,
        "retry_count": 0,
        "relevance_score": 0.0,
        "relevance_reason": "",
        "rewritten_question": "",
    }
    response = crag.invoke(initial_state)
    return response["answer"]
