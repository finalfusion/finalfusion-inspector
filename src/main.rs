use std::fs::File;
use std::io::BufReader;
use std::process;
use std::rc::Rc;

use clap::{App, AppSettings, Arg};
use finalfusion::prelude::*;
use gio::prelude::*;
use gtk::prelude::*;

#[macro_use]
pub mod clone;

mod embeddings_ext;

pub mod models;

pub mod ui;

static EMBEDDINGS: &str = "EMBEDDINGS";

static DEFAULT_CLAP_SETTINGS: &[AppSettings] = &[
    AppSettings::DontCollapseArgsInUsage,
    AppSettings::UnifiedHelpMessage,
];

fn open_embeddings(filename: Option<&str>) -> Embeddings<VocabWrap, StorageViewWrap> {
    let filename = filename
        .map(Into::into)
        .or_else(ui::open_embeddings)
        .unwrap_or_else(|| process::exit(1));

    let file = File::open(&filename).unwrap_or_else(|err| {
        ui::show_error(format!(
            "Cannot open {}: {}",
            filename.to_string_lossy(),
            err
        ));
        process::exit(1);
    });

    let embeddings: Embeddings<VocabWrap, StorageViewWrap> =
        Embeddings::mmap_embeddings(&mut BufReader::new(file)).unwrap_or_else(|err| {
            ui::show_error(format!(
                "Cannot read {}: {}",
                filename.to_string_lossy(),
                err
            ));
            process::exit(1);
        });

    embeddings
}

fn build_ui(
    application: &gtk::Application,
    embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>,
) {
    let window = ui::InspectorWindow::new(application, embeddings);
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

    let embeddings = Rc::new(open_embeddings(matches.value_of(EMBEDDINGS)));

    application.connect_activate(move |app| {
        build_ui(app, embeddings.clone());
    });

    application.run(&[]);
}
