use finalfusion::prelude::*;

mod metadata_model;
pub use self::metadata_model::*;

mod similarity_model;
pub use self::similarity_model::*;

pub trait EmbeddingsModel {
    fn embeddings(&self) -> &Embeddings<VocabWrap, StorageViewWrap>;
}
