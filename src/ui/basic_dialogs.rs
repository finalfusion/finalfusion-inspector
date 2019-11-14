use std::path::PathBuf;

use gtk::prelude::*;
use gtk::{
    ButtonsType, DialogFlags, FileChooserAction, FileChooserDialog, FileFilter, MessageDialog,
    MessageType, ResponseType, Window,
};

pub fn open_embeddings() -> Option<PathBuf> {
    let dialog = FileChooserDialog::with_buttons::<Window>(
        Some("Open File"),
        None,
        FileChooserAction::Open,
        &[
            ("_Cancel", ResponseType::Cancel),
            ("_Open", ResponseType::Accept),
        ],
    );

    let filter = FileFilter::new();
    filter.set_name(Some("finalfusion embeddings"));
    filter.add_pattern("*.fifu");

    dialog.add_filter(&filter);

    let response = dialog.run();

    let filename = match response {
        ResponseType::Accept => dialog.get_filename(),
        ResponseType::Cancel => None,
        ResponseType::DeleteEvent => None,
        _ => unreachable!(),
    };

    dialog.destroy();

    filename
}

pub fn show_error(msg: impl AsRef<str>) {
    let dialog = MessageDialog::new::<Window>(
        None,
        DialogFlags::empty(),
        MessageType::Error,
        ButtonsType::Ok,
        msg.as_ref(),
    );

    dialog.run();
    dialog.destroy();
}
