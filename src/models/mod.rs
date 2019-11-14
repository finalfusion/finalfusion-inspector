use std::rc::Rc;

use finalfusion::prelude::*;

mod metadata_model;
pub use self::metadata_model::*;

mod similarity_model;
pub use self::similarity_model::*;

mod subwords_model;
pub use self::subwords_model::*;

use crate::embeddings_ext::WordStatus;

pub trait EmbeddingsModel {
    fn word_status(&self, word: &str) -> WordStatus;

    fn switch_embeddings(&self, embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>);
}
