use std::rc::Rc;

use gtk::prelude::*;
use gtk::{
    Box, Builder, Button, Entry, IconSize, Image, SortColumn, SortType, TreeModelSort, TreeView,
};

use crate::embeddings_ext::WordStatus;
use crate::models::{EmbeddingsModel, SubwordsModel};
use crate::ui::EmbeddingsWidget;

pub struct SubwordsWidget {
    button: Button,
    entry: Entry,
    inner: Box,
    model: Rc<SubwordsModel>,
    status_image: Image,
}

impl SubwordsWidget {
    pub fn new(model: SubwordsModel) -> Rc<Self> {
        let model = Rc::new(model);

        let glade_src = include_str!("subwords_widget.glade");
        let builder = Builder::new_from_string(glade_src);

        let widget: Box = builder
            .get_object("subwordsWidget")
            .expect("Glade source is missing subwordsWidget");

        let view: TreeView = builder
            .get_object("subwordsView")
            .expect("Glade source is missing subwordsView");

        let sortable_model = TreeModelSort::new(&model.model());
        sortable_model.set_sort_column_id(SortColumn::Index(1), SortType::Ascending);
        view.set_model(Some(&sortable_model));

        let entry: Entry = builder
            .get_object("queryEntry")
            .expect("Glade source is missing queryEntry");

        let button: Button = builder
            .get_object("queryButton")
            .expect("Glade source is missing queryButton");

        let status_image: Image = builder
            .get_object("statusImage")
            .expect("Glade source is missing statusImage");

        let widget = Rc::new(SubwordsWidget {
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
            if model.word_status(&widget.query()).is_valid() {
        model.subwords(&entry.get_buffer().get_text());
            }
        }));

        button.connect_clicked(
            clone!(entry, model => move |_| model.subwords(&entry.get_buffer().get_text())),
        );

        widget.update_validity();

        widget
    }

    fn query(&self) -> String {
        self.entry.get_buffer().get_text()
    }

    pub fn widget(&self) -> Box {
        self.inner.clone()
    }
}

impl EmbeddingsWidget for SubwordsWidget {
    fn model(&self) -> &dyn EmbeddingsModel {
        &*self.model
    }

    fn update_validity(&self) {
        let status = self.model.word_status(&self.query());
        self.button.set_sensitive(status.is_valid());

        let icon_name = match status {
            WordStatus::Known => "face-angel-symbolic",
            WordStatus::Subword => "face-smile-symbolic",
            WordStatus::Unknown => "face-crying-symbolic",
        };

        self.status_image
            .set_from_icon_name(Some(icon_name), IconSize::LargeToolbar);
    }
}
