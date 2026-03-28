[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=20416479)
# NoteTaker - Personal Note Management Application

A modern, responsive web application for managing personal notes with a beautiful user interface and full CRUD functionality.

## 🌟 Features

- **Create Notes**: Add new notes with titles and rich content
- **Edit Notes**: Update existing notes with real-time editing
- **Delete Notes**: Remove notes you no longer need
- **Search Notes**: Find notes quickly by searching titles and content
- **Auto-save**: Notes are automatically saved as you type
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time Updates**: Instant feedback and updates

## 🚀 Live Demo

The application is deployed and accessible at: **https://note-taking-app-ericleung712.vercel.app**

## 🛠 Technology Stack

### Frontend
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and API communication

### Backend
- **Python Flask**: Web framework for API endpoints
- **SQLAlchemy**: ORM for database operations
- **Flask-CORS**: Cross-origin resource sharing support

### Database
- **PostgreSQL**: Lightweight, file-based database for data persistence

## 📁 Project Structure

```
note-taking-app-ericleung712/
├── src/
│   ├── models/
│   │   ├── user.py          # User model
│   │   └── note.py          # Note model with DB schema
│   ├── routes/
│   │   ├── user.py          # User API endpoints
│   │   └── note.py          # Note API endpoints (CRUD, search, AI, translation)
│   ├── static/
│   │   └── index.html       # Frontend UI (pure HTML/CSS/JS)
│   ├── llm.py               # AI note generation/translation (OpenAI, prompt)
│   ├── note_generation_prompt.py # Prompt template for AI note generation
│   └── main.py              # Flask application entry point
├── requirements.txt         # Python dependencies
├── README.md                # This documentation
├── AI_generate_note.md      # AI note generation instructions
├── Deployment_on_Vercel.md  # Vercel deployment guide
├── deploy_vercel.sh         # Vercel deployment script
├── test_api.http            # API test file
├── test_note_generation.py  # AI note generation test
├── token.txt                # Token file (secret)
├── translation_commit_summary.md # Translation commit summary
├── vercel.json              # Vercel config
```

## 🔧 Local Development Setup

### Prerequisites
- Python 3.11+
- pip (Python package manager)

### Installation Steps

1. **Clone or download the project**
   ```bash
   python -m venv venv
   ```

2. **Activate the virtual environment**
   ```bash
   source venv/bin/activate
   ```

   Remark: On Windows, use `venv\Scripts\activate`

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python src/main.py
   ```

5. **Access the application**
   - Open your browser and go to `http://localhost:5001`

## 📡 API Endpoints

### Notes API

- `GET /notes` - Get all notes
- `POST /notes` - Create a new note
- `GET /notes/<id>` - Get a specific note
- `PUT /notes/<id>` - Update a note
- `DELETE /notes/<id>` - Delete a note
- `PUT /notes/order` - Batch update note order
- `POST /notes/generate` - AI generate structured note (not saved to DB)
- `POST /notes/<id>/translate` - Translate a specific note
- `POST /translate` - Translate arbitrary content (not saved to DB)
- `GET /notes/search?q=<query>` - Search notes (title/content)

### Request/Response Format
### Note Data Format
```json
{
   "id": 1,
   "title": "My Note Title",
   "content": "Note content here...",
   "tags": ["tag1", "tag2"],
   "event_date": "2025-10-19",
   "event_time": "17:00",
   "order": 0,
   "created_at": "2025-10-19T11:26:38.123456",
   "updated_at": "2025-10-19T11:27:30.654321"
}
```

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Create new notes instantly
- **Notes List**: Scrollable list of all notes with previews
- **Note Previews**: Show title, content preview, and last modified date

### Editor Panel
- **Title Input**: Edit note titles
- **Content Textarea**: Rich text editing area
- **Save Button**: Manual save option (auto-save also available)
- **Delete Button**: Remove notes with confirmation
- **Real-time Updates**: Changes reflected immediately

### Design Elements
- **Gradient Background**: Beautiful purple gradient backdrop
- **Glass Morphism**: Semi-transparent panels with backdrop blur
- **Smooth Animations**: Hover effects and transitions
- **Responsive Layout**: Adapts to different screen sizes
- **Modern Typography**: Clean, readable font stack

## 🔒 Database Schema

### Notes Table
```sql
CREATE TABLE note (
   id INTEGER PRIMARY KEY,
   title VARCHAR(200) NOT NULL,
   content TEXT NOT NULL,
   tags VARCHAR(500),
   event_date DATE,
   event_time TIME,
   order INTEGER DEFAULT 0,
   created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
   updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚀 Deployment

The application is configured for easy deployment with:
- CORS enabled for cross-origin requests
- Host binding to `0.0.0.0` for external access
- Production-ready Flask configuration
- Persistent SQLite database

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `development` for debug mode
- `SECRET_KEY`: Flask secret key for sessions

### Database Configuration
- Database file: `src/database/app.db`
- Automatic table creation on first run
- SQLAlchemy ORM for database operations

## 📱 Browser Compatibility

- Chrome/Chromium (recommended)
- Firefox
- Safari

## 🎨 User Interface Features

### Sidebar
- **Search Box**: Real-time search through note titles and content
- **New Note Button**: Quickly create new notes
- **Notes List**: Scrollable, preview title/content/date

### Editor Panel
- **Title Input**: Edit note title
- **Content Editor**: Rich text editing area
- **Save Button**: Manual save (auto-save also available)
- **Delete Button**: Delete note (with confirmation)
- **Real-time Updates**: Changes reflected immediately

### Other Features
- **AI Structured Note Generation**: Input messy description, AI generates title/content/tags/date/time
- **Multilingual Translation**: Translate arbitrary content or notes
- **Batch Sorting**: Drag or specify order

### Design Elements
- **Gradient Background**: Beautiful purple gradient
- **Glassmorphism**: Semi-transparent panels, blur effect
- **Animation Effects**: Hover, transitions
- **Responsive Design**: Works on desktop/mobile
- **Modern Typography**: Clean and readable
3. Ensure all dependencies are installed
4. Check network connectivity for the deployed version

## 🎯 Future Enhancements

Potential improvements for future versions:
- User authentication and multi-user support
- Note categories and advanced tags
- Rich text formatting (bold, italic, lists)
- File attachments
- Export functionality (PDF, Markdown)
- Dark/light theme toggle
- Offline support (Service Worker)
- Note sharing capabilities

---

**Built with ❤️ using Flask, PostgreSQL, OpenAI, and modern web technologies**

