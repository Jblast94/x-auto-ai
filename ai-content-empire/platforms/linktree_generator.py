import os
import json
from string import Template

class LinktreeGenerator:
    def __init__(self, character_name: str):
        self.character_name = character_name.lower()
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.bibles_dir = os.path.join(self.project_root, 'content', 'character_bibles')
        self.output_dir = os.path.join(self.project_root, 'platforms', 'static_sites', self.character_name)
    
    def load_character_data(self) -> dict:
        char_file = os.path.join(self.bibles_dir, f"{self.character_name}.json")
        try:
            with open(char_file, 'r') as f:
                return json.load(f).get('character', {})
        except FileNotFoundError:
            return {"name": self.character_name.capitalize(), "style": "neutral"}
            
    def generate_html(self, affiliate_links: dict = None):
        """Generates the HTML file"""
        char_data = self.load_character_data()
        name = char_data.get('name', self.character_name).capitalize()
        style = char_data.get('style', 'neutral')
        
        # Select theme colors based on style
        themes = {
            "flirty": {"bg": "#ffb6c1", "btn": "#ff69b4", "text": "#fff"},
            "professional": {"bg": "#f0f2f5", "btn": "#0077b5", "text": "#fff"},
            "tech": {"bg": "#0d1117", "btn": "#2ea043", "text": "#fff"},
            "fitness": {"bg": "#222", "btn": "#ff4500", "text": "#fff"},
            "neutral": {"bg": "#fafafa", "btn": "#333", "text": "#fff"}
        }
        theme = themes.get(style, themes["neutral"])
        
        # Default links if none provided
        if not affiliate_links:
            affiliate_links = [
                {"title": "My X (Twitter)", "url": f"https://x.com/{self.character_name}_ai"},
                {"title": "Exclusive Content 🔒", "url": f"https://onlyfans.com/{self.character_name}"},
                {"title": "TikTok", "url": f"https://tiktok.com/@{self.character_name}_clips"},
            ]
        
        links_html = ""
        for link in affiliate_links:
            links_html += f'<a href="{link["url"]}" class="link-btn" target="_blank">{link["title"]}</a>\n'

        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{name}'s Links</title>
            <style>
                body {{
                    font-family: 'Inter', sans-serif;
                    background-color: {theme['bg']};
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 50px 20px;
                    margin: 0;
                    color: #333;
                }}
                .profile-pic {{
                    width: 120px;
                    height: 120px;
                    border-radius: 50%;
                    background-color: #ddd;
                    margin-bottom: 20px;
                    border: 3px solid {theme['btn']};
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 40px;
                    overflow: hidden;
                }}
                .name {{
                    font-size: 24px;
                    font-weight: bold;
                    margin-bottom: 30px;
                    color: {"#fff" if style in ['tech', 'fitness'] else "#333"};
                }}
                .links-container {{
                    display: flex;
                    flex-direction: column;
                    width: 100%;
                    max-width: 400px;
                    gap: 15px;
                }}
                .link-btn {{
                    background-color: {theme['btn']};
                    color: {theme['text']};
                    padding: 15px 20px;
                    border-radius: 30px;
                    text-decoration: none;
                    text-align: center;
                    font-weight: 600;
                    font-size: 16px;
                    transition: transform 0.2s, opacity 0.2s;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }}
                .link-btn:hover {{
                    transform: translateY(-2px);
                    opacity: 0.9;
                }}
            </style>
            <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
        </head>
        <body>
            <div class="profile-pic">🤖</div>
            <div class="name">@{name}</div>
            <div class="links-container">
                {links_html}
            </div>
            <p style="margin-top: 40px; font-size: 12px; color: #888;">Powered by ACE Platform</p>
        </body>
        </html>
        """
        
        os.makedirs(self.output_dir, exist_ok=True)
        output_file = os.path.join(self.output_dir, 'index.html')
        with open(output_file, 'w') as f:
            f.write(html_template)
            
        return output_file

if __name__ == "__main__":
    # Test generation for a default character
    gen = LinktreeGenerator("luna")
    output = gen.generate_html()
    print(f"Generated Linktree clone for Luna at: {output}")
