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

    if (this.element.dataset.turboStream === "true") {
      // if message come from turbo stream, auto scroll to bottom to display it
      this.scroll();
    }
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
    console.log(this.element.dataset.content);
    const html = marked.parse(this.element.dataset.content, { renderer });
    this.element.innerHTML = html;
  }

  scroll() {
    const target = document.querySelector(`#${this.targetValue}`);
    console.log(target.parentElement.scrollHeight);
    target.parentElement.scrollTop = target.parentElement.scrollHeight;
  }
}
