import { Controller } from "@hotwired/stimulus";
import { debounce } from "../utils";

export default class extends Controller {
  // @ts-ignore
  //   element;
  //   onResize;

  // maxHeightValue;
  // resizeDebounceDelayValue;

  static values = {
    resizeDebounceDelay: {
      type: Number,
      default: 100,
    },
    maxHeight: {
      type: Number,
      default: 0,
    },
  };

  initialize() {
    this.autogrow = this.autogrow.bind(this);
  }

  connect() {
    console.log(this.element);
    this.element.style.overflow = "hidden";
    const delay = this.resizeDebounceDelayValue;

    this.onResize = delay > 0 ? debounce(this.autogrow, delay) : this.autogrow;

    this.autogrow();

    this.element.addEventListener("input", this.autogrow);
    window.addEventListener("resize", this.onResize);
  }

  disconnect() {
    window.removeEventListener("resize", this.onResize);
  }

  autogrow() {
    this.element.style.height = "auto"; // Force re-print before calculating the scrollHeight value.
    console.log('maxheight', this.maxHeightValue);
    const [heightVal, overflowVal] =
      this.maxHeightValue > 0 && this.element.scrollHeight >= this.maxHeightValue
        ? [this.maxHeightValue, "scroll"]
        : [this.element.scrollHeight, "hidden"];
    this.element.style.height = `${heightVal}px`;
    this.element.style.overflow = overflowVal;
  }
}
