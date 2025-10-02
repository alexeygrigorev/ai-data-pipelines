"""
Interactive search utilities for creating question-based search interfaces.
"""

import random
from typing import List, Dict, Any
from abc import ABC, abstractmethod

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from common.display import display_results_with_navigation


class InteractiveSearch(ABC):
    """Base class for interactive search applications."""
    
    def __init__(
        self, 
        app_title: str,
        app_description: str, 
        sample_questions: List[str],
        console: Console = None
    ):
        """Initialize the interactive search application.
        
        Args:
            app_title: The title of the application
            app_description: Description of what the app does
            sample_questions: List of sample questions to show users
            console: Rich console for output (optional)
        """
        self.app_title = app_title
        self.app_description = app_description
        self.sample_questions = sample_questions
        self.console = console or Console()
        self.index = None
    
    @abstractmethod
    def load_data(self) -> Any:
        """Load and return the search index/data. Must be implemented by subclasses."""
        pass
    
    @abstractmethod
    def search(self, query: str) -> List[Dict[str, Any]]:
        """Perform search and return results. Must be implemented by subclasses."""
        pass
    
    def display_results(self, results: List[Dict[str, Any]], query: str) -> None:
        """Display search results. Can be overridden by subclasses."""
        display_results_with_navigation(results, query, self.console)
    
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
            default=random_question
        ).strip()
        
        return user_question if user_question else random_question
    
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

        self.console.print("\n[bold blue]Goodbye! 👋[/bold blue]")
    
    def run(self) -> None:
        """Main entry point to run the interactive search application."""
        self.show_welcome()
        
        if self.initialize():
            self.run_search_loop()