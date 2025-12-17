from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import xml.etree.ElementTree as ET


@dataclass
class MatchResult:
    target: str
    matched: bool
    count: int
    examples: list[str]


class UIVerifier:
    """
    Reads a UIAutomator XML dump (ui.xml) and looks for text/labels in it.

    Important note:
    If your screen is a WebView (Chrome page content), the visible page text
    often will NOT appear in ui.xml. In that case, verification should target
    non-WebView elements or you should verify via screenshot/OCR instead.
    """

    def __init__(self, ui_xml_path: Path):
        self.ui_xml_path = Path(ui_xml_path)

        if not self.ui_xml_path.exists():
            raise FileNotFoundError(f"UI XML file not found: {self.ui_xml_path}")

        self.tree = ET.parse(self.ui_xml_path)
        self.root = self.tree.getroot()

    def _node_strings(self, node: ET.Element) -> list[str]:
        """
        Collect candidate strings from a node that might contain meaningful text.
        """
        attrs_to_check = ["text", "content-desc", "resource-id", "class", "package"]
        values: list[str] = []
        for a in attrs_to_check:
            v = node.attrib.get(a, "")
            if v:
                values.append(v)
        return values

    def _all_candidates(self) -> list[str]:
        """
        Flatten all candidate strings across all nodes.
        """
        out: list[str] = []
        for node in self.root.iter():
            out.extend(self._node_strings(node))
        return out

    def find(self, target: str, case_insensitive: bool = True, partial: bool = True) -> MatchResult:
        """
        Returns whether target exists in any node attribute (text/content-desc/etc).
        """
        if not target or not target.strip():
            return MatchResult(target=target, matched=False, count=0, examples=[])

        t = target.strip()
        t_cmp = t.lower() if case_insensitive else t

        count = 0
        examples: list[str] = []

        for node in self.root.iter():
            for s in self._node_strings(node):
                s_cmp = s.lower() if case_insensitive else s
                ok = (t_cmp in s_cmp) if partial else (t_cmp == s_cmp)
                if ok:
                    count += 1
                    if len(examples) < 8:
                        examples.append(s)

        return MatchResult(target=t, matched=(count > 0), count=count, examples=examples)

    def verify_any(self, targets: list[str]) -> MatchResult:
        """
        Passes if ANY target is found.
        Returns the first successful MatchResult, or a failed one with debug.
        """
        for t in targets:
            res = self.find(t)
            if res.matched:
                return res

        # If we got here, nothing matched. Build a small debug summary.
        top_texts = self.debug_top_texts(limit=25)
        debug_examples = top_texts if top_texts else ["(No useful text found in ui.xml. This is common for WebView screens.)"]
        return MatchResult(
            target=" OR ".join(targets),
            matched=False,
            count=0,
            examples=debug_examples
        )

    def debug_top_texts(self, limit: int = 25) -> list[str]:
        """
        Returns a list of unique 'text' values found, useful for debugging.
        """
        texts = []
        seen = set()

        for node in self.root.iter():
            txt = node.attrib.get("text", "")
            if txt and txt not in seen:
                seen.add(txt)
                texts.append(txt)
            if len(texts) >= limit:
                break

        return texts
