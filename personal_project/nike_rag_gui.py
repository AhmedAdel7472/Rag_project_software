"""
Nike Football Catalog — RAG Agent GUI
Requires: pip install customtkinter langchain langchain-openai langchain-community
          langchain-chroma chromadb pymupdf langchain-huggingface sentence-transformers
Run: python nike_rag_gui.py
"""

import threading
import customtkinter as ctk
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
import re

# ── Theme ──────────────────────────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ORANGE  = "#FF4C00"
BG      = "#0a0a0a"
SURFACE = "#141414"
CARD    = "#1a1a1a"
BORDER  = "#2a2a2a"
MUTED   = "#888888"
WHITE   = "#f0f0f0"
GREEN   = "#1D9E75"

# ── Agent setup ───────────────────────────────────────────────────────────
class NikeAgent:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self._build()

    def _build(self):
        self.llm = ChatOpenAI(
            base_url=self.cfg["base_url"],
            api_key="lm-studio",
            model=self.cfg["model"],
            temperature=self.cfg["temperature"],
        )
        embeddings = HuggingFaceEmbeddings(
            model_name=self.cfg["embedding_model"]
        )
        vectorstore = Chroma(
            persist_directory=self.cfg["chroma_dir"],
            embedding_function=embeddings,
        )
        self.retriever = vectorstore.as_retriever(
            search_kwargs={"k": self.cfg["k"]}
        )
        self._make_tools()

    def _make_tools(self):
        retriever = self.retriever
        max_price = self.cfg["max_price"]

        @tool
        def nike_search(query: str) -> str:
            """Search the Nike product catalog for shirts, boots, shorts, club kits, prices."""
            docs = retriever.invoke(query)
            return "\n\n".join(d.page_content for d in docs)

        @tool
        def filter_by_price(query: str) -> str:
            """Search Nike products and return only those under the configured max price (GBP)."""
            docs = retriever.invoke(query)
            results = []
            for d in docs:
                prices = re.findall(r'£([\d.]+)', d.page_content)
                if prices and all(float(p) <= max_price for p in prices):
                    results.append(d.page_content)
            return "\n\n".join(results) if results else "No products found under that price."

        self.tools_map = {
            "nike_search": nike_search,
            "filter_by_price": filter_by_price,
        }

    def run(self, question: str, system_prompt: str) -> str:
        tools = list(self.tools_map.values())
        llm_with_tools = self.llm.bind_tools(tools)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=question),
        ]
        for _ in range(10):
            response = llm_with_tools.invoke(messages)
            messages.append(response)
            if not response.tool_calls:
                return response.content
            for tc in response.tool_calls:
                result = self.tools_map[tc["name"]].invoke(tc["args"])
                messages.append(ToolMessage(content=str(result), tool_call_id=tc["id"]))
        return "Max iterations reached."


# ── Main App ──────────────────────────────────────────────────────────────
class NikeApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Nike Football — Catalog Assistant")
        self.geometry("900x660")
        self.configure(fg_color=BG)
        self.resizable(True, True)

        self.cfg = {
            "base_url":        "http://localhost:1234/v1",
            "model":           "qwen3-4b",
            "temperature":     0.0,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "chroma_dir":      "./nike_chroma_db",
            "k":               3,
            "max_price":       100.0,
        }
        self.system_prompt = (
            "You are a Nike UK football product assistant. "
            "Use the nike_search tool to find products. "
            "Use filter_by_price when the user mentions a budget. "
            "Always mention the price in GBP in your final answer."
        )
        self.agent: NikeAgent | None = None

        self._build_ui()
        self._append_message("assistant",
            "👟  Hi! Ask me anything about Nike football kits, boots, or prices.")

    # ── Layout ────────────────────────────────────────────────────────────
    def _build_ui(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_chat()

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=0, width=240)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)
        sb.grid_columnconfigure(0, weight=1)

        # Header
        hdr = ctk.CTkFrame(sb, fg_color=CARD, corner_radius=0, height=56)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="⚙  CONFIG", font=("Helvetica", 11, "bold"),
                     text_color=MUTED).grid(row=0, column=0, padx=16, pady=16, sticky="w")

        inner = ctk.CTkScrollableFrame(sb, fg_color="transparent")
        inner.grid(row=1, column=0, sticky="nsew", padx=12, pady=8)
        sb.grid_rowconfigure(1, weight=1)
        inner.grid_columnconfigure(0, weight=1)

        row = 0

        def section(label):
            nonlocal row
            ctk.CTkLabel(inner, text=label, font=("Helvetica", 10, "bold"),
                         text_color=MUTED).grid(row=row, column=0, sticky="w",
                         padx=0, pady=(12, 4))
            row += 1

        def slider_row(label, key, from_, to, step, fmt="{:.0f}"):
            nonlocal row
            val_var = ctk.StringVar(value=fmt.format(self.cfg[key]))
            ctk.CTkLabel(inner, text=label, font=("Helvetica", 11),
                         text_color=WHITE).grid(row=row, column=0, sticky="w")
            row += 1
            val_lbl = ctk.CTkLabel(inner, textvariable=val_var,
                                   font=("Helvetica", 11), text_color=ORANGE)
            val_lbl.grid(row=row, column=0, sticky="e")

            def on_change(v, k=key, fmtstr=fmt, vv=val_var):
                self.cfg[k] = round(float(v), 4)
                vv.set(fmtstr.format(float(v)))

            s = ctk.CTkSlider(inner, from_=from_, to=to, number_of_steps=int((to-from_)/step),
                              command=on_change, button_color=ORANGE,
                              button_hover_color="#e04400",
                              progress_color=ORANGE, fg_color=BORDER)
            s.set(self.cfg[key])
            s.grid(row=row, column=0, sticky="ew", pady=(0, 4))
            row += 1

        def text_row(label, key, height=1):
            nonlocal row
            ctk.CTkLabel(inner, text=label, font=("Helvetica", 11),
                         text_color=WHITE).grid(row=row, column=0, sticky="w")
            row += 1
            if height == 1:
                e = ctk.CTkEntry(inner, font=("Courier", 11),
                                 fg_color=CARD, border_color=BORDER,
                                 text_color=WHITE)
                e.insert(0, str(self.cfg[key]))
            else:
                e = ctk.CTkTextbox(inner, font=("Courier", 10), height=height,
                                   fg_color=CARD, border_color=BORDER,
                                   text_color=WHITE)
                e.insert("0.0", self.system_prompt)
            e.grid(row=row, column=0, sticky="ew", pady=(0, 4))
            row += 1

            def on_focus_out(event, k=key, widget=e, h=height):
                val = widget.get() if h == 1 else widget.get("0.0", "end").strip()
                if k == "system_prompt":
                    self.system_prompt = val
                else:
                    self.cfg[k] = val
            e.bind("<FocusOut>", on_focus_out)

        section("LLM")
        text_row("base_url", "base_url")
        text_row("model", "model")
        slider_row("temperature", "temperature", 0, 2, 0.1, "{:.1f}")

        section("RETRIEVAL")
        text_row("chroma_dir", "chroma_dir")
        slider_row("k  (docs)", "k", 1, 10, 1)
        slider_row("max_price  £", "max_price", 10, 500, 10)

        section("EMBEDDINGS")
        text_row("model", "embedding_model")

        section("SYSTEM PROMPT")
        text_row("", "system_prompt", height=90)

        # Connect button
        ctk.CTkButton(sb, text="CONNECT", font=("Helvetica", 12, "bold"),
                      fg_color=ORANGE, hover_color="#e04400",
                      text_color="white", corner_radius=6,
                      command=self._connect_agent).grid(
            row=2, column=0, padx=12, pady=12, sticky="ew")

        self._status_var = ctk.StringVar(value="● not connected")
        ctk.CTkLabel(sb, textvariable=self._status_var,
                     font=("Helvetica", 10), text_color=MUTED).grid(
            row=3, column=0, pady=(0, 10))

    def _build_chat(self):
        chat_frame = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        chat_frame.grid(row=0, column=1, sticky="nsew")
        chat_frame.grid_rowconfigure(0, weight=1)
        chat_frame.grid_columnconfigure(0, weight=1)

        # Header
        hdr = ctk.CTkFrame(chat_frame, fg_color=SURFACE, corner_radius=0, height=56)
        hdr.grid(row=0, column=0, sticky="ew")
        hdr.grid_propagate(False)
        hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(hdr, text="NIKE FOOTBALL  ·  CATALOG ASSISTANT",
                     font=("Helvetica", 12, "bold"), text_color=WHITE).grid(
            row=0, column=0, padx=20, pady=16, sticky="w")

        # Messages
        self.chat_box = ctk.CTkTextbox(
            chat_frame,
            font=("Helvetica", 13),
            fg_color=BG,
            text_color=WHITE,
            wrap="word",
            state="disabled",
            border_width=0,
            corner_radius=0,
        )
        self.chat_box.grid(row=1, column=0, sticky="nsew")
        chat_frame.grid_rowconfigure(1, weight=1)

        self.chat_box.tag_config("user",   foreground=WHITE,  justify="right")
        self.chat_box.tag_config("ai",     foreground="#d0d0d0")
        self.chat_box.tag_config("label_user", foreground=MUTED,  justify="right")
        self.chat_box.tag_config("label_ai",   foreground=ORANGE)
        self.chat_box.tag_config("error",  foreground="#e05555")

        # Quick chips
        chips_frame = ctk.CTkFrame(chat_frame, fg_color=BG, corner_radius=0)
        chips_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(4, 0))
        chips = [
            "Arsenal kits", "Boots under £80",
            "Goalkeeper gloves", "Training gear under £50",
        ]
        for c in chips:
            ctk.CTkButton(chips_frame, text=c, font=("Helvetica", 11),
                          fg_color=CARD, hover_color=BORDER,
                          text_color=MUTED, border_color=BORDER,
                          border_width=1, corner_radius=20, height=28,
                          command=lambda q=c: self._send(q)).pack(
                side="left", padx=4, pady=6)

        # Input row
        input_row = ctk.CTkFrame(chat_frame, fg_color=SURFACE, corner_radius=0, height=60)
        input_row.grid(row=3, column=0, sticky="ew")
        input_row.grid_propagate(False)
        input_row.grid_columnconfigure(0, weight=1)

        self.input_entry = ctk.CTkEntry(
            input_row,
            placeholder_text="Ask about kits, boots, prices...",
            font=("Helvetica", 13),
            fg_color=CARD,
            border_color=BORDER,
            text_color=WHITE,
            height=40,
            corner_radius=20,
        )
        self.input_entry.grid(row=0, column=0, padx=(12, 8), pady=10, sticky="ew")
        self.input_entry.bind("<Return>", lambda e: self._send())

        self.send_btn = ctk.CTkButton(
            input_row, text="▶", width=44, height=40,
            fg_color=ORANGE, hover_color="#e04400",
            text_color="white", corner_radius=20,
            font=("Helvetica", 14, "bold"),
            command=self._send,
        )
        self.send_btn.grid(row=0, column=1, padx=(0, 12), pady=10)

    # ── Actions ───────────────────────────────────────────────────────────
    def _connect_agent(self):
        self._status_var.set("⟳  connecting...")
        def connect():
            try:
                self.agent = NikeAgent(self.cfg)
                self.after(0, lambda: self._status_var.set("● connected"))
                self.after(0, lambda: self._append_message(
                    "assistant", "✅  Connected to local model. Ready to search the catalog!"))
            except Exception as e:
                self.after(0, lambda: self._status_var.set("✗  error"))
                self.after(0, lambda: self._append_message("error", f"Connection failed: {e}"))
        threading.Thread(target=connect, daemon=True).start()

    def _send(self, text: str = ""):
        if not text:
            text = self.input_entry.get().strip()
        if not text:
            return
        self.input_entry.delete(0, "end")
        self._append_message("user", text)

        if self.agent is None:
            self._append_message("error",
                "⚠  Not connected. Click CONNECT in the sidebar first.")
            return

        self.send_btn.configure(state="disabled", text="…")
        self._append_message("assistant", "thinking...")
        query = text

        def run():
            try:
                reply = self.agent.run(query, self.system_prompt)
            except Exception as e:
                reply = f"Error: {e}"
            self.after(0, lambda: self._replace_last_thinking(reply))
            self.after(0, lambda: self.send_btn.configure(state="normal", text="▶"))

        threading.Thread(target=run, daemon=True).start()

    def _append_message(self, role: str, text: str):
        self.chat_box.configure(state="normal")
        if role == "user":
            self.chat_box.insert("end", "\nYOU\n", "label_user")
            self.chat_box.insert("end", f"{text}\n", "user")
        elif role == "assistant":
            self.chat_box.insert("end", "\nNIKE ASSISTANT\n", "label_ai")
            self.chat_box.insert("end", f"{text}\n", "ai")
        elif role == "error":
            self.chat_box.insert("end", f"\n{text}\n", "error")
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")

    def _replace_last_thinking(self, new_text: str):
        self.chat_box.configure(state="normal")
        content = self.chat_box.get("1.0", "end")
        if "thinking..." in content:
            idx = content.rfind("thinking...")
            line_num = content[:idx].count("\n") + 1
            self.chat_box.delete(f"{line_num}.0", f"{line_num}.end")
            self.chat_box.insert(f"{line_num}.0", new_text)
        self.chat_box.configure(state="disabled")
        self.chat_box.see("end")


if __name__ == "__main__":
    app = NikeApp()
    app.mainloop()