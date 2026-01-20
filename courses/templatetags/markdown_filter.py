# courses/markdown_extensions.py
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

class KatexPreprocessor(Preprocessor):
    # Matches $$...$$ (display) and $...$ (inline), but not \$ escaped
    DISPLAY_MATH_RE = re.compile(r'^\s*\$\$\s*(.*?)\s*\$\$', re.DOTALL)
    INLINE_MATH_RE = re.compile(r'(?<!\\)\$(?!\$)(.+?)(?<!\\)\$', re.DOTALL)

    def run(self, lines):
        new_lines = []
        in_display = False
        display_buffer = []

        for line in lines:
            # Handle display math ($$...$$) across multiple lines
            if self.DISPLAY_MATH_RE.match(line):
                if in_display:
                    # End previous block
                    new_lines.append(self._render_katex(''.join(display_buffer).strip(), display=True))
                    display_buffer = []
                    in_display = False
                else:
                    in_display = True
                    display_buffer = [line]
                continue
            elif in_display:
                display_buffer.append(line)
                if self.DISPLAY_MATH_RE.match(line):
                    new_lines.append(self._render_katex(''.join(display_buffer).strip(), display=True))
                    display_buffer = []
                    in_display = False
                continue

            # Handle inline math
            line = self.INLINE_MATH_RE.sub(lambda m: self._render_katex(m.group(1), display=False), line)
            new_lines.append(line)

        if in_display:
            new_lines.append(self._render_katex(''.join(display_buffer).strip(), display=True))

        return new_lines

    def _render_katex(self, latex, display):
        style = 'display: block; text-align: center;' if display else 'display: inline-block;'
        return f'<div class="katex-eq" style="{style}"><script type="math/tex; mode={"display" if display else "inline"}">{latex}</script></div>'

class KatexExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(KatexPreprocessor(md), 'katex', 25)


# courses/markdown_extensions.py
from markdown.extensions import Extension
import markdown

class KatexExtension(Extension):
    def extendMarkdown(self, md):
        # Add KaTeX support (example using delimiters $$...$$ and \(...\))
        md.inlinePatterns.register(
            markdown.inlinepatterns.SimpleTagPattern(r'(\$\$)(.*?)\1', 'katex'),
            'katex-block', 200
        )
        md.inlinePatterns.register(
            markdown.inlinepatterns.SimpleTagPattern(r'(\\\()(.+?)\\\)', 'katex'),
            'katex-inline', 190
        )

def makeExtension(**kwargs):
    return KatexExtension(**kwargs)