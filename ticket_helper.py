"""
ticket_helper.py
----------------
A command-line tool that takes a support ticket description and uses the
Claude API to suggest a professional, empathetic response.

Built from real-world support workflows developed while handling 35-45 tickets
per week in a SaaS environment. Designed to help support teams respond faster
without sacrificing quality.

Usage:
    python ticket_helper.py
    python ticket_helper.py --ticket "User can't log in after password reset"
    python ticket_helper.py --mode draft     (default - writes a full response)
    python ticket_helper.py --mode diagnose  (lists likely causes and next steps)
    python ticket_helper.py --mode both      (gives diagnosis + draft response)

Requirements:
    pip install anthropic
    
    Set your API key:
    Windows:  set ANTHROPIC_API_KEY=your_key_here
    Mac/Linux: export ANTHROPIC_API_KEY=your_key_here
"""

import anthropic
import argparse
import os
import sys


SYSTEM_PROMPT = """You are an experienced SaaS technical support engineer helping a colleague respond to customer tickets.

Your job is to either:
1. Draft a professional, empathetic customer-facing response
2. Diagnose the likely root cause and suggest next steps
3. Both

Guidelines for drafting responses:
- Be clear and direct — customers don't want to wade through filler
- Acknowledge the frustration without being over-the-top about it
- Give concrete next steps, not vague suggestions
- Keep a professional but human tone — not robotic, not overly casual
- If you need more info from the customer, ask one clear question

Guidelines for diagnosis:
- List the most likely root causes in order of probability
- For each cause, note what evidence would confirm it
- Suggest specific troubleshooting steps in a logical order
- Flag if this sounds like a known bug or a pattern worth escalating

Keep responses concise and actionable."""


def get_ticket_from_user():
    """Prompt the user to paste their ticket if not provided as an argument."""
    print("\nPaste the ticket description below.")
    print("When done, press Enter twice:\n")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def build_user_prompt(ticket_text, mode):
    """Build the prompt based on the selected mode."""
    mode_instructions = {
        "draft": "Please draft a professional customer-facing response to this ticket.",
        "diagnose": "Please diagnose the likely root causes of this issue and suggest troubleshooting steps. Do not write a customer response.",
        "both": "Please first diagnose the likely root causes and troubleshooting steps, then draft a professional customer-facing response."
    }
    instruction = mode_instructions.get(mode, mode_instructions["draft"])
    return f"{instruction}\n\nTicket:\n{ticket_text}"


def call_claude(ticket_text, mode):
    """
    Send the ticket to Claude and return the response.
    
    Args:
        ticket_text (str): The support ticket content
        mode (str): 'draft', 'diagnose', or 'both'
    
    Returns:
        str: Claude's response
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\nError: ANTHROPIC_API_KEY environment variable not set.")
        print("Set it with: set ANTHROPIC_API_KEY=your_key_here  (Windows)")
        print("             export ANTHROPIC_API_KEY=your_key_here  (Mac/Linux)")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    print(f"\nSending ticket to Claude (mode: {mode})...")
    print("-" * 50)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": build_user_prompt(ticket_text, mode)}
        ]
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(
        description="AI-assisted support ticket helper powered by Claude."
    )
    parser.add_argument(
        "--ticket",
        type=str,
        help="The ticket description (if not provided, you will be prompted to paste it)"
    )
    parser.add_argument(
        "--mode",
        choices=["draft", "diagnose", "both"],
        default="draft",
        help="What you want Claude to do: draft a response, diagnose the issue, or both (default: draft)"
    )
    args = parser.parse_args()

    print("\n=== Support Ticket Helper ===")

    if args.ticket:
        ticket_text = args.ticket
    else:
        ticket_text = get_ticket_from_user()

    if not ticket_text:
        print("No ticket text provided. Exiting.")
        sys.exit(1)

    response = call_claude(ticket_text, args.mode)

    print("\n=== Claude's Response ===\n")
    print(response)
    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
