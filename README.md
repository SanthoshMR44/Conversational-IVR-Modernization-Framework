📞 IVR Simulation System – Indian Railways (Frontend + Backend)
🧩 Project Overview
This project simulates a complete Interactive Voice Response (IVR) system — similar to what users experience when calling customer care services (like IRCTC or Airlines).
It integrates a FastAPI backend for call logic and a modern HTML/CSS/JS frontend that visually represents a phone dialer.

🖥️ Technologies Used
Component	Technology
Frontend	HTML5, CSS3, JavaScript (Vanilla JS)
Backend	Python (FastAPI Framework)
Runtime	Uvicorn (ASGI server)
Integration	REST API (JSON over HTTP)

⚙️ Features
•	🎛️ Interactive IVR keypad interface
•	🗣️ Dynamic voice prompts and simulated speaking animation
•	🔢 DTMF input handling (key press events)
•	🔁 Menu navigation (Main, Booking, Train Status, Refund)
•	💾 Call logging (Start, End, Duration, Status)
•	🌐 Backend-Frontend integration using HTTP requests
•	🚫 Works without Twilio or external services

🧠 IVR Menu Structure
Main Menu:
1.	Ticket Booking
2.	Train Status
3.	Refund Enquiry
4.	Speak to Agent
Submenus:
•	Booking Menu: Sleeper / AC Class booking options
•	Refund Menu: Cancelled Train / Tatkal refund options
•	PNR Lookup: Enter 10-digit PNR (mock simulated)

🛠️ Setup & Run Instructions
1️⃣ Backend Setup (FastAPI)
1.	Install required packages:
2.	pip install fastapi uvicorn
3.	Run the server:
4.	uvicorn ivr_sim_backend:app --reload
5.	Server starts at:
6.	http://127.0.0.1:8000

2️⃣ Frontend Setup (HTML/JS)
1.	Open the file ivr_web_sim.html in your browser.
(Preferably using “Open with Live Server” in VS Code)
2.	Click “Start Call” to initiate IVR simulation.
3.	Press numeric keys to navigate menus.
4.	Observe live call status, voice prompts, and logs.

🧾 Project Files
File	Description
ivr_sim_backend.py	FastAPI backend simulating IVR call logic, routes, and menus
ivr_web_sim.html	Frontend web-based IVR simulator (dialer interface)

🧩 API Endpoints Summary
Endpoint	Method	Description
/	GET	Health check
/ivr/start	POST	Starts a simulated call
/ivr/dtmf	POST	Handles DTMF key press input
/ivr/end	POST	Ends a call session

🧪 Example Flow
1️⃣ User clicks Start Call → Backend sends welcome message
2️⃣ User presses 1 → Navigates to Booking Menu
3️⃣ User presses 2 → AC Class Booking message → Call ends
4️⃣ Call summary logged in history

🏁 Outcome
•	Demonstrates end-to-end client-server communication
•	Models real-world telecom IVR behavior
•	Uses clean UI and modern API-driven logic
•	Perfect for showcasing internship-ready technical skills
