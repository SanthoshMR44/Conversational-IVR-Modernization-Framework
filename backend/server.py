from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import random

app = FastAPI(title="Railway IVR Backend", version="3.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CallStart(BaseModel):
    caller_number: Optional[str] = "SIMULATED"

class DTMFInput(BaseModel):
    call_id: str
    digit: str

active_calls = {}
call_history = []

MENU = {
    "main": {
        "prompt": (
            "Welcome to Railway Support.\n"
            "Press 1 for Booking.\n"
            "Press 2 for Railway Status.\n"
            "Press 3 for Ticket Cancellation.\n"
            "Press 4 for Baggage.\n"
            "Press 5 for Loyalty.\n"
            "Press 6 for Feedback.\n"
            "Press 7 for Offers.\n"
            "Press 8 to schedule a callback.\n"
            "Press 9 to speak to an agent.\n"
            "Press 0 for Emergency."
        ),
        "options": {
            "1": ("goto", "booking", "Booking menu opened."),
            "2": ("goto", "status", "Railway status menu opened."),
            "3": ("goto", "cancel", "Cancellation menu opened."),
            "4": ("goto", "baggage", "Baggage menu opened."),
            "5": ("goto", "loyalty", "Loyalty menu opened."),
            "6": ("goto", "feedback", "Feedback menu."),
            "7": ("goto", "offers", "Offers menu."),
            "8": ("goto", "callback", "Callback menu."),
            "9": ("agent", None, "Connecting to agent…"),
            "0": ("end", None, "Emergency number sent via SMS.")
        }
    },

    "booking": {
        "prompt": "Press 1 for Domestic.\nPress 2 for International.\nPress 3 for Meal.\nPress * to return.",
        "options": {
            "1": ("end", None, "sleeper booking request saved."),
            "2": ("end", None, "AC Class booking saved."),
            "3": ("goto", "meal", "Meal preference menu opened."),
            "*": ("goto", "main", "Returning to main menu.")
        }
    },

    "meal": {
        "prompt": "Press 1 for Veg.\nPress 2 for Non-Veg.\nPress 3 for Jain.\nPress * to return.",
        "options": {
            "1": ("end", None, "Veg meal updated."),
            "2": ("end", None, "Non-Veg meal updated."),
            "3": ("end", None, "Jain meal updated."),
            "*": ("goto", "booking", "Returning to booking.")
        }
    },

    "status": {
        "prompt": "Enter 6-digit PNR followed by #",
        "options": {"#": ("lookup", None, "Checking PNR…")}
    },

    "cancel": {
        "prompt": "Enter 6-digit ticket number followed by #.\nPress * to return.",
        "options": {
            "#": ("cancel_lookup", None, "Checking cancellation…"),
            "*": ("goto", "main", "Returning.")
        }
    },

    "baggage": {
        "prompt": "Press 1 for Lost.\nPress 2 to Track.\nPress 3 for Damage.\nPress * to return.",
        "options": {
            "1": ("goto", "lost", "Lost baggage menu."),
            "2": ("goto", "track", "Tracking menu."),
            "3": ("end", None, "Damage complaint registered."),
            "*": ("goto", "main", "Returning.")
        }
    },

    "lost": {
        "prompt": "Enter 5-digit bag tag number followed by #.\nPress * to return.",
        "options": {
            "#": ("lost_lookup", None, "Processing lost bag…"),
            "*": ("goto", "baggage", "Returning to baggage.")
        }
    },

    "track": {
        "prompt": "Enter 4-digit complaint ID followed by #.\nPress * to return.",
        "options": {
            "#": ("track_lookup", None, "Tracking…"),
            "*": ("goto", "baggage", "Returning.")
        }
    },

    "loyalty": {
        "prompt": "Press 1 to check points.\nPress 2 to redeem.\nPress * to return.",
        "options": {
            "1": ("end", None, "You have 14,200 points."),
            "2": ("end", None, "Points redeemed successfully."),
            "*": ("goto", "main", "Returning.")
        }
    },

    "callback": {
        "prompt": "Press 1 for 15 min.\nPress 2 for 1 hour.\nPress * to return.",
        "options": {
            "1": ("end", None, "Callback scheduled in 15 min."),
            "2": ("end", None, "Callback scheduled in 1 hour."),
            "*": ("goto", "main", "Returning.")
        }
    },

    "offers": {
        "prompt": "Press 1 for Discounts.\nPress 2 for Sales.\nPress 3 for Partner Offers.\nPress * to return.",
        "options": {
            "1": ("end", None, "Discount coupons sent via SMS."),
            "2": ("end", None, "Sales details shared."),
            "3": ("end", None, "Partner offers shared."),
            "*": ("goto", "main", "Returning.")
        }
    },

    "feedback": {
        "prompt": "Rate your experience (1–4).\n* to return.",
        "options": {
            "1": ("end", None, "We will improve. Thank you."),
            "2": ("end", None, "Thanks for your rating."),
            "3": ("end", None, "Thanks for good rating."),
            "4": ("end", None, "Thanks for excellent rating!"),
            "*": ("goto", "main", "Returning.")
        }
    },
}

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/ivr/start")
def start(call: CallStart):
    call_id = f"CALL_{random.randint(100000, 999999)}"
    active_calls[call_id] = {
        "start": datetime.now(),
        "menu": "main",
        "entered": "",
        "inputs": []
    }

    return {
        "call_id": call_id,
        "prompt": MENU["main"]["prompt"],
        "status": "connected"
    }

@app.post("/ivr/dtmf")
def dtmf(payload: DTMFInput):
    if payload.call_id not in active_calls:
        raise HTTPException(404, "Call not found")

    call = active_calls[payload.call_id]
    digit = payload.digit
    menu = call["menu"]
    call["inputs"].append(digit)

    # Handle entering numbers (PNR, lost, track)
    if menu == "status" and digit not in "#":
        call["entered"] += digit
        return {"prompt": f"PNR so far: {call['entered']}"}

    if menu == "cancel" and digit not in "#*":
        call["entered"] += digit
        return {"prompt": f"Ticket no so far: {call['entered']}"}

    if menu == "lost" and digit not in "#*":
        call["entered"] += digit
        return {"prompt": f"Bag tag: {call['entered']}"}

    if menu == "track" and digit not in "#*":
        call["entered"] += digit
        return {"prompt": f"Complaint: {call['entered']}"}

    # Validate option
    if digit not in MENU[menu]["options"]:
        return {"prompt": "Invalid option. Try again."}

    action, target, msg = MENU[menu]["options"][digit]

    if action == "goto":
        call["menu"] = target
        call["entered"] = ""
        return {"prompt": MENU[target]["prompt"]}

    if action == "agent":
        return end_call(payload.call_id, "You are now connected to an agent.")

    if action == "end":
        return end_call(payload.call_id, msg)

    if action == "lookup":  
        if len(call["entered"]) == 6:
            return end_call(payload.call_id, f"PNR {call['entered']} confirmed.")
        else:
            call["entered"] = ""
            return {"prompt": "Invalid PNR. Try again."}

    if action == "cancel_lookup":
        if len(call["entered"]) == 6:
            return end_call(payload.call_id, f"Ticket {call['entered']} cancelled.")
        else:
            call["entered"] = ""
            return {"prompt": "Invalid ticket no. Try again."}

    if action == "lost_lookup":
        if len(call["entered"]) == 5:
            return end_call(payload.call_id, f"Lost bag report filed for {call['entered']}.")
        else:
            call["entered"] = ""
            return {"prompt": "Invalid bag tag."}

    if action == "track_lookup":
        if len(call["entered"]) == 4:
            return end_call(payload.call_id, f"Complaint TKT{call['entered']} is being processed.")
        else:
            call["entered"] = ""
            return {"prompt": "Invalid complaint ID."}

def end_call(call_id, msg):
    call = active_calls[call_id]
    end = datetime.now()
    duration = (end - call["start"]).seconds

    call_history.append({
        "call_id": call_id,
        "start": call["start"],
        "end": end,
        "duration": duration,
        "inputs": call["inputs"],
    })

    del active_calls[call_id]

    return {
        "status": "ended",
        "message": msg,
        "duration": f"{duration} sec"
    }
