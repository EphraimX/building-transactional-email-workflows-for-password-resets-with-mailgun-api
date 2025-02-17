import os
import json
import uuid
import requests
import urllib.parse
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class loginData(BaseModel):
    username: str
    password: str


@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "message": ""})


@app.get("/passwordResetView/", response_class=HTMLResponse)
async def password_reset_view(request: Request):
    return templates.TemplateResponse(
        "passwordReset.html", {"request": request, "message": ""}
    )


@app.post("/home", response_class=HTMLResponse)
async def password_reset(
    request: Request, email_address: str = Form(...), password: str = Form(...)
):

    # Open and read the JSON DB file
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for user in users:

        if user["email_address"] == email_address and user["password"] == password:
            return templates.TemplateResponse("home.html", {"request": request})


    # If no match was found, return an error message
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "message": "Email or Password Incorrect. If you cannot remember your password, kindly reset it.",
        },
    )


@app.post("/resetPassword/")
async def reset_password(request: Request, email_address: str = Form(...)):

    # Open and read the JSON DB file
    try:
        with open("users.json", "r") as file:
            users = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        users = []

    for user in users:
        if user["email_address"] == email_address:

            email_address = user["email_address"]
            username = user["username"]
            reset_link = await generate_password_reset_link(email_address)

            response = await send_password_reset_email(
                username, email_address, reset_link
            )

            if response["success"]:

                return templates.TemplateResponse(
                    "login.html",
                    {
                        "request": request,
                        "message": "Kindly check your email to kindly reset your password",
                    },
                )

            else:

                return templates.TemplateResponse(
                    "passwordReset.html",
                    {
                        "request": request,
                        "message": "Unfortunately, we ran into an error while trying to reset your password, kindly try again. If issue persists, please contact support",
                    },
                )

    # If no match was found, return an error message
    return templates.TemplateResponse(
        "passwordReset.html",
        {
            "request": request,
            "message": "Unfortunately, we do not have record of your email, kindly reach out to the site admiinistrator.",
        },
    )


async def send_password_reset_email(username, email_address, reset_link):

    response = requests.post(
        "https://api.mailgun.net/v3/sandbox9199067bcb654265aae9ce9e308b6150.mailgun.org/messages",
        auth=("api", "key"),
        data={
            "from": "Mailgun Sandbox <postmaster@sandbox9199067bcb654265aae9ce9e308b6150.mailgun.org>",
            "to": f"{username} <{email_address}>",
            "subject": f"Hello {username}",
            "template": "test email",
            "h:X-Mailgun-Variables": json.dumps(
                {"reset_link": reset_link, "username": username}
            ),
        },
    )

    print(response)


async def send_password_reset_email(username, email_address, reset_link):

    API_KEY = os.getenv("API_KEY")  # Fetch API key from environment

    if not API_KEY:
        print("Error: API_KEY is not set!")
        return {"success": False, "error": "API key is missing"}

    try:
        response = requests.post(
            "https://api.mailgun.net/v3/sandbox9199067bcb654265aae9ce9e308b6150.mailgun.org/messages",
            auth=("api", API_KEY),
            data={
                "from": "Mailgun Sandbox <postmaster@sandbox9199067bcb654265aae9ce9e308b6150.mailgun.org>",
                "to": f"{username} <{email_address}>",
                "subject": f"Hello {username}",
                "template": "test email",
                "h:X-Mailgun-Variables": json.dumps(
                    {"reset_link": reset_link, "username": username}
                ),
            },
        )

        if response.status_code == 200:
            print(f"Password reset email sent successfully to {email_address}")
            return {"success": True, "message": "Email sent successfully"}
        else:
            print(
                f"Failed to send email. Status Code: {response.status_code}, Response: {response.text}"
            )
            return {"success": False, "error": response.text}

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {str(e)}")
        return {"success": False, "error": str(e)}


async def generate_password_reset_link(
    email_address, base_url="https://mailgunny.com/reset-password"
):
    token = uuid.uuid4()
    encoded_email = urllib.parse.quote(email_address)
    return f"{base_url}?email={encoded_email}&token={token}"


@app.post("/webhooks/password-reset")
async def handle_webhook(request: Request):
    data = await request.json()
    print(f"Password reset email clicked: {data}")
    return {"status": "received", "status_code": 200}
