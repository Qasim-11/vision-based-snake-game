# Hand-Controlled Snake Game 🐍🖐️

Control a simple snake game using just your index finger and a webcam. This project tracks hand movement through your webcam and uses that to steer the snake. Apples randomly appear — eat them to grow longer, but don’t hit yourself or the wall!

---

## 🎮 Features

- Real-time hand tracking with your webcam
- Snake follows your index finger
- Apples increase snake length and speed
- Collision detection with walls and self
- No need for a keyboard — just wave your hand!

---

## 📦 Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- NumPy

Install dependencies:

```bash
pip install opencv-python mediapipe numpy
```

---

## 📁 File Structure

```
├── hand.py               # Tracks hand and fingers using MediaPipe
├── snake_game.py         # Main game code. Simply make this 2 in the same directory
```

---

## 🚀 How to Play

```bash
python snake_game.py
```

- Make sure your webcam is connected
- Move your **index finger** to guide the snake
- Press `Q` to quit

---

## 🕹 Gameplay Tips

- Eat apples to grow
- The more you eat, the faster the snake is and the larger it is. So be careful
- Don’t crash into yourself or the wall
- Keep moving — inactivity for 20 seconds ends the game

---

## 🔧 Ideas for Improvements

- Add gestures to pause or use power-ups
- Add score saving or leaderboard
- Play sound effects
- Try multiplayer with both hands

---

## 🙌 Credits

- [MediaPipe](https://google.github.io/mediapipe/) for hand tracking
- [OpenCV](https://opencv.org/) for webcam and graphics

---

## 🎥 Demo

Check out a quick preview of the game in action:
[▶️ Watch the demo](Demo/Snake-Game-Demo.mp4)
---

Have fun! PRs and feature suggestions are welcome.
