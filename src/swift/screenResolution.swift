#!/usr/bin/env swift


// Function to get current resolution of the main display on macOS


import Cocoa


// get the main (currently active) screen
if let screen = NSScreen.main {
    // get resolution of screen
    let screenFrame = screen.frame
    // return resolution
    print(screenFrame)
    }
