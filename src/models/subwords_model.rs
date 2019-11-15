use std::cell::RefCell;
use std::rc::Rc;

use finalfusion::prelude::*;
use finalfusion::vocab::NGramIndices;
use gtk::prelude::*;
use gtk::ListStore;

use crate::embeddings_ext::{EmbeddingsExt, WordStatus};
use crate::models::EmbeddingsModel;

pub struct SubwordsModel {
    embeddings: RefCell<Rc<Embeddings<VocabWrap, StorageViewWrap>>>,
    inner: ListStore,
}

impl SubwordsModel {
    pub fn new(embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) -> Self {
        let model = ListStore::new(&[String::static_type(), i64::static_type()]);

        SubwordsModel {
            embeddings: RefCell::new(embeddings),
            inner: model,
        }
    }

    /// Clear the model.
    fn clear(&self) {
        self.inner.clear();
    }

    /// Execute a subword query.
    pub fn subwords(&self, word: &str) {
        self.clear();

        let embeddings = self.embeddings.borrow();

        let subword_vocab: &dyn NGramIndices = match embeddings.vocab() {
            VocabWrap::BucketSubwordVocab(ref vocab) => vocab,
            VocabWrap::ExplicitSubwordVocab(ref vocab) => vocab,
            VocabWrap::FastTextSubwordVocab(ref vocab) => vocab,
            VocabWrap::SimpleVocab(_) => return,
        };

        let ngram_indices = match subword_vocab.ngram_indices(word) {
            Some(ngrams) => ngrams,
            None => return,
        };

        for (ngram, idx) in ngram_indices {
            // There is no embedding for the n-gram if it does not
            // have an index.
            let idx = match idx {
                Some(idx) => idx,
                None => continue,
            };

            self.inner
                .insert_with_values(None, &[0, 1], &[&ngram, &(idx as i64)]);
        }
    }

    pub fn model(&self) -> ListStore {
        self.inner.clone()
    }
}

impl EmbeddingsModel for SubwordsModel {
    fn word_status(&self, word: &str) -> WordStatus {
        self.embeddings.borrow().word_status(word)
    }

    fn switch_embeddings(&self, embeddings: Rc<Embeddings<VocabWrap, StorageViewWrap>>) {
        self.clear();
        *self.embeddings.borrow_mut() = embeddings;
    }
}
