use std::rc::Rc;

use gtk::prelude::*;
use gtk::{Box, Builder, Button, Entry, IconSize, Image, TreeView};

use crate::model::{EmbeddingsExt, EmbeddingsModel, WordStatus};
use crate::similarity_model::SimilarityModel;

struct AnalogyEntry {
    entry: Entry,
    status: Image,
}

pub struct AnalogyWidget {
    button: Button,
    inner: Box,
    model: Rc<SimilarityModel>,
    entries: [AnalogyEntry; 3],
}

impl AnalogyWidget {
    pub fn new(model: SimilarityModel) -> Rc<Self> {
        let model = Rc::new(model);

        let glade_src = include_str!("analogy_widget.glade");
        let builder = Builder::new_from_string(glade_src);

        let widget: Box = builder
            .get_object("analogyWidget")
            .expect("Glade source is missing analogyWidget");

        let view: TreeView = builder
            .get_object("analogyView")
            .expect("Glade source is missing analogyView");
        view.set_model(Some(&model.model()));

        let entries = Self::create_entries(&builder);

        let button: Button = builder
            .get_object("queryButton")
            .expect("Glade source is missing queryButton");

        let widget = Rc::new(AnalogyWidget {
            button: button.clone(),
            inner: widget,
            model: model.clone(),
            entries,
        });

        for entry in &widget.entries {
            entry
                .entry
                .connect_changed(clone!(widget => move |_| widget.update_validity()));

            entry
                .entry
                .connect_activate(clone!(model, widget => move |_| {
                    if widget.all_valid() {
                model.analogy(widget.query());
                    }
                }));
        }

        button.connect_clicked(clone!(model, widget => move |_| model.analogy(widget.query())));

        widget.update_validity();

        widget
    }

    fn create_entries(builder: &Builder) -> [AnalogyEntry; 3] {
        let entry1: Entry = builder
            .get_object("analogy1Entry")
            .expect("Glade source is missing analogy1Entry");
        let status1: Image = builder
            .get_object("analogy1Status")
            .expect("Glade source is missing analogy1Status");

        let entry2: Entry = builder
            .get_object("analogy2Entry")
            .expect("Glade source is missing analogy2Entry");
        let status2: Image = builder
            .get_object("analogy2Status")
            .expect("Glade source is missing analogy2Status");

        let entry3: Entry = builder
            .get_object("analogy3Entry")
            .expect("Glade source is missing analogy3Entry");
        let status3: Image = builder
            .get_object("analogy3Status")
            .expect("Glade source is missing analogy3Status");

        [
            AnalogyEntry {
                entry: entry1,
                status: status1,
            },
            AnalogyEntry {
                entry: entry2,
                status: status2,
            },
            AnalogyEntry {
                entry: entry3,
                status: status3,
            },
        ]
    }

    fn all_valid(&self) -> bool {
        self.entries.iter().all(|e| {
            let query = e.entry.get_buffer().get_text();
            self.model.embeddings().word_status(&query).is_valid()
        })
    }

    fn query(&self) -> [String; 3] {
        [
            self.entries[0].entry.get_buffer().get_text(),
            self.entries[1].entry.get_buffer().get_text(),
            self.entries[2].entry.get_buffer().get_text(),
        ]
    }

    fn update_validity(&self) {
        for entry in &self.entries {
            let query = entry.entry.get_buffer().get_text();

            let status = self.model.embeddings().word_status(&query);
            self.button.set_sensitive(status.is_valid());

            let icon_name = match status {
                WordStatus::Known => "face-angel-symbolic",
                WordStatus::Subword => "face-smile-symbolic",
                WordStatus::Unknown => "face-crying-symbolic",
            };

            entry
                .status
                .set_from_icon_name(Some(icon_name), IconSize::LargeToolbar);
        }
    }

    pub fn widget(&self) -> Box {
        self.inner.clone()
    }
}
