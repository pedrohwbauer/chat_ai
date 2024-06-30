import { Controller } from "@hotwired/stimulus";

export default class extends Controller {

  connect() {
    const url = this.element.dataset.url;
    this.source = new WebSocket(
      (location.protocol === "https:" ? "wss" : "ws") +
        "://" +
        window.location.host +
        url
    );
    window.Turbo.connectStreamSource(this.source);
  }

  disconnect() {
    if (this.source) {
      window.Turbo.disconnectStreamSource(this.source);
      this.source.close();
      this.source = null;
    }
  }
}
