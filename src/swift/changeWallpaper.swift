#!/usr/bin/env swift

// File to change current wallpaper on macOS


import Cocoa

do {
    // get the main (currently active) screen
    if let screen = NSScreen.main {
        // get path to wallpaper file from first command line argument
        let url = URL(fileURLWithPath: CommandLine.arguments[1])
        // set the desktop wallpaper
        try NSWorkspace.shared.setDesktopImageURL(url, for: screen, options: [:])
    }
} catch {
    print(error)
}