use std::rc::Rc;

use gtk::prelude::*;
use gtk::{Builder, Dialog, TreeView};

use crate::metadata_model::MetadataModel;

pub struct MetadataDialog {
    inner: Dialog,
}

impl MetadataDialog {
    pub fn new(model: MetadataModel) -> Rc<Self> {
        let glade_src = include_str!("metadata_dialog.glade");
        let builder = Builder::new_from_string(glade_src);

        let dialog: Dialog = builder
            .get_object("metadataDialog")
            .expect("Glade source is missing metadataDialog");

        let metadata_view: TreeView = builder
            .get_object("metadataView")
            .expect("Glade source is missing metadataView");

        metadata_view.set_model(Some(&model.model()));

        Rc::new(MetadataDialog { inner: dialog })
    }

    pub fn dialog(&self) -> Dialog {
        self.inner.clone()
    }
}
