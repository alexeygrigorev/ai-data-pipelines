import frontmatter
import random
import os
import sys
from typing import List, Dict, Any

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich.progress import track


from github_docs.github import GithubRepositoryDataReader, RawRepositoryFile
from common.indexing import index_documents

console = Console()

# Pre-defined sample questions
SAMPLE_QUESTIONS = [
    "How do I run Postgres locally?",
    "How to install Docker?",
    "What are the system requirements?", 
    "How to set up the environment?",
    "How to troubleshoot installation issues?",
    "Where can I find course materials?",
    "How to submit homework?",
    "How to connect to database?"
]


def read_github_data(repo_owner: str, repo_name: str) -> List[RawRepositoryFile]:
    """Download repository data with progress indication."""
    allowed_extensions = {"md", "mdx"}

    def only_de_zoomcamp(filepath: str) -> bool:
        return "/data-engineering-zoomcamp" in filepath

    console.print("📥 [bold blue]Downloading repository data...[/bold blue]")
    
    reader = GithubRepositoryDataReader(
        repo_owner,
        repo_name,
        allowed_extensions=allowed_extensions,
        filename_filter=only_de_zoomcamp,
    )
    
    return reader.read()


def parse_data(data_raw: List[RawRepositoryFile]) -> List[Dict[str, Any]]:
    """Parse raw files with progress tracking."""
    console.print("📄 [bold blue]Parsing documents...[/bold blue]")
    
    data_parsed = []
    for f in track(data_raw, description="Processing files..."):
        post = frontmatter.loads(f.content)
        data = post.to_dict()
        data['filename'] = f.filename
        data_parsed.append(data)

    return data_parsed


def index_faq_data():
    """Load and index FAQ data."""
    repo_owner = "DataTalksClub"
    repo_name = "faq"

    with console.status("[bold green]Setting up FAQ search system..."):
        data_raw = read_github_data(repo_owner, repo_name)
        documents = parse_data(data_raw)

        console.print("🔍 [bold blue]Creating search index...[/bold blue]")
        index = index_documents(
            documents,
            chunk=True,
            chunking_params={"size": 2000, "step": 1000},
        )

    return index, len(documents)


def get_random_question() -> str:
    """Get a random sample question."""
    return random.choice(SAMPLE_QUESTIONS)





class LessPager:
    """A simple less-like pager for displaying content."""
    
    def __init__(self, content_lines: List[str], console: Console):
        self.lines = content_lines
        self.console = console
        self.current_line = 0
        self.terminal_height = console.size.height - 3  # Leave space for status line
        self._last_displayed_content = None
    

    
    def display_page(self, force_refresh=False):
        """Display the current page of content."""
        # Calculate what should be displayed
        end_line = min(self.current_line + self.terminal_height, len(self.lines))
        
        # Create content hash to check if redraw is needed
        current_content = (self.current_line, end_line)
        
        # Only redraw if content actually changed or forced
        if self._last_displayed_content != current_content or force_refresh:
            # Clear screen first
            self.console.clear()
            
            # Display the main content lines as plain text
            for i in range(self.current_line, end_line):
                if i < len(self.lines):
                    line = self.lines[i]
                    # Display all content as plain text for clean, simple output like real less
                    self.console.print(line, highlight=False, markup=False)
            
            # Add status line
            percentage = int((end_line / len(self.lines)) * 100) if self.lines else 100
            status = f":{percentage}% ({end_line}/{len(self.lines)}) Press 'q'/Ctrl+C to quit, ↑↓/j/k to scroll, Space for next page"
            self.console.print(f"\n[dim]{status}[/dim]")
            
            # Remember what we displayed
            self._last_displayed_content = current_content
    
    def run(self):
        """Run the pager with keyboard navigation."""
        try:
            import msvcrt  # Windows-specific
            
            # Initial display with full refresh
            self.display_page(force_refresh=True)
            
            while True:
                # Wait for keypress
                try:
                    key = msvcrt.getch()
                except KeyboardInterrupt:
                    # Handle Ctrl+C
                    break
                
                old_line = self.current_line
                
                if key == b'q' or key == b'Q':  # Quit
                    break
                elif key == b'\x03':  # Ctrl+C
                    break
                elif key == b' ':  # Space - next page
                    self.current_line = min(
                        self.current_line + self.terminal_height, 
                        max(0, len(self.lines) - self.terminal_height)
                    )
                elif key == b'\r' or key == b'\n':  # Enter - next line
                    if self.current_line < len(self.lines) - self.terminal_height:
                        self.current_line += 1
                elif key == b'j':  # j - down (vim-style)
                    if self.current_line < len(self.lines) - self.terminal_height:
                        self.current_line += 1
                elif key == b'k':  # k - up (vim-style)
                    self.current_line = max(0, self.current_line - 1)
                elif key == b'\x00' or key == b'\xe0':  # Special keys prefix (both variants)
                    try:
                        special_key = msvcrt.getch()
                        if special_key == b'H':  # Up arrow
                            self.current_line = max(0, self.current_line - 1)
                        elif special_key == b'P':  # Down arrow
                            if self.current_line < len(self.lines) - self.terminal_height:
                                self.current_line += 1
                        elif special_key == b'I':  # Page Up
                            self.current_line = max(0, self.current_line - self.terminal_height)
                        elif special_key == b'Q':  # Page Down
                            self.current_line = min(
                                self.current_line + self.terminal_height,
                                max(0, len(self.lines) - self.terminal_height)
                            )
                    except KeyboardInterrupt:
                        break
                
                # Only redraw if position changed
                if self.current_line != old_line:
                    self.display_page()
        
        except (ImportError, KeyboardInterrupt):
            # Fallback for non-Windows systems or if msvcrt not available, or Ctrl+C
            if not hasattr(self, '_fallback_shown'):
                self.console.print("[yellow]⚠️  Arrow key navigation not available on this system.[/yellow]")
                self.console.print("Showing all content at once:\n")
                for line in self.lines:
                    self.console.print(line)
        
        self.console.clear()


def display_results_with_navigation(results: List[Dict[str, Any]], query: str):
    """Display search results in a less-like scrollable view."""
    if not results:
        console.print("[bold red]❌ No results found![/bold red]")
        return

    # Build the complete content as lines
    content_lines = []
    content_lines.append(f"🔍 Found {len(results)} results for: {query}")
    content_lines.append("")
    
    for i, result in enumerate(results, 1):
        content = result.get('content', 'No content available')
        filename = result.get('filename', 'Unknown')
        
        # Add result header
        content_lines.append(f"{i}. {filename}")
        content_lines.append("")
        
        # Add content lines
        content_lines.extend(content.split('\n'))
        content_lines.append("")
        content_lines.append("─" * 80)
        content_lines.append("")
    
    # Create and run the pager
    pager = LessPager(content_lines, console)
    pager.run()


def get_user_question() -> str:
    """Get question from user with pre-filled random sample question."""
    # Get a random sample question
    random_question = get_random_question()
    
    console.print("\n[dim]💡 Sample question:[/dim]")
    console.print(f"[cyan]{random_question}[/cyan]")
    console.print("[dim]Press Enter to use it, or type your own question (Ctrl+C to exit)[/dim]")
    
    # Prompt with pre-filled random question  
    user_question = Prompt.ask(
        "❓ [bold white]Question[/bold white]",
        default=random_question
    ).strip()
    
    return user_question if user_question else random_question

def main():
    """Main interactive FAQ search application."""
    # Welcome message
    welcome_panel = Panel(
        Text.assemble(
            ("🚀 ", "bold blue"),
            ("DataTalks Club FAQ Search", "bold white"),
            ("\n\nInteractive search through DataTalks Club FAQ documents", "dim"),
        ),
        title="Welcome",
        title_align="center",
        border_style="bright_blue",
        padding=(1, 2)
    )
    console.print(welcome_panel)
    
    # Load and index data
    try:
        index, doc_count = index_faq_data()
        
        success_panel = Panel(
            f"[green]✅ Successfully indexed {doc_count} documents![/green]\n"
            f"[dim]Ready to answer your questions...[/dim]",
            border_style="green"
        )
        console.print(success_panel)
        
    except Exception as e:
        console.print(f"[bold red]❌ Error loading data: {e}[/bold red]")
        return

    # Interactive Q&A loop
    while True:
        try:
            console.print("\n" + "="*80 + "\n")
            
            # Get user question
            question = get_user_question()
            
            console.print(f"\n[bold yellow]🔍 Searching for:[/bold yellow] [italic]{question}[/italic]")
            
            # Search and display results
            with console.status("[bold green]Searching..."):
                results = index.search(question)
            
            display_results_with_navigation(results, question)
            
            # Ask if user wants to continue
            console.print("\n" + "─" * 50)
            if not Confirm.ask("[bold]Ask another question?[/bold]", default=True):
                break
                
        except KeyboardInterrupt:
            console.print("\n[yellow]👋 Thanks for using FAQ Search![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]❌ Error: {e}[/red]")

    console.print("\n[bold blue]Goodbye! 👋[/bold blue]")


if __name__ == "__main__":
    main()