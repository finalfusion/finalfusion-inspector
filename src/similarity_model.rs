use std::rc::Rc;

use finalfusion::prelude::*;
use finalfusion::similarity::WordSimilarity;
use gtk::prelude::*;
use gtk::ListStore;

use crate::model::{EmbeddingsExt, EmbeddingsModel};

pub struct SimilarityModel {
    embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>,
    inner: ListStore,
}

impl SimilarityModel {
    pub fn new(embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) -> Self {
        let model = ListStore::new(&[String::static_type(), f32::static_type()]);

        SimilarityModel {
            embeddings,
            inner: model,
        }
    }

    /// Execute an analogy query.
    pub fn analogy(&self, query: [impl AsRef<str>; 3]) {
        self.clear();

        // Unwrapping should be safe here, since we only allow words for
        // which an embedding can be computed.
        let similar_words = self.embeddings.analogy_flexible(query, 20).unwrap();

        for similar_word in similar_words {
            self.inner.insert_with_values(
                None,
                &[0, 1],
                &[&similar_word.word, &similar_word.similarity.into_inner()],
            );
        }
    }

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    /// Execute a similarity query.
    pub fn similarity(&self, word: &str) {
        self.clear();

        let similar_words = match self.embeddings.word_similarity(word, 20) {
            Some(results) => results,
            None => return,
        };

        for similar_word in similar_words {
            self.inner.insert_with_values(
                None,
                &[0, 1],
                &[&similar_word.word, &similar_word.similarity.into_inner()],
            );
        }
    }

    pub fn model(&self) -> ListStore {
        self.inner.clone()
    }
}

impl EmbeddingsModel for SimilarityModel {
    fn embeddings(&self) -> &Embeddings<VocabWrap, StorageViewWrap> {
        &self.embeddings
    }
}
