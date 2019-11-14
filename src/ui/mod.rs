use crate::models::EmbeddingsModel;

mod analogy_widget;
pub use self::analogy_widget::AnalogyWidget;

mod basic_dialogs;
pub use self::basic_dialogs::{open_embeddings, show_error};

mod inspector_window;
pub use self::inspector_window::InspectorWindow;

mod metadata_dialog;
pub use self::metadata_dialog::MetadataDialog;

mod similarity_widget;
pub use self::similarity_widget::SimilarityWidget;

mod subwords_widget;
pub use self::subwords_widget::SubwordsWidget;

pub trait EmbeddingsWidget {
    fn model(&self) -> &dyn EmbeddingsModel;

    fn update_validity(&self);
}
