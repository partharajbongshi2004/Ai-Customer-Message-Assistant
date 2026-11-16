"""
app.py
Interactive Command-Line Interface (CLI) for testing the AI Customer Message Assistant.
"""

import sys
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from assistant import CustomerSupportAssistant

console = Console()


def print_welcome_banner() -> None:
    """Displays startup instructions and available CLI commands."""
    banner_text = (
        "[bold cyan]AI Customer Message Assistant[/bold cyan]\n"
        "Supports [bold green]English[/bold green] & [bold green]Bengali (বাংলা)[/bold green] "
        "with multi-turn memory.\n\n"
        "[dim]Commands:[/dim]\n"
        "  [yellow]/reset[/yellow]  - Clear chat history and start a new customer session\n"
        "  [yellow]/help[/yellow]   - Show sample test prompts\n"
        "  [yellow]/exit[/yellow]   - Quit the application"
    )
    console.print(Panel(banner_text, border_style="cyan", expand=False))


def print_sample_prompts() -> None:
    """Displays sample queries in both languages to test memory and knowledge grounding."""
    samples = (
        "[bold]Try these test conversations:[/bold]\n"
        "1. [cyan]English Inquiry:[/cyan] Hi! How much is the Nakshi Kantha throw, and do you ship to Chittagong?\n"
        "2. [cyan]Memory Follow-up:[/cyan] Great, if I buy two of those, do I qualify for free delivery?\n"
        "3. [cyan]Bengali Inquiry:[/cyan] আপনাদের সুন্দরবনের মধুর দাম কত এবং রিটার্ন পলিসি কী?\n"
        "4. [cyan]Banglish Inquiry:[/cyan] Terracotta tea set ta ki stock e ache?"
    )
    console.print(Panel(samples, border_style="green", expand=False))


def main() -> None:
    """Main interactive chat loop."""
    load_dotenv()  # Load GEMINI_API_KEY from .env file if present

    try:
        assistant = CustomerSupportAssistant(model_name="gemini-2.5-flash")
    except ValueError as config_err:
        console.print(f"[bold red]Startup Error:[/bold red] {config_err}")
        sys.exit(1)

    print_welcome_banner()

    while True:
        try:
            user_input = console.input("\n[bold blue]Customer > [/bold blue]").strip()

            if not user_input:
                continue

            command = user_input.lower()
            if command in ("/exit", "exit", "quit"):
                console.print("[dim]Ending session. Goodbye![/dim]")
                break

            if command == "/reset":
                assistant.reset_conversation()
                console.print("[yellow]Conversation memory cleared. New session started.[/yellow]")
                continue

            if command == "/help":
                print_sample_prompts()
                continue

            with console.status("[bold green]Assistant is typing...[/bold green]", spinner="dots"):
                reply = assistant.send_message(user_input)

            console.print("\n[bold green]Agent >[/bold green]")
            console.print(Panel(Markdown(reply), border_style="green"))

        except KeyboardInterrupt:
            console.print("\n[dim]Session interrupted. Goodbye![/dim]")
            break


if __name__ == "__main__":
    main()
