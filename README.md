Support Ticket Helper
A command-line tool that uses the Claude AI API to help support engineers respond to tickets faster and more consistently.
Built from workflows I developed while handling 35–45 support tickets per week at a SaaS company. The goal was simple: cut the time it takes to go from reading a ticket to sending a solid response, without making the response feel canned or robotic.
What it does
Three modes:
Mode	What it does
`draft`	Writes a professional, customer-facing response
`diagnose`	Lists likely root causes and troubleshooting steps
`both`	Diagnosis first, then a draft response
Requirements
```
pip install anthropic
```
You'll also need an Anthropic API key. Get one at console.anthropic.com.
Set it as an environment variable:
```
# Windows
set ANTHROPIC_API_KEY=your_key_here

# Mac/Linux
export ANTHROPIC_API_KEY=your_key_here
```
Usage
Interactive mode — paste your ticket when prompted:
```
python ticket_helper.py
```
Pass the ticket directly:
```
python ticket_helper.py --ticket "User is getting a 401 error when trying to connect their bank account"
```
Change the mode:
```
python ticket_helper.py --mode diagnose
python ticket_helper.py --mode both
```
Example output
```
=== Support Ticket Helper ===

Sending ticket to Claude (mode: both)...
--------------------------------------------------

=== Claude's Response ===

**Diagnosis**

Most likely causes in order of probability:

1. Expired or revoked OAuth token — the user may have changed their bank password
   or the bank revoked access. Evidence: check if the token refresh is also failing.
   
2. Incorrect credentials stored — user may have multiple accounts and connected
   the wrong one. Evidence: ask if they have multiple logins at this institution.

3. Bank-side MFA requirement — some institutions now require step-up auth.
   Evidence: check if the institution is on the known MFA-required list.

**Suggested response**

Hi [Name],

Thanks for reaching out. A 401 error on the bank connection usually means
the authorization between your account and the bank needs to be refreshed.

The quickest fix is to disconnect and reconnect your bank account...
```
Why I built this
I noticed that a lot of ticket response time wasn't spent thinking — it was spent on the mechanical work of translating what I already knew into clear written prose. This tool handles that part so I can focus on the cases that actually need deep investigation.
It's not meant to replace judgment. It's meant to get a solid first draft on the screen faster.
