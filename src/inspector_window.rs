use gtk::prelude::*;
use gtk::{ApplicationWindow, Builder, MenuItem};

pub struct InspectorWindow {
    inner: ApplicationWindow,
}

impl InspectorWindow {
    pub fn new(application: &gtk::Application) -> Self {
        let glade_src = include_str!("inspector_window.glade");
        let builder = Builder::new_from_string(glade_src);

        let window: ApplicationWindow = builder
            .get_object("inspectorWindow")
            .expect("Glade source is missing inspectorWindow");
        window.set_application(Some(application));

        let quit_item: MenuItem = builder
            .get_object("quitItem")
            .expect("Glade source is missing quitItem");

        quit_item.connect_activate(clone!(window => move |_| {
            window.destroy();
        }));

        InspectorWindow { inner: window }
    }

    pub fn window(&self) -> ApplicationWindow {
        self.inner.clone()
    }
}
