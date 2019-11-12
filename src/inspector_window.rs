use std::rc::Rc;

use finalfusion::prelude::*;
use gtk::prelude::*;
use gtk::{ApplicationWindow, Builder, Label, MenuItem, Notebook, Widget};

use crate::similarity::SimilarityModel;
use crate::SimilarityWidget;

pub struct InspectorWindow {
    inner: ApplicationWindow,
}

impl InspectorWindow {
    pub fn new(
        application: &gtk::Application,
        embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>,
    ) -> Self {
        let glade_src = include_str!("inspector_window.glade");
        let builder = Builder::new_from_string(glade_src);

        let window: ApplicationWindow = builder
            .get_object("inspectorWindow")
            .expect("Glade source is missing inspectorWindow");
        window.set_application(Some(application));

        let mut notebook: Notebook = builder
            .get_object("notebook")
            .expect("Glade source is missing notebook");

        let similarity_model = SimilarityModel::new(embeddings);

        let similarity_widget = SimilarityWidget::new(similarity_model);
        Self::create_tab(
            &mut notebook,
            "Similarity",
            similarity_widget.widget().upcast::<Widget>(),
        );

        let quit_item: MenuItem = builder
            .get_object("quitItem")
            .expect("Glade source is missing quitItem");

        quit_item.connect_activate(clone!(window => move |_| {
            window.destroy();
        }));

        InspectorWindow { inner: window }
    }

    fn create_tab(notebook: &mut Notebook, title: &str, widget: Widget) {
        let label = Label::new(Some(title));
        notebook.append_page(&widget, Some(&label));
    }

    pub fn window(&self) -> ApplicationWindow {
        self.inner.clone()
    }
}
