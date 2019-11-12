use std::rc::Rc;

use finalfusion::prelude::*;
use finalfusion::similarity::WordSimilarity;
use gtk::prelude::*;
use gtk::ListStore;

use crate::model::EmbeddingsModel;

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

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    /// Execute a query.
    pub fn query(&self, word: &str) {
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
