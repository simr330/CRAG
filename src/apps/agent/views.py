
import asyncio
import json
import logging

from django.http import StreamingHttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from langchain_core.messages import HumanMessage
from langgraph.types import Command

from .agent import get_agent
from .serializer import DeterministicGuardRail


logger = logging.getLogger(__name__)


class AgentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = str(request.user.pk)
        agent = get_agent()

        resume_data = request.data.get("resume")

        if resume_data is not None:
            if not isinstance(resume_data, dict):
                return Response(
                    {"error": "Resume must be an object."},
                    status=400,
                )

            if type(resume_data.get("approved")) is not bool:
                return Response(
                    {"error": "approved must be true or false."},
                    status=400,
                )

            graph_input = Command(resume=resume_data)

        else:
            question = request.data.get("message")
            
            serializer = DeterministicGuardRail(data={"message": question})
            serializer.is_valid(raise_exception=True)
            print(serializer.data)
            graph_input = {
                "messages": [HumanMessage(content=serializer.data.get('message'))],
                "user_id": user_id,
            }

        config = {
            "configurable": {
                "thread_id": user_id,
            }
        }

        def event_stream():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            iterator = None

            async def stream_events():
                async for chunk in agent.astream(
                    graph_input,
                    config=config,
                    stream_mode="updates",
                ):
                    # Human-in-the-loop approval interrupt
                    interrupts = chunk.get("__interrupt__")

                    if interrupts:
                        for item in interrupts:
                            yield {
                                "event": "approval_required",
                                "thread_id": user_id,
                                "approval": item.value,
                            }
                        return

                    # The general agent's chat node
                    chat_update = chunk.get("chat")

                    if not isinstance(chat_update, dict):
                        continue

                    messages = chat_update.get("messages", [])

                    if not messages:
                        continue

                    message = messages[-1]

                    # A tool call is not a user-facing final answer.
                    if getattr(message, "tool_calls", []):
                        continue

                    content = getattr(message, "content", "")

                    if isinstance(content, str) and content.strip():
                        yield {
                            "event": "final_answer",
                            "answer": content,
                        }

            try:
                iterator = stream_events()

                while True:
                    try:
                        event_data = loop.run_until_complete(
                            iterator.__anext__()
                        )
                    except StopAsyncIteration:
                        break

                    yield (
                        f"event: {event_data['event']}\n"
                        f"data: {json.dumps(event_data, default=str)}\n\n"
                    )

                yield "data: [DONE]\n\n"

            except GeneratorExit:
                raise

            except Exception:
                logger.exception(
                    "LangGraph streaming failed for user_id=%s",
                    user_id,
                )
                yield (
                    "event: error\n"
                    f"data: {json.dumps({'error': 'The agent failed to process your request.'})}\n\n"
                )

            finally:
                if iterator is not None:
                    try:
                        loop.run_until_complete(iterator.aclose())
                    except Exception:
                        logger.exception("Error closing agent event stream")

                try:
                    loop.run_until_complete(loop.shutdown_asyncgens())
                except Exception:
                    logger.exception("Error shutting down async generators")
                finally:
                    asyncio.set_event_loop(None)
                    loop.close()

        response = StreamingHttpResponse(
            event_stream(),
            content_type="text/event-stream",
        )
        response["Cache-Control"] = "no-cache"
        response["X-Accel-Buffering"] = "no"

        return response
