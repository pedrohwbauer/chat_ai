import { Controller } from "@hotwired/stimulus";
import { marked } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/tomorrow-night-blue.css";

export default class extends Controller {
  static values = {
    target: String,
  };

  connect() {
    this.parse();

    this.turboFrameLoadListener = () => this.scroll();

    if (this.element.dataset.turboStream === "true") {
      // if message come from turbo stream, auto scroll smooth to bottom to display it
      this.scroll("smooth");
    } else {
      // Wait for turbo to load frame, it affects height
      document.addEventListener("turbo:frame-load", this.turboFrameLoadListener);
    }
  }

  disconnect() {
    document.removeEventListener("turbo:frame-load", this.turboFrameLoadListener);
  }

  parse() {
    const renderer = new marked.Renderer();
    renderer.code = function (code) {
      const validLanguage = hljs.getLanguage(code.lang)
        ? code.lang
        : "plaintext";

      const highlightedCode = hljs.highlight(code.text, {
        language: validLanguage,
      }).value;

      return `<pre><code class="hljs ${validLanguage}">${highlightedCode}</code></pre>`;
    };

    const html = marked.parse(this.element.dataset.content, { renderer });
    this.element.innerHTML = html;
  }

  scroll(behavior = "auto") {
    const parent = document.querySelector(`#${this.targetValue}`).parentElement;
    parent.scrollBy({ top: parent.scrollHeight, behavior: behavior });
  }
}
