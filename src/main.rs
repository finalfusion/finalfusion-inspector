use std::fs::File;
use std::io::BufReader;
use std::path::PathBuf;
use std::process;
use std::rc::Rc;

use clap::{App, AppSettings, Arg};
use finalfusion::prelude::*;
use gio::prelude::*;
use gtk::prelude::*;
use gtk::{
    ButtonsType, DialogFlags, FileChooserAction, FileChooserDialog, FileFilter, MessageDialog,
    MessageType, ResponseType, Window,
};
use stdinout::OrExit;

#[macro_use]
pub mod clone;

mod analogy_widget;
pub use analogy_widget::AnalogyWidget;

mod inspector_window;
pub use inspector_window::InspectorWindow;

mod metadata_dialog;
pub use metadata_dialog::MetadataDialog;

pub mod metadata_model;

pub mod model;

pub mod similarity_model;

mod similarity_widget;
pub use similarity_widget::SimilarityWidget;

static EMBEDDINGS: &str = "EMBEDDINGS";

static DEFAULT_CLAP_SETTINGS: &[AppSettings] = &[
    AppSettings::DontCollapseArgsInUsage,
    AppSettings::UnifiedHelpMessage,
];

fn show_error(msg: impl AsRef<str>) {
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

fn open_dialog() -> Option<PathBuf> {
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

fn open_embeddings(
    filename: Option<&str>,
) -> Result<Embeddings<VocabWrap, StorageViewWrap>, std::io::Error> {
    let filename = filename
        .map(Into::into)
        .or_else(open_dialog)
        .unwrap_or_else(|| process::exit(1));

    let file = File::open(&filename).unwrap_or_else(|err| {
        show_error(format!(
            "Cannot open {}: {}",
            filename.to_string_lossy(),
            err
        ));
        process::exit(1);
    });

    let embeddings: Embeddings<VocabWrap, StorageViewWrap> =
        Embeddings::mmap_embeddings(&mut BufReader::new(file)).unwrap_or_else(|err| {
            show_error(format!(
                "Cannot read {}: {}",
                filename.to_string_lossy(),
                err
            ));
            process::exit(1);
        });

    Ok(embeddings)
}

fn build_ui(
    application: &gtk::Application,
    embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>,
) {
    let window = InspectorWindow::new(application, embeddings);
    window.window().show_all();
}

fn main() {
    let app = App::new("finalfusion-inspector")
        .settings(DEFAULT_CLAP_SETTINGS)
        .arg(Arg::with_name(EMBEDDINGS).help("Embedding file").index(1));

    let matches = app.get_matches();

    let application =
        gtk::Application::new(Some("com.github.finalfusion.inspector"), Default::default())
            .expect("Initialization failed...");

    let embeddings =
        Rc::new(open_embeddings(matches.value_of(EMBEDDINGS)).or_exit("Cannot read embeddings", 1));

    application.connect_activate(move |app| {
        build_ui(app, embeddings.clone());
    });

    application.run(&[]);
}
