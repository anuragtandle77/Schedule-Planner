import json
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import datetime
from typing  import Literal 


# This is the messy syllabus data your script needs to clean up
load_dotenv()


class Deadline(BaseModel):
    event_name: str = Field(description="The name of the assignment, quiz, or exam.")
    date: str = Field(description="The standardized date of the event in YYYY-MM-DD format.")
    time: str = Field(description="The 24-hour time of the event in HH:MM format. Default to 00:00 if no time is mentioned.")
    category: Literal["Exam", "quiz", "Assignment"] = Field(description="The category of the event, which can be either  Exam, quiz, or Assignment")

    priority: Literal["High", "Medium", "Low"] = Field(description="The priority level of the event, which can be either High, Medium.")
    is_tentative: bool = Field(description="A boolean indicating whether the date is tentative or fixed.(If the date is tentative then it should be true otherwise false.)")
    notes: str = Field(description="If the date is tentative, provide a brief explanation of why it's tentative. If the date is fixed, this field can be left empty.")

class ScheduleContainer(BaseModel):
    deadlines: list[Deadline] = Field(description="A list of all extracted deadlines from the text.")

MESSY_SYLLABUS = """
Alright team, here is the roadmap. 
Homework 1 is definitely due on 2026-06-08. No exceptions.
We will tentatively hold the First Quiz on 2026-06-12, but that might change depending on room availability.
The Final Project presentation is locked in for 2026-06-25 in the main auditorium.
"""
api_key = os.environ.get("GEMINI_API_KEY")


def extract_deadlines(raw_text: str):

    client = genai.Client(api_key=api_key)
    MODEL = "gemini-3.1-flash-lite"
    now = datetime.datetime.now()
    current_date = now.strftime('%Y-%m-%d') 

    

    prompt = """Extract the deadlines and assignments from the provided text payload 
        and format them according to the required schema structure. Also, filter out background noise(like general information or non-evalute events)."""

    response = client.models.generate_content(
    model=MODEL,
    contents=[
        raw_text, 
        prompt
    ],
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=ScheduleContainer, # <-- This forces Gemini to follow your Pydantic model structure!
        system_instruction=f"""You are a strict data formatting assistant. Extract the events, absolute dates, and times. Ensure dates strictly use YYYY-MM-DD and assume the year is 2026 unless specified otherwise and categorize, prioritize the data based on the schema structure. You also have to determine if the date is tentative or fixed and provide notes if it's tentative based on the schema structure.

        IMPORTANT CONTEXT: TODAY'S DATE IS {current_date}.
        If relative date expressions are used like ("two weeks from today", "next Friday", "three days after that"),calculate the exact calendar absolute date using {current_date} as your starting point.
        
         """,
    )
    )
    print(response.text)
    


print('Extracting deadlines from the syllabus...')
extract_deadlines(MESSY_SYLLABUS)
