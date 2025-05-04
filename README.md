# Building Transactional Email Workflows for Password Resets with Mailgun API

This repository provides an instructional guide and code for setting up transactional email workflows using the [Mailgun API](https://www.mailgun.com/). The example workflow focuses on sending password reset emails to users.

## Features:
- **Password Reset Flow:** A complete flow for resetting passwords, including email verification.
- **Mailgun Integration:** Uses Mailgun's API for sending emails.
- **HTML Email Templates:** Includes an HTML template for the password reset email.

## Getting Started:
1. Clone this repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Mailgun account and configure your API key.
4. Run the app:
   ```bash
   python main.py
   ```

## Files:
- `main.py`: Python script for handling the email sending logic.
- `email_template.html`: Template for the reset password email.
- `users.json`: Sample user data for the email workflow.
- `requirements.txt`: Python dependencies.

## 📄 Reference Article

Here's an article providing detailed steps on how to build this:

🔗 [How to Build Transactional Password Reset Email Workflows](https://www.mailgun.com/blog/dev-life/how-to-build-transactional-password-reset-email-workflows/)

## Contributions:
Feel free to fork the repo and submit issues or pull requests.
