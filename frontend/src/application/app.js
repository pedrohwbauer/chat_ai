// This is the scss entry file
import "../styles/index.scss";

import "@hotwired/turbo"; 
import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";
// import TextareaAutogrow from 'stimulus-textarea-autogrow'; 

window.Stimulus = Application.start();
const context = require.context("../controllers", true, /controller\.js$/);
window.Stimulus.load(definitionsFromContext(context));
// window.Stimulus.register('textarea-autogrow', TextareaAutogrow);