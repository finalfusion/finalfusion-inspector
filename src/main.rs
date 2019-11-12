use std::fs::File;
use std::io::BufReader;
use std::rc::Rc;

use clap::{App, AppSettings, Arg};
use finalfusion::prelude::*;
use gio::prelude::*;
use gtk::prelude::*;
use stdinout::OrExit;

#[macro_use]
pub mod clone;

mod inspector_window;
pub use inspector_window::InspectorWindow;

pub mod model;

pub mod similarity;

mod similarity_widget;
pub use similarity_widget::SimilarityWidget;

static EMBEDDINGS: &str = "EMBEDDINGS";

static DEFAULT_CLAP_SETTINGS: &[AppSettings] = &[
    AppSettings::DontCollapseArgsInUsage,
    AppSettings::UnifiedHelpMessage,
];

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
        .arg(
            Arg::with_name(EMBEDDINGS)
                .help("Embedding file")
                .index(1)
                .required(true),
        );

    let matches = app.get_matches();
    let embeddings_filename = matches.value_of(EMBEDDINGS).unwrap();

    let application =
        gtk::Application::new(Some("com.github.finalfusion.inspector"), Default::default())
            .expect("Initialization failed...");

    let mut read = BufReader::new(File::open(embeddings_filename).or_exit(
        format!("Cannot read embeddings from {}", embeddings_filename),
        1,
    ));
    let embeddings: Embeddings<VocabWrap, StorageViewWrap> = Embeddings::mmap_embeddings(&mut read)
        .or_exit(
            format!("Cannot read embeddings from {}", embeddings_filename),
            1,
        );
    let embeddings = Rc::new(embeddings);

    application.connect_activate(move |app| {
        build_ui(app, embeddings.clone());
    });

    application.run(&[]);
}
