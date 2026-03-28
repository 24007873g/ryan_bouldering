# Translation Function Commit Summary

## 1. 主要修改內容

### 前端 (index.html)

#### 主要程式片段與演進說明

**1. 新增語言選擇與翻譯、還原按鈕**
```html
<select id="targetLangSelect" class="form-input" style="width:auto;min-width:120px;">
    <option value="">🌐 Select Language</option>
    <option value="zh-tw">繁體中文</option>
    <option value="en">English</option>
    <option value="ja">日本語</option>
    ...
</select>
<button class="btn btn-translate" id="translateBtn">🌐 Translate</button>
<button class="btn" id="revertBtn">↩️ Revert</button>
```
**原因：** 讓使用者可選擇目標語言並即時翻譯，並可還原翻譯前內容。

**2. translateNote() 支援新建筆記，並暫存原始內容**
```javascript
async translateNote() {
    const content = document.getElementById('noteContent').value.trim();
    if (!content) {
        this.showMessage('請先輸入要翻譯的內容', 'error');
        return;
    }
    const targetLang = document.getElementById('targetLangSelect').value;
    if (!targetLang) {
        this.showMessage('請先選擇目標語言', 'error');
        document.getElementById('targetLangSelect').focus();
        return;
    }
    // 暫存原始內容（僅在第一次翻譯時）
    if (this.originalContent === null) {
        this.originalContent = content;
    }
    this.showMessage('翻譯中...', 'loading');
    try {
        const response = await fetch(`/api/translate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content, target_lang: targetLang })
        });
        if (!response.ok) throw new Error('翻譯失敗');
        const data = await response.json();
        document.getElementById('noteContent').value = data.translated_content;
        this.showMessage('翻譯完成！', 'success');
    } catch (error) {
        this.showMessage(`翻譯失敗: ${error.message}`, 'error');
    }
}
```
**原因：** 讓使用者在新建或編輯筆記時都能即時翻譯內容，且不會影響資料庫。

**3. revertContent() 可還原翻譯前內容**
```javascript
revertContent() {
    if (this.originalContent !== null) {
        document.getElementById('noteContent').value = this.originalContent;
        this.showMessage('已還原為原始內容', 'success');
        this.originalContent = null; // 還原後清除暫存
    } else {
        this.showMessage('沒有可還原的內容', 'error');
    }
}
```
**原因：** 提供使用者翻譯後可隨時還原，避免誤操作。

**4. 在選擇/新建筆記時重設暫存**
```javascript
selectNote(noteId) {
    // ...existing code...
    this.originalContent = null;
    // ...existing code...
}
createNewNote() {
    // ...existing code...
    this.originalContent = null;
    // ...existing code...
}
```
**原因：** 切換筆記或新建時，確保暫存內容不會殘留。

**5. Extend the translation coverage to title in translateNote()**
```javascript
                const noteId = this.currentNote && this.currentNote.id;
                const title = document.getElementById('noteTitle').value.trim();

                const targetLang = document.getElementById('targetLangSelect').value;
                if (!title && !content) {
                    this.showMessage('請先輸入標題或內容', 'error');
                    return;
                }

                if (this.originalTitle === null) {
                    this.originalTitle = title;
                }

                try {
                    let response;
                    if (noteId) {
                        response = await fetch(`/api/notes/${noteId}/translate`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ target_lang: targetLang })
                        });
                    } else {
                        response = await fetch(`/api/translate`, {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({ title, content, target_lang: targetLang })
                        });
                    }
                }
                    const data = await response.json();
                    if (data.translated_title !== undefined && data.translated_title !== null) {
                        document.getElementById('noteTitle').value = data.translated_title;
                    }
                    if (data.translated_content !== undefined && data.translated_content !== null) {
                        document.getElementById('noteContent').value = data.translated_content;
                    }
```
**原因：** More convenient 。

**6. Insert generate note function with the aid of AI chatbot**
```Javascript
document.getElementById('generateNoteBtn').addEventListener('click', function() {
            const area = document.getElementById('generateNoteArea');
            area.style.display = area.style.display === 'none' ? 'block' : 'none';
            document.getElementById('generateNoteResult').innerHTML = '';
            document.getElementById('generateNoteInput').value = '';
        });
        
        document.getElementById('generateNoteSubmit').addEventListener('click', async function() {
            const input = document.getElementById('generateNoteInput').value.trim();
            const resultDiv = document.getElementById('generateNoteResult');
            if (!input) {
                resultDiv.innerHTML = '<span style="color:#d9534f;">請輸入描述</span>';
                return;
            }
            resultDiv.innerHTML = 'AI 產生中...';
            try {
                const res = await fetch('/api/notes/generate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ content: input })
                });
                if (!res.ok) throw new Error('AI 產生失敗');
                const data = await res.json();
                if (data.error) throw new Error(data.error);
                const note = data.note;
                resultDiv.innerHTML = `
                    <div style="background:#f8f9fa;padding:10px;border-radius:8px;">
                        <b>標題：</b>${note.title || ''}<br>
                        <b>內容：</b><pre style="white-space:pre-wrap;">${note.content || ''}</pre>
                        <b>標籤：</b>${note.tags || ''}<br>
                        <b>日期：</b>${note.event_date || ''} <b>時間：</b>${note.event_time || ''}
                    </div>
                    <button id="fillToEditorBtn" style="margin-top:8px;background:#28a745;color:#fff;border:none;border-radius:8px;padding:6px 14px;cursor:pointer;">一鍵填入編輯器</button>
                `;
                document.getElementById('fillToEditorBtn').onclick = function() {
                    // 將 AI 產生內容填入編輯器
                    noteTaker.createNewNote();
                    document.getElementById('noteTitle').value = note.title || '';
                    document.getElementById('noteContent').value = note.content || '';
                    document.getElementById('noteTags').value = note.tags || '';
                    document.getElementById('noteEventDate').value = note.event_date || '';
                    document.getElementById('noteEventTime').value = note.event_time || '';
                    document.getElementById('editorTitle').textContent = note.title || 'New Note';
                };
            } catch (e) {
                resultDiv.innerHTML = `<span style="color:#d9534f;">${e.message}</span>`;
            }
        });

### 後端 (routes/note.py)

**1. 新增 /api/translate API**
```python
@note_bp.route('/translate', methods=['POST'])
def translate_content():
    """Translate arbitrary content to target language (no DB change)"""
    from src.llm import translate
    data = request.json
    title = data.get('title')
    content = data.get('content')
    target_lang = data.get('target_lang')
    if (not title and not content) or not target_lang:
        return jsonify({'error': 'title or content and target_lang required'}), 400
    try:
        translated_title = translate(title, target_lang) if title else ''
        translated_content = translate(content, target_lang) if content else ''
        return jsonify({
            'translated_title': translated_title,
            'translated_content': translated_content
        }), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@note_bp.route('/notes/<int:note_id>/translate', methods=['POST'])
def translate_note(note_id):
    """Translate note content to target language"""
    from src.llm import translate
    note = Note.query.get_or_404(note_id)
    data = request.json
    target_lang = data.get('target_lang')
    if not target_lang:
        return jsonify({'error': 'target_lang required'}), 400
    try:
        translated_title = translate(note.title, target_lang)
        translated_content = translate(note.content, target_lang)
        return jsonify({
            'translated_title': translated_title,
            'translated_content': translated_content
        }), 200
    except Exception as e:
        import traceback
        print(traceback.format_exc())  # 印出詳細錯誤
        return jsonify({'error': str(e)}), 500
```
**原因：** 讓前端可翻譯標題和內容，不需 note_id，且不會改變資料庫。

### llm.py

**1. translate 函式**
```python
def translate(text, target_language):
    # ...呼叫 LLM API 並回傳翻譯內容...
```
**原因：** 封裝 LLM 翻譯邏輯，供 API 呼叫。


## 2. 步驟與說明
1. **設計前端 UI**：在編輯器區塊新增語言選擇與翻譯、還原按鈕。
2. **前端暫存原始內容**：翻譯前將內容暫存，翻譯後可還原。
3. **API 設計**：新增 `/api/translate`，支援翻譯任意內容，不需 note_id。
4. **串接 LLM**：後端呼叫 llm.py 的 translate 函式。
5. **確保資料安全**：只有儲存或自動儲存才會寫入資料庫，翻譯/還原不影響 DB。

## 3. 影響檔案
- `src/static/index.html`
- `src/routes/note.py`
- `src/llm.py`

---

此 commit 讓使用者可在編輯或新建筆記時即時翻譯內容，並可隨時還原，提升多語言筆記體驗且不影響資料安全。
每段程式碼均有演進原因，方便日後維護與擴充。