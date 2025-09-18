#!/usr/bin/env python3
"""
Simple Test Game Server for MYNFINI
Tests the complete beginner experience
"""

from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)
app.secret_key = 'test-secret-key'

@app.route('/')
def game_homepage():
    """Main game interface - designed for absolute beginners"""
    return '''
<!DOCTYPE html>
<html><head><title>[DICE] MYNFINI Adventure Game</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 50px;
    margin: 0;
    min-height: 100vh;
}
.game-container {
    background: white;
    color: #333;
    border-radius: 25px;
    padding: 40px;
    max-width: 800px;
    margin: 0 auto;
    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
}
h1 { color: #4CAF50; font-size: 42px; }
.subtitle { color: #666; font-size: 20px; margin: 20px 0; }
.start-btn {
    background: linear-gradient(135deg, #4CAF50, #45a049);
    color: white;
    border: none;
    padding: 20px 40px;
    font-size: 24px;
    border-radius: 25px;
    cursor: pointer;
    animation: pulse 2s infinite;
    margin: 20px;
}
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
.game-screen {
    background: #f8f9fa;
    border-radius: 15px;
    padding: 30px;
    margin: 20px 0;
    text-align: left;
}
.story-text { font-size: 18px; line-height: 1.6; margin-bottom: 20px; }
.choice-btn {
    background: #007bff;
    color: white;
    border: none;
    padding: 15px 25px;
    margin: 10px;
    border-radius: 15px;
    font-size: 16px;
    cursor: pointer;
    transition: background 0.3s ease;
}
.choice-btn:hover { background: #0056b3; }
</style></head><body>
    <div class="game-container">
        <h1>[DICE] Your Adventure Awaits!</h1>
        <p class="subtitle">Welcome to your magical storytelling journey where YOU create the story! [STAR]</p>

        <div id="welcome">
            <p>Ready to start your amazing adventure? Just click the big green button below!</p>
            <button class="start-btn" onclick="startAdventure()">[ROCKET] Let's Start the Magic!</button>
        </div>

        <div id="game" style="display:none;">
            <div class="game-screen">
                <div class="story-text" id="story-text">
                    You wake up in a mysterious tavern with a sword at your side and a map in your pocket. The bartender mentions a legendary treasure hidden in the Crystal Mountains...
                </div>
                <h3>What do you want to do?</h3>
                <button class="choice-btn" onclick="makeChoice(1)">Head to the Crystal Mountains</button>
                <button class="choice-btn" onclick="makeChoice(2)">Talk to the bartender for more information</button>
                <button class="choice-btn" onclick="makeChoice(3)">Explore the village first</button>
            </div>
        </div>

        <div style="margin-top: 30px; font-size: 14px; color: #666;">
            [CHECK] Game Connected Successfully!<br>
            <em>Created for absolute beginners - just click and play!</em>
        </div>
    </div>

    <script>
        function startAdventure() {
            document.getElementById('welcome').style.display = 'none';
            document.getElementById('game').style.display = 'block';
        }

        function makeChoice(choice) {
            const stories = {
                1: "The Crystal Mountains are dangerous but rewarding. After hours of climbing, you discover an ancient cave entrance...",
                2: "The bartender tells you the treasure requires three magical keys. He offers to show you the location of the first key in exchange for helping him clean up.",
                3: "The village has a mysterious old magician who offers to teach you a magical spell that will help you navigate the Crystal Mountains safely."
            };
            document.getElementById('story-text').textContent = stories[choice];
        }
    </script>
</body></html>
    '''

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "game": "running"})

if __name__ == '__main__':
    print("[DICE] Starting MYNFINI Adventure Game on port 5000...")
    print("[ROCKET] Open your browser to: http://localhost:5000")
    print("[STAR] Your magical adventure awaits!")
    app.run(debug=True, port=5000, host='0.0.0.0')