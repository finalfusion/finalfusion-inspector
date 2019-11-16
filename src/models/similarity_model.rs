use std::cell::RefCell;
use std::f32;
use std::rc::Rc;

use finalfusion::prelude::*;
use finalfusion::similarity::WordSimilarity;
use gtk::prelude::*;
use gtk::ListStore;

use crate::embeddings_ext::{EmbeddingsExt, WordStatus};
use crate::models::EmbeddingsModel;

/// A model of word similarity.
///
/// The model has the following columns:
///
/// * 0: Word
/// * 1: Cosine similarity
/// * 2: Cosine similarity as a string with 2 digits
/// * 3: Cosine similarity as a percentage
pub struct SimilarityModel {
    embeddings: RefCell<Rc<Embeddings<VocabWrap, StorageViewWrap>>>,
    inner: ListStore,
}

impl SimilarityModel {
    pub fn new(embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) -> Self {
        let model = ListStore::new(&[
            String::static_type(),
            f32::static_type(),
            String::static_type(),
            i32::static_type(),
        ]);

        SimilarityModel {
            embeddings: RefCell::new(embeddings),
            inner: model,
        }
    }

    /// Execute an analogy query.
    pub fn analogy(&self, query: [impl AsRef<str>; 3]) {
        self.clear();

        let embeddings = self.embeddings.borrow();

        // Unwrapping should be safe here, since we only allow words for
        // which an embedding can be computed.
        let similar_words = embeddings.analogy_flexible(query, 20).unwrap();

        for similar_word in similar_words {
            let angular_similarity = Self::angular_similarity(similar_word.similarity.into_inner());

            self.inner.insert_with_values(
                None,
                &[0, 1, 2, 3],
                &[
                    &similar_word.word,
                    &similar_word.similarity.into_inner(),
                    &format!("{:.2}", similar_word.similarity),
                    &((angular_similarity * 100f32) as i32),
                ],
            );
        }
    }

    fn angular_similarity(cosine_similarity: f32) -> f32 {
        1f32 - (cosine_similarity.acos() / f32::consts::PI)
    }

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    /// Execute a similarity query.
    pub fn similarity(&self, word: &str) {
        self.clear();

        let embeddings = self.embeddings.borrow();

        let similar_words = match embeddings.word_similarity(word, 20) {
            Some(results) => results,
            None => return,
        };

        for similar_word in similar_words {
            let angular_similarity = Self::angular_similarity(similar_word.similarity.into_inner());

            self.inner.insert_with_values(
                None,
                &[0, 1, 2, 3],
                &[
                    &similar_word.word,
                    &similar_word.similarity.into_inner(),
                    &format!("{:.2}", similar_word.similarity),
                    &((angular_similarity * 100f32) as i32),
                ],
            );
        }
    }

    pub fn model(&self) -> ListStore {
        self.inner.clone()
    }
}

impl EmbeddingsModel for SimilarityModel {
    fn word_status(&self, word: &str) -> WordStatus {
        self.embeddings.borrow().word_status(word)
    }

    fn switch_embeddings(&self, embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) {
        self.clear();
        *self.embeddings.borrow_mut() = embeddings;
    }
}
