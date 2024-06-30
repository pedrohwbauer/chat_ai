// This is the scss entry file
import "../styles/index.scss";

import { Application } from "@hotwired/stimulus";
import websocketController from "../controllers/websocket_controller";

import "@hotwired/turbo"; 
window.Stimulus = Application.start();
window.Stimulus.register("websocket", websocketController);

window.document.addEventListener("DOMContentLoaded", function () {
  window.console.log("dom ready");
});