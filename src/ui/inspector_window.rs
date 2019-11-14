use std::fs::File;
use std::io::BufReader;
use std::rc::Rc;

use finalfusion::prelude::*;
use gtk::prelude::*;
use gtk::{ApplicationWindow, Builder, Label, MenuItem, Notebook, Widget};

use crate::models::{MetadataModel, SimilarityModel, SubwordsModel};
use crate::ui::{
    open_embeddings, show_error, AnalogyWidget, EmbeddingsWidget, MetadataDialog, SimilarityWidget,
    SubwordsWidget,
};

pub struct InspectorWindow {
    inner: ApplicationWindow,
    widgets: Vec<Rc<dyn EmbeddingsWidget>>,
}

impl InspectorWindow {
    pub fn new(
        application: &gtk::Application,
        embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>,
    ) -> Rc<Self> {
        let glade_src = include_str!("inspector_window.glade");
        let builder = Builder::new_from_string(glade_src);

        let window: ApplicationWindow = builder
            .get_object("inspectorWindow")
            .expect("Glade source is missing inspectorWindow");
        window.set_application(Some(application));

        let mut notebook: Notebook = builder
            .get_object("notebook")
            .expect("Glade source is missing notebook");

        let similarity_widget = SimilarityWidget::new(SimilarityModel::new(embeddings.clone()));
        Self::create_tab(
            &mut notebook,
            "Similarity",
            similarity_widget.widget().upcast::<Widget>(),
        );

        let analogy_widget = AnalogyWidget::new(SimilarityModel::new(embeddings.clone()));
        Self::create_tab(
            &mut notebook,
            "Analogy",
            analogy_widget.widget().upcast::<Widget>(),
        );

        let subwords_widget = SubwordsWidget::new(SubwordsModel::new(embeddings.clone()));
        Self::create_tab(
            &mut notebook,
            "Subwords",
            subwords_widget.widget().upcast::<Widget>(),
        );

        let metadata_dialog = MetadataDialog::new(MetadataModel::new(embeddings));
        metadata_dialog.dialog().set_transient_for(Some(&window));
        metadata_dialog.dialog().connect_delete_event(|dialog, _| {
            dialog.hide();
            Inhibit(true)
        });

        let inspector_window = Rc::new(InspectorWindow {
            inner: window.clone(),
            widgets: vec![
                similarity_widget.clone(),
                analogy_widget.clone(),
                subwords_widget.clone(),
                metadata_dialog.clone(),
            ],
        });

        let metadata_item: MenuItem = builder
            .get_object("metadataItem")
            .expect("Glade source is missing metadataItem");
        metadata_item.connect_activate(move |_| {
            metadata_dialog.dialog().run();
            metadata_dialog.dialog().hide();
        });

        let open_item: MenuItem = builder
            .get_object("openItem")
            .expect("Glade source is missing openItem");
        open_item.connect_activate(clone!(inspector_window => move |_| {
            inspector_window.open_embeddings();
        }));

        let quit_item: MenuItem = builder
            .get_object("quitItem")
            .expect("Glade source is missing quitItem");

        quit_item.connect_activate(move |_| {
            window.destroy();
        });

        inspector_window
    }

    fn create_tab(notebook: &mut Notebook, title: &str, widget: Widget) {
        let label = Label::new(Some(title));
        notebook.append_page(&widget, Some(&label));
    }

    fn open_embeddings(&self) {
        let filename = match open_embeddings() {
            Some(filename) => filename,
            None => return,
        };

        let file = match File::open(&filename) {
            Ok(file) => file,
            Err(err) => {
                show_error(format!(
                    "Cannot open {}: {}",
                    filename.to_string_lossy(),
                    err
                ));
                return;
            }
        };

        let embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>> =
            match Embeddings::mmap_embeddings(&mut BufReader::new(file)) {
                Ok(embeddings) => Rc::new(embeddings),
                Err(err) => {
                    show_error(format!(
                        "Cannot read {}: {}",
                        filename.to_string_lossy(),
                        err
                    ));
                    return;
                }
            };

        for widget in &self.widgets {
            widget.model().switch_embeddings(embeddings.clone());
            widget.update_validity();
        }
    }

    pub fn window(&self) -> ApplicationWindow {
        self.inner.clone()
    }
}
