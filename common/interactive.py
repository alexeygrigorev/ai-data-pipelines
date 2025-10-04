"""
Interactive search utilities for creating question-based search interfaces.
"""

import random
import traceback
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.markdown import Markdown


def getch():
    """Cross-platform getch function."""
    import sys
    
    if sys.platform == "win32":
        import msvcrt
        return msvcrt.getch()
    else:
        import termios
        import tty
        
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            key = sys.stdin.read(1)
            return key.encode('utf-8')
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)



def display_results_with_navigation(
        results: List[Dict[str, Any]],
        query: str,
        console: Console,
        content_field: str = 'content',
        filename_field: str = 'filename',
):
    """Display search results one at a time with navigation."""
    if not results:
        console.print("[bold red]❌ No results found![/bold red]")
        return
    
    current_result = 0
    total_results = len(results)
    
    while current_result < total_results:
        # Clear screen
        console.clear()
        
        # Show header
        console.print(f"[bold blue]🔍 Found {total_results} results for:[/bold blue] [italic]{query}[/italic]\n")
        
        # Get current result
        result = results[current_result]
        content = result.get(content_field, 'No content available')
        filename = result.get(filename_field, 'Unknown')

        # Show result number and filename
        console.print(f"[bold green]Result {current_result + 1}/{total_results}: {filename}[/bold green]")
        console.print()
        
        # Render content as markdown
        try:
            md = Markdown(content)
            console.print(md)
        except Exception:
            # Fallback to plain text
            console.print(content)
        
        # Show navigation prompt
        console.print("\n" + "─" * 80)
        if current_result < total_results - 1:
            console.print("[dim]Press SPACE for next result, 'q' to quit[/dim]")
        else:
            console.print("[dim]End of results - press 'q' to quit[/dim]")
        
        # Wait for user input
        try:
            while True:
                key = getch()
                
                if key == b'q' or key == b'Q':  # Quit
                    console.clear()
                    return
                elif key == b'\x03':  # Ctrl+C
                    console.clear()
                    return
                elif key == b' ':  # Space - next result
                    if current_result < total_results - 1:
                        current_result += 1
                        break
                    else:
                        # At end, quit
                        console.clear()
                        return
        
        except (ImportError, KeyboardInterrupt):
            # Fallback for non-Windows systems or Ctrl+C
            console.print("[yellow]Navigation not available - showing all results[/yellow]")
            for i, result in enumerate(results, 1):
                content = result.get('content', 'No content available')
                filename = result.get('filename', 'Unknown')
                console.print(f"\n[bold green]{i}. {filename}[/bold green]")
                try:
                    md = Markdown(content)
                    console.print(md)
                except Exception:
                    console.print(content)
                console.print("\n" + "─" * 80)
            return


class InteractiveSearch(ABC):
    """Base class for interactive search applications."""
    
    def __init__(
        self, 
        app_title: str,
        app_description: str, 
        sample_questions: List[str],
        console: Console = None,
        content_field: str = 'content',
        filename_field: str = 'filename',
    ):
        """Initialize the interactive search application.
        
        Args:
            app_title: The title of the application
            app_description: Description of what the app does
            sample_questions: List of sample questions to show users
            console: Rich console for output (optional)
            content_field: The field name in results that contains the main content to display
            filename_field: The field name in results that contains the filename or title
        """
        self.app_title = app_title
        self.app_description = app_description
        self.sample_questions = sample_questions
        self.console = console or Console()
        self.index = None
        self.content_field = content_field
        self.filename_field = filename_field

    @abstractmethod
    def load_data(self) -> Any:
        """Load and return the search index/data. Must be implemented by subclasses."""
        pass

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Perform search and return results."""
        return self.index.search(query)
    
    def display_results(self, results: List[Dict[str, Any]], query: str) -> None:
        """Display search results. Can be overridden by subclasses."""
        display_results_with_navigation(
            results,
            query,
            self.console,
            content_field=self.content_field,
            filename_field=self.filename_field
        )

    def get_random_question(self) -> str:
        """Get a random sample question."""
        return random.choice(self.sample_questions)
    
    def get_user_question(self) -> str:
        """Get question from user with pre-filled random sample question."""
        random_question = self.get_random_question()
        
        self.console.print("\n[dim]💡 Sample question:[/dim]")
        self.console.print(f"[cyan]{random_question}[/cyan]")
        self.console.print("[dim]Press Enter to use it, or type your own question (Ctrl+C to exit)[/dim]")
        
        user_question = Prompt.ask(
            "❓ [bold white]Question[/bold white]",
        ).strip()
        
        if user_question:
            return user_question
        return random_question


    def show_welcome(self) -> None:
        """Display welcome message."""
        welcome_panel = Panel(
            Text.assemble(
                ("🚀 ", "bold blue"),
                (self.app_title, "bold white"),
                (f"\n\n{self.app_description}", "dim"),
            ),
            title="Welcome",
            title_align="center",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.console.print(welcome_panel)
    
    def initialize(self) -> bool:
        """Load data and show success message. Returns True if successful."""
        try:
            self.index = self.load_data()

            success_panel = Panel(
                "[green]✅ Successfully loaded data![/green]\n"
                "[dim]Ready to answer your questions...[/dim]",
                border_style="green"
            )
            self.console.print(success_panel)
            return True

        except Exception as e:
            self.console.print(f"[bold red]❌ Error loading data: {e}[/bold red]")
            traceback.print_exc()
            return False
    
    def run_search_loop(self) -> None:
        """Run the main interactive search loop."""
        while True:
            try:
                self.console.print("\n" + "="*80 + "\n")
                
                # Get user question
                question = self.get_user_question()
                
                self.console.print(f"\n[bold yellow]🔍 Searching for:[/bold yellow] [italic]{question}[/italic]")
                
                # Search and display results
                with self.console.status("[bold green]Searching..."):
                    results = self.search(question)
                
                self.display_results(results, question)
                
                # Ask if user wants to continue
                self.console.print("\n" + "─" * 50)
                if not Confirm.ask("[bold]Ask another question?[/bold]", default=True):
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]👋 Thanks for using the search![/yellow]")
                break
            except Exception as e:
                self.console.print(f"[red]❌ Error: {e}[/red]")
                traceback.print_exc()

        self.console.print("\n[bold blue]Goodbye! 👋[/bold blue]")
    
    def run(self) -> None:
        """Main entry point to run the interactive search application."""
        self.show_welcome()
        
        if self.initialize():
            self.run_search_loop()