#!/usr/bin/env python3
"""Note generation tests removed (AI features disabled)."""
        
        try:
            # Make API request
            response = requests.post(
                f"{base_url}/api/notes/generate",
                headers={"Content-Type": "application/json"},
                json={
                    "content": test_case["content"],
                    "language": test_case["language"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                note = result.get("note", {})
                
                print("✅ Success!")
                print(f"Title: {note.get('title', 'N/A')}")
                print(f"Content: {note.get('content', 'N/A')}")
                print(f"Tags: {note.get('tags', 'N/A')}")
                print(f"Date: {note.get('event_date', 'N/A')}")
                print(f"Time: {note.get('event_time', 'N/A')}")
            else:
                print(f"❌ Failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_note_generation()