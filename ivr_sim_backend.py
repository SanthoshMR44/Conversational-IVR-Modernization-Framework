# ivr_simulator_backend.py
# Complete IVR Backend WITHOUT needing ACS/Twilio account

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import random

app = FastAPI(title="IVR Simulator Backend", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class CallStart(BaseModel):
    caller_number: str
    call_id: Optional[str] = None

class DTMFInput(BaseModel):
    call_id: str
    digit: str
    current_menu: str

class CallLog(BaseModel):
    call_id: str
    caller_number: str
    start_time: str
    end_time: Optional[str] = None
    duration: Optional[int] = None
    menu_path: List[str] = []
    inputs: List[str] = []

# ==================== IN-MEMORY STORAGE ====================

# Active calls
active_calls = {}

# Call history
call_history = []

# Menu definitions
MENU_STRUCTURE = {
    "main": {
        "prompt": "Welcome to Indian Railways Booking Agent. Press 1 for Ticket Booking. Press 2 for Train Status. Press 3 for Refund Enquiry. Press 9 to speak with an agent.",
        "options": {
            "1": {"action": "goto_menu", "target": "booking", "message": "You selected Ticket Booking."},
            "2": {"action": "goto_menu", "target": "train_status", "message": "You selected Train Status."},
            "3": {"action": "goto_menu", "target": "refund", "message": "You selected Refund Enquiry."},
            "9": {"action": "transfer_agent", "message": "Connecting you to a railway customer care executive."}
        }
    },
    "booking": {
        "prompt": "Press 1 for Sleeper Class Booking. Press 2 for AC Class Booking. Press 0 to return to Main Menu.",
        "options": {
            "1": {"action": "end_call", "message": "Sleeper class booking selected. Our agent will contact you shortly."},
            "2": {"action": "end_call", "message": "AC class booking selected. Please visit irctc.co.in to proceed."},
            "0": {"action": "goto_menu", "target": "main", "message": "Returning to Main Menu."}
        }
    },
    "train_status": {
        "prompt": "Please enter your 10-digit PNR number followed by hash.",
        "options": {
            "#": {"action": "lookup_pnr", "message": "Checking your train status..."}
        }
    },
    "refund": {
        "prompt": "Press 1 for Cancelled Train Refund. Press 2 for Tatkal Refund. Press 0 to return to Main Menu.",
        "options": {
            "1": {"action": "end_call", "message": "Refund for cancelled train will be processed in 3–5 days."},
            "2": {"action": "end_call", "message": "Tatkal refund request registered. Visit irctc.co.in for details."},
            "0": {"action": "goto_menu", "target": "main", "message": "Returning to Main Menu."}
        }
    }
}


# ==================== ENDPOINTS ====================

@app.get("/")
def root():
    """Health check"""
    return {
        "status": "IVR Simulator Running",
        "active_calls": len(active_calls),
        "total_calls": len(call_history)
    }

@app.post("/ivr/start")
def start_call(call_data: CallStart):
    """
    Simulate incoming call
    
    This would be triggered by ACS/Twilio in real system
    Here we simulate it with web interface
    """
    
    call_id = f"CALL_{random.randint(100000, 999999)}"
    
    # Create call session
    active_calls[call_id] = {
        "call_id": call_id,
        "caller_number": call_data.caller_number,
        "start_time": datetime.now().isoformat(),
        "current_menu": "main",
        "menu_path": ["main"],
        "inputs": [],
        "pnr_buffer": ""
    }
    
    print(f"\n📞 NEW CALL: {call_id} from {call_data.caller_number}")
    
    # Return welcome message
    return {
        "call_id": call_id,
        "status": "connected",
        "prompt": MENU_STRUCTURE["main"]["prompt"]
    }

@app.post("/ivr/dtmf")
def handle_dtmf(input_data: DTMFInput):
    """
    Process DTMF key press
    
    This is the core IVR logic - same as ACS/Twilio would do
    """
    
    call_id = input_data.call_id
    digit = input_data.digit
    
    # Check if call exists
    if call_id not in active_calls:
        raise HTTPException(status_code=404, detail="Call not found")
    
    call = active_calls[call_id]
    current_menu = call["current_menu"]
    
    # Log input
    call["inputs"].append(digit)
    
    print(f"\n🔢 DTMF INPUT: Call {call_id}, Menu: {current_menu}, Digit: {digit}")
    
    # Get menu definition
    menu = MENU_STRUCTURE.get(current_menu)
    if not menu:
        return {"error": "Invalid menu state"}
    
    # Special handling for PNR input
    if current_menu == "flight_status" and digit != "#":
        call["pnr_buffer"] += digit
        if len(call["pnr_buffer"]) < 6:
            return {
                "status": "collecting",
                "prompt": f"You entered {digit}. Continue entering PNR.",
                "collected": call["pnr_buffer"]
            }
    
    # Check if digit is valid option
    if digit not in menu["options"]:
        return {
            "status": "invalid",
            "prompt": "Invalid option. Please try again.",
            "current_menu": current_menu,
            "valid_options": list(menu["options"].keys())
        }
    
    # Get action for this option
    option = menu["options"][digit]
    action = option["action"]
    message = option["message"]
    
    response = {
        "status": "processed",
        "message": message
    }
    
    # Execute action
    if action == "goto_menu":
        target_menu = option["target"]
        call["current_menu"] = target_menu
        call["menu_path"].append(target_menu)
        response["current_menu"] = target_menu
        response["prompt"] = MENU_STRUCTURE[target_menu]["prompt"]
        
    elif action == "end_call":
        response["status"] = "call_ended"
        response["call_action"] = "hangup"
        # Move call to history
        call["end_time"] = datetime.now().isoformat()
        call_history.append(call.copy())
        del active_calls[call_id]
        
    elif action == "transfer_agent":
        response["status"] = "transferring"
        response["call_action"] = "transfer"
        call["end_time"] = datetime.now().isoformat()
        call_history.append(call.copy())
        del active_calls[call_id]
        
    elif action == "lookup_pnr":
        pnr = call["pnr_buffer"]
        if len(pnr) == 6:
            # Mock PNR lookup
            response["status"] = "pnr_found"
            response["pnr_info"] = {
                "pnr": pnr,
                "flight": "AI101",
                "status": "Confirmed",
                "route": "Mumbai to Delhi"
            }
            response["message"] = f"Your PNR {pnr} is confirmed. Flight AI101 from Mumbai to Delhi."
            response["call_action"] = "hangup"
            call["end_time"] = datetime.now().isoformat()
            call_history.append(call.copy())
            del active_calls[call_id]
        else:
            response["status"] = "invalid_pnr"
            response["message"] = "Invalid PNR. Please try again."
            call["pnr_buffer"] = ""
    
    print(f"✅ ACTION: {action} - {message}")
    
    return response

@app.post("/ivr/end")
def end_call(call_id: str):
    """End call (user hung up)"""