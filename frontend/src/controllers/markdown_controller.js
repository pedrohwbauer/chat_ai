import { Controller } from "@hotwired/stimulus";
import { marked } from "marked";
import hljs from "highlight.js";
import "highlight.js/styles/tomorrow-night-blue.css";

export default class extends Controller {
  connect() {
    this.parse();
  }

  parse() {
    const renderer = new marked.Renderer();
    renderer.code = function (code) {
      console.log("code", code);
      const validLanguage = hljs.getLanguage(code.lang)
        ? code.lang
        : "plaintext";
      console.log("language", validLanguage);
      console.log("1");
      const highlightedCode = hljs.highlight(code.text, {
        language: validLanguage,
      }).value;
      console.log("2");
      return `<pre><code class="hljs ${validLanguage}">${highlightedCode}</code></pre>`;
    };
    console.log(this.element.dataset.content);
    const html = marked.parse(this.element.dataset.content, { renderer });
    this.element.innerHTML = html;
  }
}
