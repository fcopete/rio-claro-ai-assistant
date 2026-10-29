from flask import Blueprint, request, jsonify
from services.chat_service import ask_chatbot
chat_bp=Blueprint("chat",__name__)
@chat_bp.route("/ask",methods=["POST"])
def ask():
    payload=request.get_json()
    question=payload.get("question","").strip()
    history=payload.get("history",[])
    if not question: return jsonify({"success":False,"message":"Question is required"}),400
    return jsonify({"success":True,"answer":ask_chatbot(question,history)})
