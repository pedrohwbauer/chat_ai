// This is the scss entry file
import "../styles/index.scss";

import { Application } from "@hotwired/stimulus";
import { definitionsFromContext } from "@hotwired/stimulus-webpack-helpers";

import "@hotwired/turbo"; 
window.Stimulus = Application.start();
const context = require.context("../controllers", true, /\.js$/);
window.Stimulus.load(definitionsFromContext(context));
