"""
Display utilities for creating less-like pagers and interactive content viewers.
"""

from typing import List, Dict, Any

from rich.console import Console


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


def display_results_with_navigation(results: List[Dict[str, Any]], query: str, console: Console):
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