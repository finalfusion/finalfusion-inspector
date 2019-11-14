use std::rc::Rc;

use gtk::prelude::*;
use gtk::{Box, Builder, Button, Entry, IconSize, Image, TreeView};

use crate::embeddings_ext::{EmbeddingsExt, WordStatus};
use crate::models::{EmbeddingsModel, SimilarityModel};

pub struct SimilarityWidget {
    button: Button,
    entry: Entry,
    inner: Box,
    model: Rc<SimilarityModel>,
    status_image: Image,
}

impl SimilarityWidget {
    pub fn new(model: SimilarityModel) -> Rc<Self> {
        let model = Rc::new(model);

        let glade_src = include_str!("similarity_widget.glade");
        let builder = Builder::new_from_string(glade_src);

        let widget: Box = builder
            .get_object("similarityWidget")
            .expect("Glade source is missing similarityWidget");

        let view: TreeView = builder
            .get_object("similarityView")
            .expect("Glade source is missing similarityView");
        view.set_model(Some(&model.model()));

        let entry: Entry = builder
            .get_object("queryEntry")
            .expect("Glade source is missing queryEntry");

        let button: Button = builder
            .get_object("queryButton")
            .expect("Glade source is missing queryButton");

        let status_image: Image = builder
            .get_object("statusImage")
            .expect("Glade source is missing statusImage");

        let widget = Rc::new(SimilarityWidget {
            button: button.clone(),
            entry: entry.clone(),
            inner: widget,
            model: model.clone(),
            status_image,
        });

        widget
            .entry
            .connect_changed(clone!(widget => move |_| widget.update_validity()));

        entry.connect_activate(clone!(entry, model, widget => move |_| {
            if model.embeddings().word_status(&widget.query()).is_valid() {
        model.similarity(&entry.get_buffer().get_text());
            }
        }));

        button.connect_clicked(
            clone!(entry, model => move |_| model.similarity(&entry.get_buffer().get_text())),
        );

        widget.update_validity();

        widget
    }

    fn query(&self) -> String {
        self.entry.get_buffer().get_text()
    }

    fn update_validity(&self) {
        let status = self.model.embeddings().word_status(&self.query());
        self.button.set_sensitive(status.is_valid());

        let icon_name = match status {
            WordStatus::Known => "face-angel-symbolic",
            WordStatus::Subword => "face-smile-symbolic",
            WordStatus::Unknown => "face-crying-symbolic",
        };

        self.status_image
            .set_from_icon_name(Some(icon_name), IconSize::LargeToolbar);
    }

    pub fn widget(&self) -> Box {
        self.inner.clone()
    }
}
