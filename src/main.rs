use gio::prelude::*;
use gtk::prelude::*;

use std::env::args;

#[macro_use]
pub mod clone;

mod inspector_window;
use inspector_window::InspectorWindow;

fn build_ui(application: &gtk::Application) {
    let window = InspectorWindow::new(application);
    window.window().show_all();
}

fn main() {
    let application =
        gtk::Application::new(Some("com.github.finalfusion.inspector"), Default::default())
            .expect("Initialization failed...");

    application.connect_activate(|app| {
        build_ui(app);
    });

    application.run(&args().collect::<Vec<_>>());
}
