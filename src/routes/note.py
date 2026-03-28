from flask import Blueprint, jsonify, request
from src.models.note import Note, db
from datetime import datetime, date, time

note_bp = Blueprint('note', __name__)

@note_bp.route('/notes', methods=['GET'])
def get_notes():
    """Get all notes, ordered by order then updated_at"""
    user_id = request.args.get('user_id', type=int)
    q = Note.query
    if user_id:
        q = q.filter_by(user_id=user_id)
    notes = q.order_by(Note.order.asc(), Note.updated_at.desc()).all()
    return jsonify([note.to_dict() for note in notes])

# 批次更新筆記順序
@note_bp.route('/notes/order', methods=['PUT'])
def update_notes_order():
    """Update notes order by a list of note ids"""
    try:
        data = request.json
        note_ids = data.get('note_ids')
        if not note_ids or not isinstance(note_ids, list):
            return jsonify({'error': 'note_ids (list) required'}), 400
        for idx, note_id in enumerate(note_ids):
            note = Note.query.get(note_id)
            if note:
                note.order = idx
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes', methods=['POST'])
def create_note():
    """Create a new note"""
    try:
        data = request.json
        if not data or 'title' not in data or 'content' not in data:
            return jsonify({'error': 'Title and content are required'}), 400
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': 'user_id required'}), 400
        
        # 處理日期和時間字符串
        event_date = None
        if data.get('event_date'):
            try:
                event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            except ValueError:
                pass

        event_time = None
        if data.get('event_time'):
            try:
                event_time = datetime.strptime(data['event_time'], '%H:%M').time()
            except ValueError:
                pass

        note = Note(
            title=data['title'],
            content=data['content'],
            tags=data.get('tags'),
            event_date=event_date,
            event_time=event_time,
            user_id=user_id
        )
        db.session.add(note)
        db.session.commit()
        return jsonify(note.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# AI generation endpoint removed

@note_bp.route('/notes/<int:note_id>', methods=['GET'])
def get_note(note_id):
    """Get a specific note by ID"""
    note = Note.query.get_or_404(note_id)
    return jsonify(note.to_dict())

@note_bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    """Update a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        note.title = data.get('title', note.title)
        note.content = data.get('content', note.content)
        note.tags = data.get('tags', note.tags)

        # 處理日期
        if 'event_date' in data:
            try:
                note.event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date() if data['event_date'] else None
            except ValueError:
                pass

        # 處理時間
        if 'event_time' in data:
            try:
                note.event_time = datetime.strptime(data['event_time'], '%H:%M').time() if data['event_time'] else None
            except ValueError:
                pass
        # 若 event_date 或 event_time 沒有在 data 中，則不覆蓋原本的值

        db.session.commit()
        return jsonify(note.to_dict())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    """Delete a specific note"""
    try:
        note = Note.query.get_or_404(note_id)
        db.session.delete(note)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@note_bp.route('/translate', methods=['POST'])
def translate_content():
    """Translate arbitrary content to target language (no DB change)"""
    return jsonify({'error': 'translation feature removed'}), 404

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    return jsonify({'error': 'translation feature removed'}), 404

@note_bp.route('/notes/search', methods=['GET'])
def search_notes():
    """Search notes by title or content"""
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    
    notes = Note.query.filter(
        (Note.title.contains(query)) | (Note.content.contains(query))
    ).order_by(Note.updated_at.desc()).all()
    
    return jsonify([note.to_dict() for note in notes])

