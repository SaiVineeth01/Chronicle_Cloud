# app/routes/concept_routes.py

from flask import Blueprint, jsonify
from flask_login import login_required
from app.models import Note
from app.ai.concept_map import generate_concept_map

concept_bp = Blueprint("concept", __name__, url_prefix="/concept")

@concept_bp.route("/map/<int:note_id>")
@login_required
def get_concept_map(note_id):
    note = Note.query.get_or_404(note_id)
    graph_data = generate_concept_map(note.content)
    return jsonify(graph_data)
